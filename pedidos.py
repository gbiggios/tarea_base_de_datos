import os

class Pedidos:
    archivo_contador='contador.txt'
    def __init__(self, _id, fecha, cliente, platos, total):
        
        self._id = _id
        self.fecha = fecha
        self.cliente = cliente
        self.platos = platos
        self.total = total

    def toDBCollection(self):
        # Convierte los atributos del objeto en un diccionario para insertarlo en la colección
        return {
            "_id": self._id,
            "fecha": self.fecha,
            "cliente": self.cliente,
            "platos": self.platos,
            "total": self.total
        }


    def _cargar_contador(self):
        if os.path.exists(self.archivo_contador):
            with open(self.archivo_contador, 'r') as archivo:
                return int(archivo.read())  # Convert to integer
        else:
            return 0

    def _guardar_contador(self):
        with open(self.archivo_contador, 'w') as archivo:
            archivo.write(str(self._id))  # Write as a string

def insertar_documento(doc, coleccion_objetivo):
    while True:
        cursor = coleccion_objetivo.find({}, {"_id": 1}).sort([("_id", -1)]).limit(1)
        seq = cursor.next()["_id"] + 1 if cursor.hasNext() else 1
        doc["_id"] = seq
        resultados = coleccion_objetivo.insert(doc)
        if resultados.hasWriteError():
            if resultados.writeError.code == 11000:  # Clave duplicada
                continue
            else:
                print("Error inesperado al insertar datos:", resultados)
        break