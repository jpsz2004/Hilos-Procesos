import threading
import random
import time


def inicio_carrera():
    """
    Callback que se ejecuta de forma autom�tica justo en el momento 
    en que la barrera se libera (cuando el �ltimo participante llama a wait()).
    """
    print("--- �CARRERA! ---")

def auto(id_auto: int, barrera: threading.Barrier):
    """
    Simula el comportamiento individual de cada auto.
    
    Args:
        id_auto: Identificador �nico del auto.
        barrera: Objeto de sincronizaci�n (Barrier) para alinear las salidas.
    """
    # 1. Simulaci�n del tiempo aleatorio para 'llegar a la pista'
    tiempo_llegada = random.uniform(0.5, 3.0)
    time.sleep(tiempo_llegada)
    
    # 2. El auto avisa que lleg� y se queda bloqueado esperando a los dem�s
    print(f"Auto {id_auto} lleg� a la salida y est� esperando.")
    barrera.wait()
    
    # 3. La barrera fue superada, comienza la carrera para todos simult�neamente
    print(f"Auto {id_auto} inici� la carrera.")

def main():
    CANTIDAD_AUTOS = 5
    
    # Se crea la barrera configurada para 5 hilos.
    # El par�metro 'action' permite ejecutar una funci�n en el instante exacto en que se rompe la barrera.
    barrera = threading.Barrier(CANTIDAD_AUTOS, action=inicio_carrera)
    
    hilos_autos = []
    
    # Se crean e inician los hilos que simular�n los autos
    for i in range(1, CANTIDAD_AUTOS + 1):
        hilo = threading.Thread(target=auto, args=(i, barrera))
        hilos_autos.append(hilo)
        hilo.start()
        
    # Buena pr�ctica: Esperar a que todos los hilos concluyan su ejecuci�n 
    # para no tener procesos 'zombies' y hacer una salida limpia del script principal.
    for hilo in hilos_autos:
        hilo.join()

if __name__ == "__main__":
    main()
