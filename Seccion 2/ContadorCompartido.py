import threading

contador = 0
lock = threading.Lock()

class ContadorSeguro:
    def __init__(self):
        self.valor = 0
        self.lock = threading.Lock()

    def incrementar(self):
        if not self.lock.locked():  # Condición de carrera potencial, porque otro hilo podría adquirir el lock después de esta verificación
            with self.lock:
                self.valor += 1
        else:
            pass # Si el lock está ocupado, simplemente se omite la operación, lo que puede llevar a un conteo incorrecto.

contador_obj = ContadorSeguro()

def tarea():
    for _ in range(100000):
        contador_obj.incrementar()

hilos = [threading.Thread(target=tarea) for _ in range(10)]
for h in hilos:
    h.start()
for h in hilos:
    h.join()

print(f"Valor final del contador: {contador_obj.valor}")

# ---------------------------------- CORRECIÓN ----------------------------------
# El código anterior tiene un problema de condición de carrera debido a la verificación del lock antes de adquirirlo.
# Esto puede llevar a que múltiples hilos incrementen el contador al mismo tiempo, causando resultados incorrectos.
# La corrección es eliminar la verificación del lock y simplemente adquirirlo cada vez que se necesite incrementar el contador, asegurando que solo un hilo pueda modificar el valor a la vez.

import threading

class ContadorSeguro:
    def __init__(self):
        self.valor = 0
        self.lock = threading.Lock()

    def incrementar_batch(self, cantidad): # En lugar de incrementar de uno en uno, se incrementa en batch para reducir la cantidad de veces que se adquiere el lock
        with self.lock: #
            self.valor += cantidad # Se incrementa el contador en una sola operación crítica, lo que mejora la eficiencia y evita la condición de carrera.

contador_obj = ContadorSeguro()

def tarea():
    local = 0
    for _ in range(100000):
        local += 1 
    
    # Se hace una sola operación crítica para incrementar el contador con el valor acumulado local, lo que reduce la contención del lock y mejora el rendimiento.
    contador_obj.incrementar_batch(local) 

hilos = [threading.Thread(target=tarea) for _ in range(10)]

for h in hilos:
    h.start()

for h in hilos:
    h.join()

print(f"Valor final del contador: {contador_obj.valor}")