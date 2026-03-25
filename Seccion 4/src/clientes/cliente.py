import random
import time
from modelo.trabajo import Trabajo

def cliente(nombre, tipo, cola):
    cantidad =  random.randint(5, 10)

    for i in range(cantidad):
        time.sleep(random.uniform(0.1, 0.5)) # Simular tiempo entre solicitudes

        trabajo = Trabajo(f"VIDEO-{nombre}-{i}", tipo, nombre)
        cola.agregar_trabajo(trabajo)