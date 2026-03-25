import threading

from cola.cola_prioridad import ColaPrioridad
from clientes.cliente import cliente
from workers.worker import worker
from utils.constantes import PREMIUM, FREE

def main():
    cola = ColaPrioridad()

    # Workers: Se crean 3 hilos (workers) para procesar los trabajos de la cola.
    workers_threads = [
        threading.Thread(target=worker, args=(i, cola))
        for i in range(1, 4)
    ]

    # Clientes
    clientes_threads = []

    # Premium (3)
    for i in range (1, 4):
        clientes_threads.append(
            threading.Thread(target=cliente, args=(f"Cliente-Premium-{i}", PREMIUM, cola))
        )
    
    # Free (5)
    for i in range (1, 6):
        clientes_threads.append(
            threading.Thread(target=cliente, args=(f"Cliente-Free-{i}", FREE, cola))
        )
    
    # Iniciar workers
    for w in workers_threads:
        w.start()
    
    # Iniciar clientes
    for c in clientes_threads:
        c.start()
    
    # Esperar a que los clientes terminen
    for c in clientes_threads:
        c.join()
    
    # Finalizar la cola para que los workers puedan terminar
    cola.finalizar()

    # Esperar a que los workers terminen
    for w in workers_threads:
        w.join()
    
    print("\n---SISTEMA FINALIZADO---")

if __name__ == "__main__":
    main()