import requests,json,os
from dotenv import load_dotenv

load_dotenv()

def log_in():
    """
    Establece conexión con la API-REST de InvertirOnline
    """
    url = "https://api.invertironline.com/token"
    user = os.environ.get("USER")
    password = os.environ.get("PASSWORD")
    data = {"username":user,"password":password,"grant_type":"password"}
    r = requests.post(url=url, data=data)
    access = json.loads(r.text)
    path = "./.env"

    with open(path,"r",encoding="utf-8") as handler:
        content = "".join([x for x in handler.readlines()[0:2]])

    with open(path,"w",encoding="utf-8") as handler:
        handler.write(content+"ACCESS-TOKEN='"+access["access_token"]+"'\nREFRESH-TOKEN='"+access["refresh_token"]+"'")



def get_options():
    """
    Obtenemos listas con las opciones del próximo ejercicio
    También devuelve el OPEX (Option Expiration Date)
    """

    vencimiento = "2021-06-18T00:00:00"
    headers = {"Authorization":"Bearer "+os.environ.get("ACCESS-TOKEN")}
    r2 = requests.get(url="https://api.invertironline.com/api/v2/bCBA/Titulos/GGAL/Opciones",headers = headers)
    r = json.loads(r2.text)
    
    opc = []
    for i in range(len(r)):
        if r[i]["fechaVencimiento"] == vencimiento:
            ticker = r[i]["simbolo"]
            base = r[i]["descripcion"].split(" ")[2]
            side = ticker[3]
            price = r[i]["cotizacion"]["ultimoPrecio"]
            opc.append([base,side,ticker,price])
    return opc, vencimiento

def get_equity(stock="GGAL"):
    """
    Obtenemos precios de GGAL
    """
    headers = {"Authorization": "Bearer " + os.environ.get("ACCESS-TOKEN")}
    r = requests.get(url="https://api.invertironline.com/api/v2/bCBA/Titulos/"+stock.upper()+"/Cotizacion",
                      headers= headers)

    return json.loads(r.text)["ultimoPrecio"]



log_in()

