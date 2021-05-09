import requests,json,os
from datetime import datetime,timedelta
from dotenv import load_dotenv

load_dotenv()
class Data_market:
    def __init__(self):
        self.dt_opex = self.get_opex()
        self.days_to_opex = (self.dt_opex-datetime.today()).days
        self.opex = self.dt_opex.strftime("%Y-%m-%dT") + "00:00:00"
        self.log_in()


    def log_in(self):
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
            content = "".join([x for x in handler.readlines()[0:3]])

        with open(path,"w",encoding="utf-8") as handler:
            handler.write(content+"ACCESS-TOKEN='"+access["access_token"]+"'\nREFRESH-TOKEN='"+access["refresh_token"]+"'")



    def get_options(self,stock="GGAL"):
        """
        Obtenemos listas con las opciones del próximo ejercicio
        También devuelve el OPEX (Option Expiration Date)
        """

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

    def get_equity(self,stock="GGAL"):
        """
        Obtenemos precios de GGAL
        """
        headers = {"Authorization": "Bearer " + os.environ.get("ACCESS-TOKEN")}
        r = requests.get(url="https://api.invertironline.com/api/v2/bCBA/Titulos/"+stock.upper()+"/Cotizacion",
                        headers= headers)

        return json.loads(r.text)["ultimoPrecio"]

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


            
