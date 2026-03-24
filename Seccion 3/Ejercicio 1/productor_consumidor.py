import threading
import time
import random

class BufferCompartido:
    def __init__(self, capacidad):
        self.buffer = []
        self.capacidad = capacidad
        self.condicion = threading.Condition() # Condición para sincronizar el acceso al buffer
        self.produccion_terminada = False
    
    def producir(self, item):
        with self.condicion:
            while len(self.buffer) == self.capacidad:
                self.condicion.wait() # Espera si el buffer está lleno

                self.buffer.apend(item) # Agrega el item al buffer
                print(f"Productor: Tarea {item} añadida. Buffer: [{self.buffer}]")

                self.condicion.notify_all() # Notifica a los consumidores que hay un nuevo item
    
    def consumir(self, id_consumidor):
        with self.condicion:
            while len(self.buffer) == 0:
                if self.produccion_terminada:
                    return None # Si la producción ha terminado y el buffer está vacío, el consumidor puede terminar
                self.condicion.wait() # Espera si el buffer está vacío
            
            item = self.buffer.pop(0) # Consume el primer item del buffer
            print(f"Consumidor-{id_consumidor}: Tomó tarea {item}. Buffer: [{self.buffer}]")

            self.condicion.notify_all() # Notifica a los productores que hay espacio en el buffer
            return item