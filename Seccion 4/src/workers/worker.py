import time
import random

# Thread Pool: Se usan 3 hilos (workers) para procesar los trabajos de la cola, no se crean hilos por cada trabajo, sino que los mismos hilos van a ir tomando trabajos de la cola y procesándolos. Esto es más eficiente y evita la sobrecarga de crear y destruir hilos constantemente.

def worker(id_worker, cola):
    while True:
        trabajo = cola.obtener_trabajo()

        if trabajo is None:
            break

        print(f"Worker-{id_worker}: Procesando {trabajo.id_video} de {trabajo.cliente}")

        time.sleep(random.uniform(0.5, 1.5)) # Simular tiempo de procesamiento