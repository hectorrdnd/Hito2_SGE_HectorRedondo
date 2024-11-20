import pymysql
from pymysql.err import OperationalError

def conectar():
    try:
        conexion = pymysql.connect(
            host='localhost',
            user='root',
            password='curso',
            database='encuestas'
        )
        print("Conexión exitosa a la base de datos")
        return conexion
    except OperationalError as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

def cerrar_conexion(conexion):
    if conexion:
        conexion.close()
        print("Conexión cerrada")