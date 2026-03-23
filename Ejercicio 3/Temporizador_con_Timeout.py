import threading
import random
import time

def conectar_a_servicio() -> str:
    """Simula una conexi�n a un servicio que tarda entre 1 y 5 segundos."""
    tiempo_espera = random.randint(1, 5)
    time.sleep(tiempo_espera)
    return "Conectado"

def timeout_expirado(evento_cancelacion: threading.Event):
    """Callback que activa el evento tras el timeout (2s)."""
    print("Timeout: La conexi�n tard� demasiado. Operaci�n cancelada.")
    evento_cancelacion.set()

def realizar_conexion(evento_cancelacion: threading.Event, resultado: list):
    """Ejecuta la conexi�n en un hilo separado para no bloquear el programa principal."""
    try:
        resultado_conexion = conectar_a_servicio()
        # Si termina la conexi�n y no se cancel� por timeout, se avisa del �xito
        if not evento_cancelacion.is_set():
            resultado.append(resultado_conexion)
            evento_cancelacion.set() # Despierta al wait() del main
    except Exception as e:
        print(f"Error en la conexi�n: {e}")

def main():
    # 1. Se crea el evento de cancelaci�n
    evento_cancelacion = threading.Event()
    
    # Lista compartida para traer el resultado (Python usa referencias)
    resultado = []
    
    # 2. Se inician el Timer (2 segundos) y el Hilo de la conexi�n
    temporizador = threading.Timer(2.0, timeout_expirado, args=(evento_cancelacion,))
    hilo_conexion = threading.Thread(target=realizar_conexion, args=(evento_cancelacion, resultado))
    
    temporizador.start()
    hilo_conexion.start()
    
    # 3. El hilo principal espera a que pase el Evento (�xito o timeout)
    evento_cancelacion.wait()
    
    # 4. Evaluamos qui�n activ� el evento revisando si la lista resultado tiene elementos
    if resultado:
        temporizador.cancel() # Buena pr�ctica: cancelar el temporizador por seguridad
        print(f"Conexi�n exitosa: {resultado[0]}")
    
    # Esperamos a que el hilo libere sus recursos del time.sleep en background
    hilo_conexion.join()

if __name__ == "__main__":
    main()
