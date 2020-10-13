"""
JUEGO OPCIONES


1. Crear la clase opción(base,side,vencimiento):                    LISTO
2. Crear todas las bases y meterlas en un diccionario               MEJOR EN UN DF
3. Crear la tenencia de las opciones                                                        FALTA
4. Crear un subyascente y sus variaciones RANDOM                    LISTO
5. Hacer que el comportamiento de las opciones tenga coherencia con el subyascente, respetando valor intrinseco y poniendo un valor extrinseco random     LISTO
6. Hacer grafico de resultado al vencimiento y resultado teórico    LISTO AL VTO            FALTA EL TEORICO
    A. Cotizacion fluyendo                                          LISTO
    B. Cuadro de posición                                           LISTO
    C. Agregar esos plots al tkinter                                LISTO
    D. Poner verde/rojo cuando titilen                              LISTO
    E. Poner los checkbox para cada opción                          LISTO
    F. Poner el formulario de cantidad para comprar y checks para market o limit   MEJOR NO
7. Hacer aplicación gráfica                                         LISTO
8. Guardar datos en .txt                                                                    FALTA


(ENTORNO DIDÁCTICO - PRÁCTICA)

.... and MOST IMPORTANT:
9. Conectar con Datos reales.                                                               FALTA
Para eso:
* Investigar conexión websocket de IOL                                                      FALTA
* Enlazar los JSON con las clases                                                           FALTA
* Crear un menú para elegir entre entorno práctica y entorno real                           FALTA


(ENTORNO REAL - OPERAR EN TIEMPO REAL)




CALCULAR SUMA CADA VEZ QUE HAYA UNA NUEVA COMPRA

TENER UN .TXT DE TODAS LAS POSICIONES





*LINEA X
*ARREGLAR GGAL
"""
from datetime import datetime
import time
import numpy as np
import random
import pandas as pd
import tkinter as tk
from tkinter import *
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.ticker as ticker
from scipy.stats import norm
import iol_request



"""
root = tk.Tk()
root.geometry("500x500")
root.title("Entorno de opciones GGAL")
root.pack_propagate(False)
root.resizable(0,0) #No puede agrandarse, ni achicarse la ventana


frame1 = tk.LabelFrame(root,text="Tabla")
frame1.place(height=250,width=500)

file_frame = tk.LabelFrame(root,text="Open File")
file_frame.place(height=100,width=400,rely=0.65,relx=0)

button1 = tk.Button(file_frame,text="Browse a File")
button1.place(rely=0.65,relx=0.5)

button2 = tk.Button(file_frame,text= "Load a File")
button2.place(rely=0.65,relx=0.3)

label_file = ttk.Label(file_frame,text="No file Selected")
label_file.place(rely=0,relx=0)

#Treeview Widget
tv1 = ttk.Treeview(frame1)
tv1.place(relheight=1,relwidth=1)

treescrolly = tk.Scrollbar(frame1,orient="vertical",command=tv1.yview)
treescrollx = tk.Scrollbar(frame1,orient="horizontal",command=tv1.xview)
tv1.configure(xscrollcommand = treescrollx.set,yscrollcommand= treescrolly.set)
treescrollx.pack(side="bottom",fill="x")
treescrolly.pack(side="right",fill="y")





root.mainloop()

"""


# Poner mayusculas a las clases
# Eliminar al vender






class Ggal:

    def __init__(self,price = 0):
        self.price = price
        self.pendientes = 0

    def __str__(self):
        return "GGAL"

class Contexto:

    def __init__(self,environment):
        self.environment = environment


        self.contextos = {1:{"Subiendo, muy volátil":[round(x,2) for x in np.arange(-1,4,0.1)]},
                     2:{"Subiendo, volatilidad media":[round(x,2) for x in np.arange(-1,3,0.1)]},
                     3:{"Subiendo, poca volatilidad": [round(x,2) for x in np.arange(-1,2,0.1)]},
                     4:{"Lateral, muy volátil": [round(x,2) for x in np.arange(-3,3,0.1)]},
                     5:{"Lateral, volatilidad media": [round(x,2) for x in np.arange(-2,2,0.1)]},
                     6:{"Lateral, poca volatilidad": [round(x,2) for x in np.arange(-1,1,0.1)]},
                     7:{"Bajando, muy volátil": [round(x,2) for x in np.arange(-4,1,0.1)]},
                     8:{"Bajando, volatilidad media": [round(x,2) for x in np.arange(-3,1,0.1)]},
                     9:{"Bajando, poca volatilidad": [round(x,2) for x in np.arange(-2,1,0.1)]}
                     }
        self.contexto = random.randint(1,9)
        self.possibilities = list(self.contextos[self.contexto].values())[0]
        self.vto = 0

    def __str__(self):
        return str(list(self.contextos[self.contexto].keys())[0]).upper()

    def sortear_contexto(self):
        print(random.randint(1, 9),list(self.contextos[self.contexto].values())[0])
        self.contexto = random.randint(1, 9)
        self.possibilities = list(self.contextos[self.contexto].values())[0]
        subyascente.price += random.choice(self.possibilities)

class Opcion:

    def __init__(self,base,side,ticker,prima=0):
        self.base = base
        self.side = side
        self.ticker = "GGAL_" + self.side + "_" + str(self.base) + "_10"

        if mi_contexto == 1:
            self.arbitrado = True
        else:
            self.arbitrado = None

        if self.side == "C":
            if subyascente.price >= self.base:
                self.prima = subyascente.price - self.base
                self.estado = True
            else:
                self.prima = 0.1
                self.estado = False
        else:
            if subyascente.price <= self.base:
                self.prima = self.base - subyascente.price
                self.estado = True
            else:
                self.prima = 0.1
                self.estado = False

        if mi_contexto != 1:
            self.ticker = ticker
            self.prima = prima



    def __str__(self):
        return self.ticker

    def restar_día(self,arbitrado):
        self.arbitrado = arbitrado

    def actualizar_prima(self):
        if self.side == "C":
            if subyascente.price >= self.base:
                self.estado = True
            else:
                self.estado = False
        else:
            if subyascente.price <= self.base:
                self.estado = True
            else:
                self.estado = False

        if self.arbitrado:
            if self.side == "C":
                if subyascente.price >= self.base:
                    self.prima = subyascente.price - self.base
                else:
                    self.prima = 0.1
            else:
                if subyascente.price <= self.base:
                    self.prima = self.base - subyascente.price
                else:
                    self.prima = 0.1

class Cartera:

    def __init__(self,efectivo):
        self.efectivo = efectivo
        self.acciones = 0
        self.opciones = 0
        self.total = efectivo
        self.suma = [0 for x in x]
        self.tenencia = df.loc[df["Cantidad"] != 0]

    def __str__(self):
        return "Mi Cartera"

    def buy_ggal(self,cant,market=True):
        if market:
            if self.efectivo >= cant * subyascente.price:
                self.efectivo -= cant * subyascente.price
                self.acciones += cant

        precio_conseguido = df.loc["GGAL", "Prima"]

        df.loc["GGAL", "Cantidad"] = self.acciones
        df.loc["GGAL", "Tenencia"] = df.loc["GGAL", "Prima"] * self.acciones

        total = (df.loc["GGAL", "Cantidad"])

        print("TOTALLLLLL",total,df.loc["GGAL", "PP"],cant)

        if cant > 0:
            try:
                df.loc["GGAL", "PP"] = round((df.loc["GGAL", "PP"] * (total - cant) + (
                        df.loc["GGAL", "Prima"] *
                        cant)) / total,2)
            except ZeroDivisionError:
                df.loc["GGAL","PP"] = 0

        recta = [round((x - precio_conseguido)*cant,2) for x in x]

        self.suma = [self.suma[x] + recta[x] for x in range(len(self.suma))]










    def buy_opc(self,cant,name,market,lote=100):
        """
        Baja efectivo
        """
        if market == "y":
            if self.efectivo >= cant * lote * df.loc[name,"Prima"]:
                print("ENTRAAAAAAA")
                self.efectivo -= cant * lote * df.loc[name,"Prima"]





    def actualizar_tenencia(self,tenencia):
        self.tenencia = tenencia

        print("PRIMIIIIIII ",self.tenencia)

        #Reuno los datos para pasarselo a la función
        total = list()
        for i in range(len(self.tenencia)):
            if self.tenencia.index[i] == "GGAL":
                total.append(["GGAL",self.tenencia.loc["GGAL","Prima"],self.tenencia.loc["GGAL","Cantidad"]])
            else:
                data = self.tenencia.index[i].split("_")
                if mi_contexto.environment == 1:
                    data = [data[1], data[2]]
                else:
                    data = data[0]
                    print("INDEX            ",df.index.get_loc(data))
                    data = [data[3],opciones[df.index.get_loc(data)].base]
                    pass

                print("DATA      ",data)
                total.append(data+list(self.tenencia.iloc[i]))
        self.suma = graph(total)




    def actualizar(self):
        self.opciones = round(sum(list(df.loc[df["Cantidad"] != 0, "Tenencia"])),2)
        print(self.opciones)






def y_graph(side,base,prima,cant,lote=100):
    """
    Determina la curva de una opción, sea call/put comprado/lanzado
    """
    global x


    if side == "C":
        """
        compra True = comprar call (view alcista)
        compra False = lanzar call (view bajista)
        """
        if cant > 0:
            return [-prima * lote *cant if x <= base else round((x - (base+prima)) * lote * cant,2) for x in x ]
        return [prima * lote * -cant if x <= base else round(((base+prima) - x) * lote * -cant ,2)  for x in x ]

    else:
        """
        compra True = comprar put (view bajista)
        compra False = lanzar put (view alcista)
        """
        if cant > 0:
            return [-prima * lote * cant if x >= base else round(((base-prima) - x) * lote * cant,2) for x in x]
        return [prima * lote * -cant if x >= base else round((x - (base - prima)) * lote * -cant,2) for x in x]

def graph(details):
    """
    Calcula los valores de Y para la suma de todos los activos en cartera.
    Valores que muestra el gráfico en pantalla
    """
    #print("SUMA: ",suma)
    #print("NEW: ",new)

    suma = [0 for x in x]

    for i in details:
        print(i)
        for j in range(len(suma)):
            if len(i) == 3:
                suma[j] += [(x-i[1]) * i[2] for x in x][j]
            else:
                suma[j] += y_graph(i[0],float(i[1]),i[2],i[3])[j]
    print(suma)
    return suma

def calculo_blackScholes(spot,strike,tiempo_al_vencimiento,type = "C"):
    """
    Cálculo teórico de valuación de opciones financieras.
    Parte del DataFrame.
    """
    #Variables
    interes = 0.3
    #spot = 108
    #strike = 104
    #tiempo_al_vencimiento = 14/365
    sigma = 0.3



    #Cálculo de
    d1 = (np.log(spot/strike) + (interes + sigma**2/2)*tiempo_al_vencimiento)/(sigma*np.sqrt(tiempo_al_vencimiento))
    d2 = d1 - sigma*np.sqrt(tiempo_al_vencimiento)

    try:
        if type == "C":
            price = spot*norm.cdf(d1,0,1) - strike*np.exp(-interes*tiempo_al_vencimiento) \
                    * norm.cdf(d2,0,1)
        elif type == "V":
            price = strike*np.exp(-interes*tiempo_al_vencimiento)*norm.cdf(-d2,0,1)\
            - spot*norm.cdf(-d1,0,1)

        return round(price,2)
    except:
        return "Error"

def comprar(activo,cant_comprada=1):
    """
    Comprar un activo, actualizar el DataFrame
    """
    global opcion

    if cant_comprada == 1:
        print("COMPRANDO", opcion.get())
    else:
        print("VENDIENDO", opcion.get())

    if activo == "GGAL":
        mi_cartera.buy_ggal(cant_comprada * 100)
    else:
        mi_cartera.buy_opc(cant_comprada,activo,"y")
        #Actualizo DataFrame
        df.loc[activo, "Cantidad"] += cant_comprada  # Nueva Cantidad
        total = (df.loc[activo, "Cantidad"])

        if cant_comprada > 0:
            try:
                df.loc[activo, "PP"] = round((df.loc[activo, "PP"] * (df.loc[activo, "Cantidad"] - cant_comprada) + (df.loc[activo, "Prima"] *
                                        cant_comprada)) / total,2)
            except ZeroDivisionError:
                df.loc[activo, "PP"] = 0

        df.loc[activo, "Tenencia"] = df.loc[activo, "Prima"] * df.loc[activo, "Cantidad"] * 100 # Tenencia

    df.loc[activo, "Cantidad"] = int(df.loc[activo, "Cantidad"])


    mi_cartera.actualizar_tenencia(df.loc[df["Cantidad"] != 0,["Prima","Cantidad"]])

    time.sleep(0.5)
    actualizar()

def mostrar_cartera():
    """
    Mostrar el rendimiento de mi cartera de activos.
    """
    pass

def actualizar():
    """
    Actualiza los datos de opciones, acciones y el paso del tiempo.
    También actualiza el gráfico
    """

    global figure,parar

    plt.close()

    t1 = time.time()

    #Destruyo texto anterior y creo el nuevo
    text1.delete("1.0", "end")
    text2.delete("1.0", "end")
    text4.delete("1.0", "end")

    if mi_contexto.environment == 1:
        if parar.get() == 0:
            #Paso del tiempo
            mi_contexto.vto += 1
            if mi_contexto.vto % 15 == 0:
                mi_contexto.sortear_contexto()

            #Actualizo GGAL
            subyascente.price += random.choice(mi_contexto.possibilities)
            df.loc["GGAL", "Cantidad"] = mi_cartera.acciones
            df.loc["GGAL", "Prima"] = subyascente.price
            df.loc["GGAL", "Tenencia"] = df.loc["GGAL", "Prima"] * mi_cartera.acciones
            if mi_cartera.acciones == 0:
                df.loc["GGAL","PP"] = 0



    #Actualizo gráfico
    figure.clear()
    figure = plt.figure(figsize=(5, 4), dpi=100)
    ax1 = figure.add_subplot(111)
    ax1.plot(x, mi_cartera.suma)
    if any(mi_cartera.suma) is False:
        rango = [0,100]
    else:
        rango = mi_cartera.suma

    ax2 = figure.add_subplot(111)
    ax2.plot((subyascente.price, subyascente.price), (max(rango), min(rango)))
    ax3 = figure.add_subplot(111)
    ax3.plot(x,[0 for x in x],color = "black",linewidth= 1)

    ax1.set_xlabel("Precio GGAL")
    ax1.set_ylabel("($) Ganancia")
    ax1.xaxis.set_major_formatter(ticks_x)
    ax1.yaxis.set_major_formatter(ticks_y)
    plt.xlim(subyascente.price-40,subyascente.price+40)

    #SUBPLOT = 1 RENGLON, 1 COLUMNA, POSICIÓN 1
    chart = FigureCanvasTkAgg(figure, root)
    chart.get_tk_widget().place(x=1150)


    if mi_contexto.environment == 1:
        text1.insert(tk.INSERT, df.iloc[[x for x in range(1, len(df) - 1, 2)]].to_string())  # Calls
        text2.insert(tk.INSERT, df.iloc[[x for x in range(2, len(df), 2)]].to_string())  # Puts
        text4.insert(tk.INSERT, "GGAL: \n" + df.loc["GGAL"].to_string())  # GGAL
    else:
        text1.insert(tk.INSERT, df.iloc[[x for x in range(1,len(df)) if df.index[x][3] == "C"]].to_string())  # Calls
        text2.insert(tk.INSERT, df.iloc[[x for x in range(1,len(df)) if df.index[x][3] == "V"]].to_string())  # Puts
        text4.insert(tk.INSERT, "GGAL: \n" + df.loc["GGAL"].to_string())  # GGAL

    #print([x for x in range(len(df)) if df.iloc[x,"Serie"][3] == "C"].to_string())
    print(len(df))
    print("LETRA:", [x for x in range(1,len(df)) if df.index[x][3] == "C"])
    print("LETRA:", [x for x in range(1,len(df)) if df.index[x][3] == "V"])


    renglon = 1

    if mi_contexto.environment == 1: #Entorno Práctica
        for i in opciones:
            #Actualizar precios de prima
            i.restar_día(random.choice([True,False,False,False,False]))
            i.actualizar_prima()

            if i.arbitrado:
                df.loc[i.ticker,"Prima"] = round(i.prima,2)

            df.loc[i.ticker,"B&Sch"] = calculo_blackScholes(subyascente.price,i.base,68/360,i.side)
            df.loc[i.ticker, "Tenencia"] = df.loc[i.ticker, "Prima"] * df.loc[i.ticker, "Cantidad"] * 100

            if df.loc[i.ticker, "Cantidad"] != 0:
                try:
                    df.loc[i.ticker, "Rendimiento"] = round(((df.loc[i.ticker, "Prima"] - df.loc[i.ticker, "PP"]) / df.loc[i.ticker, "PP"]) * 100, 2)
                except ZeroDivisionError:
                    df.loc[i.ticker, "Rendimiento"] = 0
            else:
                df.loc[i.ticker, "PP"] = 0
                df.loc[i.ticker, "Rendimiento"] = 0


            #Colores a las opciones DUPLICADOOOOOOOOOOOOOOOOOOOOOOOOO
            etiqueta, inicio, fin = "et" + str(renglon) + i.side, str(renglon + 2) + ".0", str(renglon + 3) + ".0"

            if i.side == "C":
                text1.tag_add(etiqueta, inicio, fin)
                if i.estado:
                    text1.tag_config(etiqueta, background="#76D7C4", foreground="black")
                else:
                    text1.tag_config(etiqueta, background="#F1948A", foreground="black")

            else:
                text2.tag_add(etiqueta, inicio, fin)
                if i.estado:
                    text2.tag_config(etiqueta, background="#76D7C4", foreground="black")
                else:
                    text2.tag_config(etiqueta, background="#F1948A", foreground="black")
                renglon += 1
    elif mi_contexto.environment != 1: #Entorno Real

        subyascente.price = iol_request.get_ggal(bearer_token)

        if parar.get:
            opc, vto = iol_request.get_options(bearer_token)

        print(len(opc), len(opciones))

        for i in range(len(opciones)):
            df.loc[opciones[i].ticker,"Prima"] = opc[i][1]

            df.loc[opciones[i].ticker, "B&Sch"] = calculo_blackScholes(subyascente.price, opciones[i].base, days_to_opex/365, opciones[i].side)
            df.loc[opciones[i].ticker, "Tenencia"] = df.loc[opciones[i].ticker, "Prima"] * df.loc[opciones[i].ticker, "Cantidad"] * 100

            if df.loc[opciones[i].ticker, "Cantidad"] != 0:
                try:
                    df.loc[opciones[i].ticker, "Rendimiento"] = round(
                        ((df.loc[opciones[i].ticker, "Prima"] - df.loc[opciones[i].ticker, "PP"]) / df.loc[opciones[i].ticker, "PP"]) * 100, 2)
                except ZeroDivisionError:
                    df.loc[opciones[i].ticker, "Rendimiento"] = 0
            else:
                df.loc[opciones[i].ticker, "PP"] = 0
                df.loc[opciones[i].ticker, "Rendimiento"] = 0

            # Colores a las opciones DUPLICADOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
            # VER opciones[i]
            etiqueta, inicio, fin = "et" + str(renglon) + opciones[i].side, str(renglon + 2) + ".0", str(renglon + 3) + ".0"

            if opciones[i].side == "C":
                text1.tag_add(etiqueta, inicio, fin)
                if opciones[i].estado:
                    text1.tag_config(etiqueta, background="#76D7C4", foreground="black")
                else:
                    text1.tag_config(etiqueta, background="#F1948A", foreground="black")
            else:
                text2.tag_add(etiqueta, inicio, fin)
                if opciones[i].estado:
                    text2.tag_config(etiqueta, background="#76D7C4", foreground="black")
                else:
                    text2.tag_config(etiqueta, background="#F1948A", foreground="black")
                renglon += 1







    mi_cartera.actualizar()

    text3["text"] = "EFECTIVO: ${} \n\nACT. VALORIZADOS: ${} \n\nDÍAS DESDE EL INICIO: {} \n\nCONTEXTO \n{}".format\
        (mi_cartera.efectivo,mi_cartera.opciones,mi_contexto.vto,mi_contexto)

    t2 = time.time()
    print("ACTUALIZO",(t2-t1))






    plt.grid()

def guardar_datos(file):
    """
    Guarda la posición en formato .txt
    """
    with open(file,"w",encoding="utf-8") as file:
        file.write(str(round(subyascente.price,2))+"\n")
        file.write(str(round(mi_cartera.efectivo,2))+"\n")

        for i in list(mi_cartera.tenencia.index):
            renglon = [i]+list(df.loc[i])
            print(renglon)
            for j in renglon:
                file.write(str(j) + " ")
            file.write("\n")
    print("GUARDADO!")

def clicked(value):
    """
    Informa por consola la compra/venta realizada
    """
    myLabel = Label(root,text=value)
    myLabel.place(x="15",y="570")
    print("CLICKED")

def pausa():
    """
    Pausa el tiempo e inmoviliza el subyascente. Sólo para prácticar y pensar la estrategia.
    Maneja el checkbutton.
    """
    if parar.get():
        parar.set(False)
    else:
        parar.set(True)

def loop():
    """
    Loop principal
    """
    i = 0
    t1 = time.time()
    while 1:
        if i % 4 == 0:
            actualizar()
            t2 = time.time()
            print(round((t2-t1),2)," seg. en dar una vuelta.")
            t1 = time.time()
        time.sleep(2)
        root.update()
        i += 1

def v_1():
    """
    Variables entorno práctica
    """
    global opciones,subyascente,mi_cartera

    # Creando Objetos
    subyascente = Ggal(125)
    mi_cartera = Cartera(100000)
    opciones = list()

    df.loc["GGAL"] = [subyascente.price, 0, 0, 0, 0, 0]

    for i in range(98, 189, 3):
        for j in ["C", "V"]:
            new = Opcion(i, j,"GGAL_"+j+"_"+str(i)+"_10",1)
            df.loc[new.ticker] = [new.prima, 0, 0, 0, 0, 0]
            opciones.append(new)


    # Cargando Tenencia

    with open(path, "r", encoding="utf-8") as file:
        try:
            subyascente.price = float(file.readline())

            mi_cartera.efectivo = float(file.readline())
            for i in file.readlines():
                i = i.split(" ")
                i.remove("\n")

                df.loc[i[0]] = [round(float(i[1]), 2), round(float(i[2]), 2), round(float(i[3]), 2),
                                round(float(i[4]), 2), int(i[5]), round(float(i[6]), 2)]
        except:
            pass

    print(df)
    print("HAY ",len(opciones)," OPCIONES")

    mi_cartera.actualizar_tenencia(df.loc[df["Cantidad"] != 0, ["Prima", "Cantidad"]])

def v_2():
    """
    Variables para entornos que necesitan autenticación con la API
    """
    global bearer_token, refresh_roken, mi_cartera, subyascente, opciones, days_to_opex
    print("CARGANDO COTIZACIONES")
    print()

    subyascente = Ggal()
    mi_cartera = Cartera(100000)

    bearer_token, refresh_token = iol_request.log_in()
    opc, vto = iol_request.get_options(bearer_token)
    days_to_opex = iol_request.get_opex(vto)

    print(opc)

    opciones = list()
    subyascente.price = iol_request.get_ggal(bearer_token)

    df.loc["GGAL"] = [subyascente.price, 0, 0, 0, 0, 0]

    for i in opc:
        new = Opcion(float(i[2]),i[0][3],i[0],float(i[1]))
        df.loc[new.ticker] = [new.prima, 0, 0, 0, 0, 0]
        opciones.append(new)

    print(df)

def variables():
    """
    Seteo variables generales
    """
    global x,df,ticks_x,ticks_y,opex

    df = pd.DataFrame(columns=["Serie", "Prima", "B&Sch", "Tenencia", "PP", "Cantidad", "Rendimiento"])
    df.set_index("Serie", inplace=True)
    x = [x for x in range(20, 300, 2)]
    ticks_x = ticker.FuncFormatter(lambda x, pos: "{:.0f}".format(x))
    ticks_y = ticker.FuncFormatter(lambda y, pos: "{:.2f}K".format(y / 1000))

    print(df)

    if mi_contexto.environment == 1:
        v_1()
    else:
        v_2()

def init_tkinter():
    """
    Creo Objetos en tkinter al iniciar el programa
    """
    global root, text1, text2, text3, text4, parar, figure, ticks_x, ticks_y, opcion

    # root
    root = tk.Tk()
    root.geometry("1750x600")
    root.title("Entorno de opciones GGAL")
    root.pack_propagate(False)
    #root.resizable(0, 0)  # No puede agrandarse, ni achicarse la ventana

    # Cuadros calls/puts
    text1 = tk.Text(root)
    text1.place(x=30, height=550, width=520)
    text2 = tk.Text(root)
    text2.place(x=600, height=550, width=520)
    text3 = tk.Label(root, text="")
    text3.place(x=1450, y=425)
    text4 = tk.Text(root)
    text4.place(x=1150, y=425, height=100, width=200)

    # RadioButton
    opcion = StringVar()
    opcion.set(df.index[0])

    y = 30
    for i in range(-1, len(df) - 1):
        if i == -1:
            Radiobutton(root, var=opcion, value="GGAL", command=lambda: clicked(opcion.get())).place(x="1370",y="475")
        else:
            if i % 2 == 0:
                Radiobutton(root, var=opcion, value=df.index[i + 1], command=lambda: clicked(opcion.get())).place(y=str(y))
            else:
                Radiobutton(root, var=opcion, value=df.index[i + 1], command=lambda: clicked(opcion.get())).place(x="570", y=str(y))
                y += 16

    # Botones
    button2 = tk.Button(root, text="Comprar", command=lambda: comprar(opcion.get()))
    button2.place(x="125", y="567")
    button3 = tk.Button(root, text="Vender", command=lambda: comprar(opcion.get(), -1))
    button3.place(x="200", y="567")
    button4 = tk.Button(root, text = "Guardar",command = lambda: guardar_datos(path))
    button4.place(x="1200", y="550")

    # CheckButton - parar tiempo
    parar = IntVar()
    check_parar = Checkbutton(root, variable="parar", command=pausa, text="Pausa", onvalue=True, offvalue=False,
                              width=5)
    parar.set(False)
    check_parar.place(x="275", y="567")

    # Grafico
    figure = plt.figure(figsize=(5, 4), dpi=100)
    ax1 = figure.add_subplot(111)
    ax1.plot(x, mi_cartera.suma)
    ax1.set_xlabel("Precio GGAL")
    ax1.set_xlabel("($) Ganancia")
    ax1.xaxis.set_major_formatter(ticks_x)
    ax1.yaxis.set_major_formatter(ticks_y)

    chart = FigureCanvasTkAgg(figure, root)
    chart.get_tk_widget().place(x=1150)

    figure.add_subplot(111).plot((subyascente.price, subyascente.price), (max(mi_cartera.suma), min(mi_cartera.suma)))

def main():
    """
    Defino variables principales
    """
    global mi_contexto

    environment = ask_enviroment()
    mi_contexto = Contexto(environment)

    print("MI CONTEXTO: ",mi_contexto.environment)

    variables()

    init_tkinter()


    loop()

def ask_enviroment():
    """
    Pregunta el entorno a abrir para setear la clase Contexto
    """
    print("Bienvenido!")
    print("Seleccione el entorno: ")
    print("( 1 ) Modo Práctica")
    print("( 2 ) Práctica - Precios Reales")
    print("( 3 ) Tiempo Real")

    opcion = 0
    while opcion not in [1,2,3]:
        opcion = int(input(""))

    return opcion





path = "C:/Users/Giuliano/Desktop/CODES/PYTHON/JSON/ENTORNO DE OPCIONES/posicion.txt"






main()
root.mainloop()

print("SE SALIOOOOOOOOOOO")








