import threading

# Se aplica patrón Monitor para gestionar el acceso concurrente a las colas de trabajos. La condición se utiliza para sincronizar el acceso a las colas y controlar el flujo de procesamiento de trabajos premium y gratis.

# Se aplica patrón Productor-Consumidor para manejar la producción de trabajos por parte de los clientes y el consumo por parte de los editores. Los clientes producen trabajos que se agregan a las colas, mientras que los editores consumen trabajos de las colas siguiendo las reglas de prioridad establecidas.

# Se aplica Strategy en la definición de la lógica de prioidad para el procesamiento de trabajos. La estrategia de prioridad se implementa en el método `obtener_trabajo`, donde se decide si procesar un trabajo premium o gratis basado en el contador de trabajos premium procesados y el límite establecido.

class ColaPrioridad:
    def __init__(self, limite_premium=3):
        self.premium_queue = []
        self.free_queue = []
        self.condition = threading.Condition() # Condición para sincronizar el acceso a las colas
        self.contador_premium = 0 # Contador para controlar el número de trabajos premium procesados consecutivamente
        self.limite_premium = limite_premium # Límite de trabajos premium antes de procesar uno gratis
        self.trabajos_pendientes = 0
        self.finalizado = False


    def agregar_trabajo(self, trabajo):
        with self.condition:
            if trabajo.tipo == "premium":
                self.premium_queue.append(trabajo)
            else:
                self.free_queue.append(trabajo)
            
            self.trabajos_pendientes += 1

            print(f"{trabajo.cliente}: Envió trabajo [{trabajo.id_video}]")

            self.condition.notify_all() # Notificar a los editores que hay un nuevo trabajo disponible
    
    def obtener_trabajo(self):
        with self.condition:
            while self.trabajos_pendientes == 0 and not self.finalizado:
                self.condition.wait() # Esperar hasta que haya trabajos disponibles

            if self.trabajos_pendientes == 0 and self.finalizado:
                return None
            
            # Lógica de prioridad con fairness: Procesar hasta `limite_premium` trabajos premium antes de procesar uno gratis
            if (self.premium_queue and
                (self.contador_premium < self.limite_premium or not self.free_queue)):

                trabajo = self.premium_queue.pop(0)
                self.contador_premium += 1 
            else:
                trabajo = self.free_queue.pop(0)
                self.contador_premium = 0 # Reiniciar el contador de premium después de procesar un trabajo gratis
            
            self.trabajos_pendientes -= 1

            self.condition.notify_all() # Notificar a los clientes que hay espacio en las colas
            return trabajo
    
    def finalizar(self):
        with self.condition:
            self.finalizado = True
            self.condition.notify_all() # Notificar a los editores para que puedan finalizar si no hay más trabajos pendientes
    