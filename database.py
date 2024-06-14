import pymongo

class Restaurante:
    def __init__(self):
        self.myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        self.mydb = self.myclient["restaurante"]
        self.mycol = self.mydb["pedidos"]

    def dbConnection(self):
        try:
            db = self.mydb  # Use the existing self.myclient directly
        except ConnectionError:
            print('Error de conexión con la bd')
        return db
