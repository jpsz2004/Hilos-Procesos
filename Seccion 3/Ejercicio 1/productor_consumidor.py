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

            self.buffer.append(item) # Agrega el item al buffer
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


# El productor no debe poder añadir una tarea si el buffer está lleno.
def productor(buffer):
    for i in range(1, 21):
        time.sleep(random.uniform(0.1, 0.5)) # Simula el tiempo de producción
        buffer.producir(i) # Produce una tarea

    with buffer.condicion:
        buffer.produccion_terminada = True # Indica que la producción ha terminado
        buffer.condicion.notify_all() # Notifica a los consumidores que no habrá más producción



def consumidor(buffer, id_consumidor):
    while True:
        item = buffer.consumir(id_consumidor) # Consume una tarea
        if item is None:
            break # Los consumidores no deben poder tomar una tarea si el buffer está vacío.

        time.sleep(random.uniform(0.5, 1.0)) # Simula el tiempo de consumo
        print(f"Consumidor-{id_consumidor}: Procesó tarea {item}.")


def main():
    buffer = BufferCompartido(capacidad=10)

    hilo_productor = threading.Thread(target=productor, args=(buffer,))
    consumidores = [
        threading.Thread(target=consumidor, args=(buffer, i))
        for i in range (1, 3) #Dos consumidores
    ]

    hilo_productor.start()

    for hilo in consumidores:
        hilo.start()

    hilo_productor.join() # Espera a que el productor termine

    for hilo in consumidores:
        hilo.join() # Espera a que los consumidores terminen
    
    print("\nTodas las tareas fueron procesadas")


if __name__ == "__main__":
    main()