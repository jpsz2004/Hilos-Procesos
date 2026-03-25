# Se aplica modelo de dominio para encapsular la información de cada tarea de edición de video. Cada trabajo tiene un ID de video, un tipo (premium o gratis) y un cliente asociado.

class Trabajo:
    def __init__(self, id_video, tipo, cliente):
        self.id_video = id_video
        self.tipo = tipo # Premium o gratis
        self.cliente = cliente
