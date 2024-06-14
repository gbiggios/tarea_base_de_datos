# Conexión a la base de datos
import pymongo
import os
from datetime import date

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["restaurante"]
mycol = mydb["pedidos"]

# Leer el valor actual del contador 
archivo_contador = 'contador.txt'
if os.path.exists(archivo_contador):
    with open(archivo_contador, 'r') as archivo:
        numPedido = int(archivo.read())
else:
    numPedido = 0

# Obtener los datos del pedido
fecha = date.today()
cliente = input('Ingrese el nombre del cliente: ')
plato = input('Ingrese el plato del cliente: ')
total = int(input('Ingrese el valor total: '))

# Crear el diccionario con los datos del pedido
mi_pedido = {
    '_id': numPedido,  # Usamos el contador como _id
    'fecha': str(fecha),
    'cliente': cliente,
    'plato': plato,
    'total': total
}

# Insertar el documento en la colección
x = mycol.insert_one(mi_pedido)

# Incrementar el contador
numPedido += 1

# Guardar el nuevo valor del contador en el archivo
with open(archivo_contador, 'w') as archivo:
    archivo.write(str(numPedido))

print(f"Pedido insertado con _id: {mi_pedido['_id']}")