import requests,json,os
import pandas as pd, numpy as np
import math, statistics
from datetime import datetime,timedelta
from dotenv import load_dotenv

load_dotenv()
class Data_market:
    def __init__(self):
        self.dt_opex = self.get_opex()
        self.today = datetime.today()
        self.days_to_opex = (self.dt_opex-self.today).days
        self.opex = self.dt_opex.strftime("%Y-%m-%dT") + "00:00:00"
        
        
        if not self.key_valid():
            self.log_in()


    def key_valid(self):
        is_valid = os.environ.get("VALID_TO")
        is_valid = datetime.strptime(is_valid,"%Y-%m-%d %H:%M:%S.%f")
        return True if datetime.now() < is_valid else False

    def log_in(self):
        """
        Establece conexión con la API-REST de InvertirOnline
        """
        path = "./.env"
        with open(path,"r",encoding="utf-8") as handler:
            content = "".join([x for x in handler.readlines()[0:3]])
        print("LOG IN")

        url = "https://api.invertironline.com/token"
        user = os.environ.get("USER")
        password = os.environ.get("PASSWORD")
        data = {"username":user,"password":password,"grant_type":"password"}
        r = requests.post(url=url, data=data)
        access = json.loads(r.text)

        valid_to = str(datetime.now()+timedelta(minutes=14,seconds=30))
        with open(path,"w",encoding="utf-8") as handler:
            handler.write(content+"VALID_TO='"+valid_to+"'\nACCESS-TOKEN='"+access["access_token"]+"'\nREFRESH-TOKEN='"+access["refresh_token"]+"'")


    def get_options(self,stock="GGAL"):
        """
        Obtenemos listas con las opciones del próximo ejercicio
        También devuelve el OPEX (Option Expiration Date)
        """
        if self.key_valid():
            headers = {"Authorization":"Bearer "+os.environ.get("ACCESS-TOKEN")}
            r2 = requests.get(url="https://api.invertironline.com/api/v2/bCBA/Titulos/"+stock.upper()+"/Opciones",headers = headers)
            r = json.loads(r2.text)
            
            opc = []
            for i in range(len(r)):
                if r[i]["fechaVencimiento"] == self.opex:
                    ticker = r[i]["simbolo"]
                    base = r[i]["descripcion"].split(" ")[2]
                    side = ticker[3]
                    price = r[i]["cotizacion"]["ultimoPrecio"]
                    opc.append([base,side,ticker,price])
            return opc
        else:
            pass
            #self.log_in()
            #self.get_options(stock)

    def get_equity(self,stock="GGAL"):
        """
        Obtenemos precios de GGAL
        """
        if self.key_valid():
            headers = {"Authorization": "Bearer " + os.environ.get("ACCESS-TOKEN")}
            r = requests.get(url="https://api.invertironline.com/api/v2/bCBA/Titulos/"+stock.upper()+"/Cotizacion",
                            headers= headers)

            return json.loads(r.text)["ultimoPrecio"]
        else:
            pass
            #self.log_in()
            #self.get_equity(stock)


    def third_friday(self,month,year):
        first_day = datetime(year,month,1)
        third_friday = 1 + abs(4 - first_day.weekday()) + 14
        return third_friday
 
    def get_opex(self):
        now = datetime.today()
        day,month, weekday,year = now.day,now.month,now.weekday(),now.year

        if month % 2 != 0:
            month += 1
        else:
            third_friday = self.third_friday(month,year)
            if day < third_friday:
                return datetime(year,month,third_friday)
            month += 2
            if month > 12:
                month %= 12
                year += 1
        return datetime(year,month,self.third_friday(month,year))

    def get_volatilidad_historica(self,stock,last=40,data=365):
        """
        Obtenemos precios de GGAL
        *56 días son 40 ruedas*
        """
        path = os.getcwd()+os.sep+"data"+os.sep+str(self.today.year)+"-"+str(self.today.month)+"-"+str(self.today.day)+"-"+str(stock)+"-"+str(last)+"-data.txt"
        if os.path.exists(path):
            with open(path,"r",encoding="utf-8") as handler:
                xaxis = handler.readline().replace("\n","").split(" ")
                yaxis = [np.nan if x == "nan" else float(x) for x in handler.readline().replace("\n","").split(" ")]
                ystock = [np.nan if x == "nan" else float(x) for x in handler.readline().replace("\n","").split(" ")]
                last = float(handler.readline().replace("\n",""))
        else:
            headers = {"Authorization": "Bearer " + os.environ.get("ACCESS-TOKEN")}
            from_ = datetime.today()
            to = from_ - timedelta(days=data)
            r3 = requests.get(url="https://api.invertironline.com/api/v2/bCBA/Titulos/"+stock.upper()+"/Cotizacion/seriehistorica/"+
                                to.strftime("%Y-%m-%d")+"/"+from_.strftime("%Y-%m-%d")+"/ajustada",
                            headers=headers)

            df = pd.DataFrame(columns=["Día","Minimo","Máximo","Cierre","Variacion","St Desv","Volatilidad"])
            df.set_index("Día",inplace=True)
            iterable = json.loads(r3.text)

            print(df)

            cierre_ant = 1
            fecha_ant = 0
            fecha_40 = iterable[0]["fechaHora"][:10]
            muestra = list()
            for i in range(len(iterable)):
                a = iterable[i]
                df.loc[a["fechaHora"][:10]] = [a["minimo"],a["maximo"],a["ultimoPrecio"],np.nan,np.nan,np.nan]
                variacion = (math.log(a["ultimoPrecio"] / cierre_ant)) * -1
                df.loc[fecha_ant,"Variacion"] = variacion

                if len(muestra) == last:
                    muestra.pop(0)
                    muestra.append(variacion)
                    desvio = statistics.stdev(muestra)
                    df.loc[fecha_40, "St Desv"] = desvio
                    df.loc[fecha_40, "Volatilidad"] = desvio * math.sqrt(252)
                    fecha_40 = iterable[i-40]["fechaHora"][:10]
                else:
                    muestra.append(variacion)
                    df.loc[fecha_40, "St Desv"] = None
                    df.loc[fecha_40, "Volatilidad"] = None

                fecha_ant = a["fechaHora"][:10]
                cierre_ant = a["ultimoPrecio"]


            print(df)
            xaxis, yaxis,ystock, last = list(df.index)[::-1], list(df.loc[:, "Volatilidad"])[::-1], list(df.loc[:, "Cierre"])[::-1], df.iloc[0,-1]
            df.to_excel('example.xlsx', sheet_name='Volatilidad Histótica')  
            with open(path,"w",encoding="utf-8") as handler:
                handler.write(" ".join([str(x) for x in xaxis])+"\n"+" ".join([str(y) for y in yaxis])+"\n"+" ".join([str(y) for y in ystock])+"\n"+str(last))
        return [xaxis[-data:-1],yaxis[-data:-1],ystock[-data:-1]],last
            

