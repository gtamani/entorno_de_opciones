import pyRofex
from datetime import datetime
import pandas as pd
import os


#Variables
dolar = 77.0517
posiciones_abiertas = 0
switch = True

#activos_disponibles = sorted([x["instrumentId"]["symbol"] for x in pyRofex.get_all_instruments(pyRofex.Environment.REMARKET)["instruments"]])

vencimientos = {"DOOct20":"2020-10-30",
                "DONov20":"2020-11-30",
                "DODic20":"2020-12-30",
                "DOEne21":"2021-01-29",
                "DOFeb21":"2021-02-26",
                "DOMar21":"2021-03-31",
                "DOAbr21":"2021-04-30",
                "DOMay21":"2021-05-31",
                "DOJun21":"2021-06-30",
                "DOJul21":"2021-07-30",
                "RFX20Dic20":"2020-12-30",
                "I.RFX20":"SPOT"}

#DataFrame
dataframe = pd.DataFrame( columns= ["Futuros","Precio","Brecha","Vencimiento","Días al vto","TNA","TEA"])
dataframe.set_index("Futuros",inplace=True)
for i in vencimientos.keys():
    dataframe.loc[i] = [None]*6
print(dataframe)
print()

#Inicio el entorno
file = open("C:/Users/Giuliano/Desktop/CODES/PYTHON/JSON/txt/datos cuenta.txt")
datos = [i.replace("\n","") for i in file.readlines()]
file.close()


pyRofex.initialize(user =  datos[0],
                   password = datos[1],
                   account = datos[2],
                   environment = pyRofex.Environment.REMARKET)



def shortear():
    global posiciones_abiertas, switch
    if switch is True:
        pyRofex.send_order("DOAbr20", 2, pyRofex.OrderType.LIMIT, pyRofex.Side.SELL)
        switch = False
        posiciones_abiertas += 1
    return None


#Funciones
def data_handler(event):
    global dolar, switch, posiciones_abiertas

    #Organizo datos
    instrumento = event["instrumentId"]["symbol"]
    vto = [int(x) for x in vencimientos[instrumento].split("-")]
    vto = datetime(vto[0],vto[1],vto[2])
    precio = round(event["marketData"]["LA"]["price"],2)
    brecha = round(precio - dolar,2)
    faltan = (vto - datetime.today()).days
    tna = round((((precio/dolar)-1)*(365/faltan)*100),2)
    tea = round((((precio/dolar)**(365/faltan))-1)*100,2)

    dataframe.loc[instrumento] = [precio,brecha,vto.strftime("%d/%m/%Y"),faltan,tna,tea]

    #print("{}  -----> PRECIO: {} | BRECHA: {} | VENCIMIENTO: {} | FALTAN {} DÍAS | TNA {}% | TEA {}%".format(instrumento,precio,brecha,vto.strftime("%d/%m/%Y"),faltan,tna,tea))

    shortear()
    print(switch,posiciones_abiertas)

    os.system("cls")
    print(dataframe)

    dataframe.to_excel("FUTUROS.xls")




def error_handler(event):
    print("Error: {}".format(event))

def order_report_handler(event):
    print("Event: {}".format(event))




#Conexión con WEBSOCKET
pyRofex.init_websocket_connection(market_data_handler= data_handler)
pyRofex.add_websocket_order_report_handler(order_report_handler)
pyRofex.add_websocket_error_handler(error_handler)

instruments = list(vencimientos.keys()) + ["RFX20Dic20","I.RFX20"] # Instruments list to subscribe
entries = [#pyRofex.MarketDataEntry.BIDS, #punta compradora
           #pyRofex.MarketDataEntry.OFFERS,
           pyRofex.MarketDataEntry.LAST]

#ESPECIFICAR LOS JASONS A ENVIAR EN EL DATA_ HANDLER
pyRofex.market_data_subscription(tickers=instruments,
                                 entries=entries)

pyRofex.send_order("DOAbr20",2,pyRofex.OrderType.LIMIT,pyRofex.Side.SELL)