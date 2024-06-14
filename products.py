from datetime import date
import os

class Pedidos:
    archivo_contador = "contador.txt"

    def __init__(self, id, fecha, cliente, platos, total):
        self.id = id
        self.fecha = fecha or None
        self.cliente = cliente or "Cliente desconocido"
        self.platos = platos or []
        self.total = total or 0

    def _cargar_contador(self):
        if os.path.exists(self.archivo_contador):
            with open(self.archivo_contador, 'r') as archivo:
                return int(archivo.read())
        else:
            return 0