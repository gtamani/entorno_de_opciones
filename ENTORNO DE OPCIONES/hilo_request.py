import threading
import iol_request
import logging
import time
import pyRofex
from bs4 import BeautifulSoup as b
import requests

class Hilo_update(threading.Thread):
    def __init__(self,name,pause):
        threading.Thread.__init__(self,name="Hilo_update",target = Hilo_update.run)
        self.name = name
        self.puntas_ggal = "Esperando puntas..."
        self.days_to_opex = 0
        self.pause = False
        self.first = True

    def __str__(self):
        return "Hilo que obtiene datos constantemente."


    def run(self,init=True):
        logging.basicConfig(level=logging.INFO, format=" [%(levelname)s] (%(threadName)-s) %(message)s ")

        if self.first:
            self.bearer_token, self.refresh_token = iol_request.log_in()
            self.coord, self.sigma_h = iol_request.get_volatilidad_historica(self.bearer_token,media=365)

            logging.info("Loggeandose en API...")

        lap = 0
        init_bearer = time.time()


        while self.pause is False:
            #print(self.coord)
            try:
                t1 = time.time()
                # Cargo Datos
                self.opciones, self.vencimiento_opc = iol_request.get_options(self.bearer_token)
                self.ggal = iol_request.get_ggal(self.bearer_token)
                self.puntas_ggal = iol_request.get_puntas("GGAL",self.bearer_token,all=True)

                if lap == 0:
                    self.days_to_opex = iol_request.get_opex(self.vencimiento_opc)

                lap += 1
                t2 = time.time()

                if t2 - init_bearer > 840:
                    self.bearer_token,self.refresh_token = iol_request.refresh(self.refresh_token)
                    init_bearer = time.time()
                    logging.info("Token actualizado!")
                else:
                    logging.info("Tiempo desde bearer token: " + str(t2 - init_bearer))

                #print()
                logging.info("GGAL: "+str(self.ggal))
                logging.info("OPCIONES ACTUALIZADAS! ")
                logging.info("Update en: " + str(t2 - t1))
                #print()

            except:
                print("\n"*10)
                print("ERRORRRRRRR")
                print("\n" * 10)

    def play_pause(self):
        if self.pause:
            self.pause = False
            self.run()
        else:
            self.pause = True

class Ggal_futuro(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self,name="ggal_futuro",target=Ggal_futuro.run)
        self.price = 0

        with open("C:/Users/Giuliano/Desktop/CODES/PYTHON/JSON/txt/datos cuenta.txt","r",encoding="utf-8") as file:
            datos = [i.replace("\n", "") for i in file.readlines()]

        pyRofex.initialize(user=datos[0],
                           password=datos[1],
                           account=datos[2],
                           environment=pyRofex.Environment.REMARKET)


    def run(self):
        time.sleep(10)
        pyRofex.init_websocket_connection(market_data_handler=self.data_handler)
        pyRofex.add_websocket_order_report_handler(self.order_report_handler)
        pyRofex.add_websocket_error_handler(self.error_handler)

        pyRofex.market_data_subscription(tickers=["GGALOct20"],entries=[pyRofex.MarketDataEntry.LAST])

    def data_handler(self,event):
        self.price = float(event["marketData"]["LA"]["price"])
        print(self.price)

    def error_handler(self,event):
        print("Error: {}".format(event))

    def order_report_handler(self,event):
        print("Event: {}".format(event))


class Ggal_adr(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self,name="ggal_adr",target=Ggal_adr.run)
        self.price = 0
        self.url = "http://www.rava.com/empresas/perfil.php?e=ADRGGAL&x=13&y=9"
        self.play = True

    def run(self):
        time.sleep(10)
        page = requests.get(self.url)
        while self.play:
            page = requests.get(self.url)
            if page.status_code == 200:
                soup = b(page.text, "html.parser")
                eq = soup.find("span", {"class": "fontsize6"}).text.replace(",", ".")
                self.price = float(eq)
                print(self.price)
            else:
                print("Error. Se salió del bucle")
                break

