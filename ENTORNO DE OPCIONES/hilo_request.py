import threading
import iol_request
import logging
import time

logging.basicConfig(level=logging.INFO,format=" [%(levelname)s] (%(threadName)-s) %(message)s ")


class Hilo_update(threading.Thread):
    def __init__(self,name):
        threading.Thread.__init__(self,name="Hilo_update",target = Hilo_update.run)
        self.name = name

    def __str__(self):
        return "Hilo que obtiene datos constantemente."

    def run(self):
        self.bearer_token, self.refresh_token = iol_request.log_in()
        logging.info("Loggeandose en API...")
        init_bearer = time.time()
        while True:
            t1 = time.time()
            self.opciones, self.vencimiento_opc = iol_request.get_options(self.bearer_token)
            self.ggal = iol_request.get_ggal(self.bearer_token)
            self.days_to_opex = iol_request.get_opex(self.vencimiento_opc)
            t2 = time.time()

            time.sleep(60)

            print()
            logging.info("GGAL: "+str(self.ggal))
            logging.info("OPCIONES ACTUALIZADAS! ")
            logging.info("Update en: " + str(t2 - t1))
            if t2 - init_bearer > 840:
                self.bearer_token,self.refresh_token = iol_request.refresh(self.refresh_token)
                init_bearer = time.time()
                logging.info("Token actualizado!")
            else:
                logging.info("Tiempo desde bearer token: " + str(t2 - init_bearer))
            print()


#hilo = Hilo_update("update")
#hilo.start()