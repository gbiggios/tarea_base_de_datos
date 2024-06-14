import pymongo
import os
from datetime import date

class Restaurante:
    def __init__(self):
        self.myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        self.mydb = self.myclient["restaurante"]
        self.mycol = self.mydb["pedidos"]
        self.archivo_contador = 'contador.txt'
        self.numPedido = self._cargar_contador()

    def _cargar_contador(self):
        if os.path.exists(self.archivo_contador):
            with open(self.archivo_contador, 'r') as archivo:
                return int(archivo.read())
        else:
            return 0

    def _guardar_contador(self):
        with open(self.archivo_contador, 'w') as archivo:
            archivo.write(str(self.numPedido))

    def insertar_pedido(self):
        fecha = date.today()
        cliente = input('Ingrese el nombre del cliente: ')
        # Ahora permitimos ingresar múltiples platos separados por comas
        platos = input('Ingrese los platos del cliente (separados por comas): ').split(',')
        total = int(input('Ingrese el valor total: '))

        mi_pedido = {
            '_id': self.numPedido,
            'fecha': str(fecha),
            'cliente': cliente,
            'plato': platos,  # Campo "plato" ahora es una lista
            'total': total
        }

        x = self.mycol.insert_one(mi_pedido)
        self.numPedido += 1
        self._guardar_contador()

        print(f"Pedido insertado con _id: {mi_pedido['_id']}")

    def find_all(self):
    # Buscar todos los documentos en la colección
        cursor = self.mycol.find()
        documentos_encontrados = list(cursor)  # Convertir el cursor a una lista

        if documentos_encontrados:
            for documento in documentos_encontrados:
                print(documento)
        else:
         print("No se han encontrado pedidos en la colección.")

    def pedido_cliente(self, nombre_cliente):
        consulta={'cliente':nombre_cliente}
        cursor = self.mycol.find(consulta)
        for documento in cursor:
            print(documento)

    def pedido_total(self, total_):
        consulta = {'total': {'$gte': int(total_)}} 
        cursor = self.mycol.find(consulta)
        for documento in cursor:
            print(documento)
    
    def del_many_byclient(self,nombre_cliente):#Todos los pedidos de un cliente
        consulta={'cliente':nombre_cliente}
        cliente_existente = self.mycol.find_one({'cliente': nombre_cliente})
        if cliente_existente:
            consulta = {'cliente': nombre_cliente}
            self.mycol.delete_many(consulta)
            print(f"Se eliminaron todos los pedidos del cliente '{nombre_cliente}'.")
        else:
            print(f"No se encontraron pedidos para el cliente '{nombre_cliente}'.")

    def insertar_varias_ordenes(self, num_ordenes):
        fecha = date.today()
        ordenes = []
        for i in range(num_ordenes):
            print(f"\nOrden {i + 1}:")
            cliente = input('Ingrese el nombre del cliente: ')
            platos = input('Ingrese los platos del cliente (separados por comas): ').split(',')
            total = int(input('Ingrese el valor total: '))

            # Genera un _id único para cada orden
            orden = {
            '_id': self.numPedido,  # Utiliza el contador actual como _id
            'fecha': str(fecha),
            'cliente': cliente,
            'plato': platos,
            'total': total
            }
            ordenes.append(orden)
            self.numPedido += 1
            self._guardar_contador()

        result = self.mycol.insert_many(ordenes)

        print(f"Se insertaron {len(result.inserted_ids)} órdenes.")


    def look_by_id(self,pedido_id):
        filtro = {'_id': pedido_id}
        cursor = self.mycol.find(filtro)

        for documento in cursor:
            print(documento)

    def actualizar_total_por_id(self, pedido_id, nuevo_total):
        filtro = {'_id': pedido_id}
        actualizacion = {'$set': {'total': nuevo_total}}
        self.mycol.update_one(filtro, actualizacion)
        print(f"Total actualizado para el pedido con _id {pedido_id}.")
    
    def agregar_entregado_a_todos(self):
        filtro = {}
        actualizacion = {'$set': {'entregado': False}}
        self.mycol.update_many(filtro, actualizacion)
        print("Se añadió el campo 'entregado' a todos los pedidos.")

    def borrar_base_de_datos(self):
        sw1=True
        while sw1==True:
            sw3=input('¿Está seguro que quiere borrar toda la base de datos? Si=1, No=0')
            if sw3=='1':
                self.myclient.drop_database("restaurante")
                print("Base de datos eliminada correctamente.")
                sw1=False
            elif sw3=='0':
                print('No se ha borrado nada')
                sw1=False
            else:
                print('Error respuesta inválida')

    def borrar_todos_los_pedidos(self):
        sw1=True
        while sw1==True:
            sw2=input('¿Está seguro que quiere borrar toda la base de datos? Esto es irreversible Si=1, No=0')
            if sw2=='1':
                self.mycol.delete_many({})
                print("Se eliminaron todos los documentos de la colección 'pedidos'.")
                sw1=False
            elif sw2=='0':
                print('No se ha borrado nada')
                sw1=False
            else:
                print('Error respuesta inválida')

