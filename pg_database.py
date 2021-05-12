from API_data import Data_market
import psycopg2
import dotenv, os
from datetime import datetime


dotenv.load_dotenv()
class Postgres_database:

    def __init__(self):
        self.options_columns = ["stock","ticker","price","strike","opex"]
        self.historial_columns = ["datetime","side","quantity","price","total","opcion"]
        self.tenencia_columns = ["options","quant","avg_price","current_price","total_value"]
        self.user_columns = ["username","creation_on","last_login"]

        self.database = {"options":self.options_columns, "historial":self.historial_columns,"tenencia":self.tenencia_columns,"users":self.user_columns}

        self.host = "localhost"
        self.database_name = "entorno_de_opciones"
        self.user = "postgres"
        self.password = os.environ.get("POSTGRESS_PASSWORD")

    def query(self,command):
        try:
            con = psycopg2.connect(
                host = self.host,
                database = self.database_name,
                user = self.user,
                password = self.password
            )
            print("connected!")

            cursor = con.cursor()
            cursor.execute(command)

            try:
                result =  cursor.fetchall()
                cursor.close()
                con.commit()
                con.close()
                return  result
            except:
                cursor.close()
                con.commit()
                con.close()
                print("saved!")
        except:
            raise "Error manipulating data."

    def insert_into(self,table,data):
        print(self.database)
        print("DATA: ",data)
        columns = "("+", ".join(self.database[table])+")"

        values = []
        for i in data:
            edit_data = "(" + ", ".join([str(x) if type(x) is int or type(x) is float else "'"+x+"'" if not x.startswith("to_timestamp") else x for x in i]) + ")"
            print(edit_data)
            values.append(edit_data)
        
        values = ", ".join(values)

        command= f"INSERT INTO {table} {columns} VALUES {values}"
        self.query(command)

    def delete(self,table,key,value):
        command = f"DELETE FROM {table} WHERE {key} = '{value}';"
        self.query(command)

    def select(self,table,columns="*",condition=None):

        command = f"SELECT {columns} FROM {table}"
        if condition:
            command += f" WHERE {condition};" if condition else ";"
        return self.query(command)

    def update(self,table,key,value,attribute_key,atribute_value):
        command = f"UPDATE {table} set {key}={value} WHERE {attribute_key}='{atribute_value}';"
        self.query(command)
    
    def multiple_update(self,table,key,atribute_key, dict_values): 

        command= f"UPDATE {table} SET {key} = CASE "

        for k,v in dict_values.items():
            command += f"WHEN {atribute_key} = '{k}' THEN {v} " 
        command += f"END WHERE {atribute_key} IN {tuple(dict_values.keys())}"
        self.query(command)

    def truncate(self,table):
        if table == "all":
            table = []
            for i in self.database.keys():
                table.append(i)
            table = ", ".join(table)
        command = f"TRUNCATE TABLE {table};"
        self.query(command)

db = Postgres_database()
#db.truncate("all")