from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from config import Config


def dbConnection():
    try:
        client = MongoClient(Config.MONGO_URI, server_api=ServerApi("1"))
        db = client["bibliotecas"]
        print("Conexión a la base de datos exitosa")
    except ConnectionError:
        print("Error de conexión con la base de datos")
    return db
