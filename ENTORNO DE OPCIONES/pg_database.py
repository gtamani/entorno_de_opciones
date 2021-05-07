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
        columns = "("+", ".join(self.database[table])+")"
        edit_data = "(" + ", ".join([str(x) if type(x) is int or type(x) is float else "'"+x+"'" if not x.startswith("to_timestamp") else x for x in data]) + ")"
        print(edit_data)

        command= f"INSERT INTO {table} {columns} VALUES {edit_data}"
        self.query(command)

    def select(self,table,columns="*",condition=None):

        command = f"SELECT {columns} FROM {table}"
        add = f" WHERE {condition};" if condition else ";"
        return self.query(command + add)

    def update(self,table,key,value):
        command = f"UPDATE {table} set {key}={value};"
        self.query(command)

db = Postgres_database()
#print(db.update("users","last_login","to_timestamp("+str(datetime.timestamp(datetime.now()))+")"))
#print(dict(db.select("users",columns="username,last_login")))
#db.query("ALTER TABLE historial ADD COLUMN opcion varchar(20)")
print(db.select("historial"))