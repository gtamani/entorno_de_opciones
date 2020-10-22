import threading
import iol_request
import logging
import time


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
            logging.info("Loggeandose en API...")

        lap = 0
        init_bearer = time.time()

        while self.pause is False:
            t1 = time.time()
            # Cargo Datos
            self.opciones, self.vencimiento_opc = iol_request.get_options(self.bearer_token)
            self.ggal = iol_request.get_ggal(self.bearer_token)
            self.puntas_ggal = iol_request.get_puntas("GGAL",self.bearer_token,all=True)

            if lap != 0:
                self.days_to_opex = iol_request.get_opex(self.vencimiento_opc)

            lap += 1
            t2 = time.time()

            if t2 - init_bearer > 840:
                self.bearer_token,self.refresh_token = iol_request.refresh(self.refresh_token)
                init_bearer = time.time()
                logging.info("Token actualizado!")
            else:
                logging.info("Tiempo desde bearer token: " + str(t2 - init_bearer))

            print()
            logging.info("GGAL: "+str(self.ggal))
            logging.info("OPCIONES ACTUALIZADAS! ")
            logging.info("Update en: " + str(t2 - t1))
            print()


    def play_pause(self):
        if self.pause:
            self.pause = False
            self.run()
        else:
            self.pause = True
