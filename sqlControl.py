import pyodbc
import pandas as pd

class Sql_conexion:

    def __init__(self, server, db, user, password, query):
        self.server = server
        self.db = db
        self.user = user
        self.password = password

        self.conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+db+';UID='+user+';PWD='+password)
        self.cursor = self.conn.cursor()
        self.query = query
        self.cursor.execute(self.query)
        self.description = self.cursor.description
        self.data = self.cursor.fetchall()
        self.conn.close()
    
    def get_data(self):
        return self.data

if __name__ == "__main__":
    table = ''
    query = (
        f"SELECT * "
        f"FROM {table} "

        # Example JOIN
        # f"JOIN dbo.Terceros Ter ON Fac.Tercero = Ter.Codigo "
        # f"JOIN dbo.Ubicaciones Ubi ON Fac.Ubicacion = Ubi.Codigo "

        # Example WHERE
        # f"WHERE Fecha >= '2024-01-01' AND Fecha <= '2024-01-01'"
    )
    conexion = Sql_conexion('example.com.co', 'dbname', 'user', 'password', query)
    rows = conexion.get_data()