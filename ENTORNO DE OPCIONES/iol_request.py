import requests
import json
from datetime import datetime

def log_in():
    """
    Establece conexión con la API-REST de InvertirOnline
    """
    print("ESTABLECIENDO CONEXION")

    url = "https://api.invertironline.com/token"

    user = input("User: ")
    password = input("Password: ")

    data = {"username":user,
            "password":password,
            "grant_type":"password"}

    r = requests.post(url=url, data=data)
    access = json.loads(r.text)

    return access["access_token"], access["refresh_token"]

def get_options(bearer_token):
    """
    Obtenemos listas con las opciones del próximo ejercicio
    También devuelve el OPEX (OPtion Expiration Date)
    """

    print("ENTRANDO A OPCIONES")

    headers = {"Authorization":"Bearer "+bearer_token}
    r2 = requests.get(url="https://api.invertironline.com/api/v2/bCBA/Titulos/GGAL/Opciones",
                                headers = headers)

    opciones_GGAL = json.loads(r2.text)
    print(opciones_GGAL)

    opc = []

    for i in range(len(opciones_GGAL)):
        side = opciones_GGAL[i]["tipoOpcion"]
        if opciones_GGAL[i]["fechaVencimiento"] == "2020-10-16T00:00:00":
                opc.append([opciones_GGAL[i]["simbolo"],opciones_GGAL[i]["cotizacion"]["ultimoPrecio"],
                            opciones_GGAL[i]["descripcion"].split(" ")[2]])

    return opc, opciones_GGAL[0]["fechaVencimiento"]

def get_ggal(bearer_token):
    """
    Obtenemos precios de GGAL
    """

    print("ENTRANDO A GGAL")

    headers = {"Authorization": "Bearer " + bearer_token}

    r3 = requests.get(url="https://api.invertironline.com/api/v2/bCBA/Titulos/GGAL/Cotizacion",
                      headers= headers)

    GGAL = json.loads(r3.text)
    GGAL = GGAL["ultimoPrecio"]

    return GGAL

def get_opex(string):
    """
    Devuelve tiempo hasta el vencimiento
    """
    year,month,day = int(string[:4]),\
                     int(string[5:7]),\
                     int(string[8:10])
    print(year,month,day)
    opex = datetime(year,month,day)
    today = datetime.today()
    remains = (opex - today).days
    return remains

#bearer_token, refresh_token = log_in()

#opciones, opex = get_options(bearer_token)





