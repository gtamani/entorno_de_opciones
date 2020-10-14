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


import time
import numpy as np
import random
import pandas as pd
import tkinter as tk
from tkinter import *
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.ticker as ticker
from hilo_request import Hilo_update
import finance


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


        try:
            df.loc["GGAL", "PP"] = round((df.loc["GGAL", "PP"] * (total - cant) + (
                    precio_conseguido * cant)) / total,2)
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
                self.efectivo -= cant * lote * df.loc[name,"Prima"]

    def actualizar_tenencia(self,tenencia):
        self.tenencia = tenencia

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
                    data = [data[3],opciones[df.index.get_loc(data)+1].base]

                total.append(data+list(self.tenencia.iloc[i]))
        self.suma = finance.graph(total,x)




    def actualizar(self):
        self.opciones = round(sum(list(df.loc[df["Cantidad"] != 0, "Tenencia"])),2)





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

        print(cant_comprada,df.loc[activo, "Cantidad"])

        if cant_comprada > 0 and df.loc[activo, "Cantidad"] > 0 or cant_comprada < 0 and df.loc[activo, "Cantidad"] <= 0:
            try:
                df.loc[activo, "PP"] = round((df.loc[activo, "PP"] * (df.loc[activo, "Cantidad"] - cant_comprada) + (df.loc[activo, "Prima"] *
                                        cant_comprada)) / total,2)
                if df.loc[activo, "Cantidad"] < 0:
                    df.loc[activo, "PP"] *= -1

                print("ENTRAAAAAA")
            except ZeroDivisionError:
                df.loc[activo, "PP"] = 0
                df.loc[activo, "Rendimiento"] = 0
        elif df.loc[activo, "Cantidad"] == 0:
            df.loc[activo, "PP"] = 0
            df.loc[activo, "Rendimiento"] = 0


        df.loc[activo, "Tenencia"] = df.loc[activo, "Prima"] * df.loc[activo, "Cantidad"] * 100 # Tenencia

    df.loc[activo, "Cantidad"] = int(df.loc[activo, "Cantidad"])


    mi_cartera.actualizar_tenencia(df.loc[df["Cantidad"] != 0,["Prima","Cantidad"]])

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
    y1, y2 = 30, 30

    actualizar_texto(True)

    if mi_contexto.environment == 1:
        if parar.get() == 0:
            #Paso del tiempo
            mi_contexto.vto += 1
            if mi_contexto.vto % 15 == 0:
                mi_contexto.sortear_contexto()

            #Actualizo GGAL
            subyascente.price += random.choice(mi_contexto.possibilities)
    else:
        subyascente.price = hilo.ggal

    df.loc["GGAL", "Cantidad"] = mi_cartera.acciones
    df.loc["GGAL", "Prima"] = subyascente.price
    df.loc["GGAL", "Tenencia"] = df.loc["GGAL", "Prima"] * mi_cartera.acciones
    if mi_cartera.acciones == 0:
        df.loc["GGAL", "PP"] = 0



    #Actualizo gráfico
    figure.clear()

    medio = min([(abs(x[z]-subyascente.price),z) for z in range(len(x))])[1]

    figure = plt.figure(figsize=(5, 4), dpi=100)
    ax1 = figure.add_subplot(111)
    ax1.plot(x[medio-ancho:medio+ancho], mi_cartera.suma[medio-ancho:medio+ancho])

    if any(mi_cartera.suma) is False:
        rango = [0,100]
    else:
        rango = mi_cartera.suma[medio-ancho:medio+ancho]

    ax2 = figure.add_subplot(111)
    try:
        ax2.plot((subyascente.price, subyascente.price), (max(rango), min(rango)))
    except:
        ax2.plot((subyascente.price, subyascente.price), (max(mi_cartera.suma), min(mi_cartera.suma)))
    ax3 = figure.add_subplot(111)
    ax3.plot(x,[0 for x in x],color = "black",linewidth= 1)

    ax1.set_xlabel("Precio GGAL")
    ax1.set_ylabel("($) Ganancia")
    ax1.xaxis.set_major_formatter(ticks_x)
    ax1.yaxis.set_major_formatter(ticks_y)
    plt.xlim(subyascente.price-(ancho*mostrar_ancho),subyascente.price+(ancho*mostrar_ancho))

    #SUBPLOT = 1 RENGLON, 1 COLUMNA, POSICIÓN 1
    chart = FigureCanvasTkAgg(figure, root)
    chart.get_tk_widget().place(x=1150)


    actualizar_texto()

    if mi_contexto.environment != 1:
        opc, vto = hilo.opciones, hilo.vencimiento_opc

    for i in range(len(opciones)):
        a = opciones[i]
        try:
            b = opc[i][1]
            actualizar_df(a,b)
        except:
            actualizar_df(a)

        if a.side == "C":
            botons_and_colors(a.ticker, y1, a.side, a.estado)
            y1 += 16
        else:
            botons_and_colors(a.ticker, y2, a.side, a.estado)
            y2 += 16











    mi_cartera.actualizar()

    text3["text"] = "EFECTIVO: ${} \n\nACT. VALORIZADOS: ${} \n\nDÍAS DESDE EL INICIO: {} \n\nCONTEXTO \n{}".format\
        (mi_cartera.efectivo,mi_cartera.opciones,mi_contexto.vto,mi_contexto)

    t2 = time.time()
    print("ACTUALIZO",(t2-t1))

    plt.grid()




def botons_and_colors(ticker,y,side,itm):
    """
    Maneja los Botones y los colores
    """
    renglon = ((y - 30) / 16) -1
    color = "#76D7C4" if itm else "#F1948A"
    inicio, fin, etiqueta =  str(renglon+4), str(renglon+5),"et" + str(renglon) + side

    if side == "C":
        x = 0
        text1.tag_add(etiqueta, inicio, fin)
        text1.tag_config(etiqueta, background=color, foreground="black")
    else:
        x = 570
        text2.tag_add(etiqueta, inicio, fin)
        text2.tag_config(etiqueta, background=color, foreground="black")

    """
    if i == -1:
        Radiobutton(root, var=opcion, value="GGAL", command=lambda: clicked(opcion.get())).place(x="1370", y="475")
    """
    if lap == 0:
        Radiobutton(root, var=opcion, value=ticker, command=lambda: clicked(opcion.get())).place(x=x, y=y)

def actualizar_df(a,b = 0):
    """
    Actualiza DataFrame ante cambios en los precios de las opciones, accion
    a = opción
    """

    if mi_contexto.environment == 1:
        a.restar_día(random.choice([True, False, False, False, False]))
        a.actualizar_prima()
        if a.arbitrado:
            df.loc[a.ticker, "Prima"] = round(a.prima, 2)
    else:
        df.loc[a.ticker, "Prima"] = b

    df.loc[a.ticker, "B&Sch"] = finance.calculo_blackScholes(subyascente.price, a.base, 68 / 360, a.side)
    df.loc[a.ticker, "Tenencia"] = df.loc[a.ticker, "Prima"] * df.loc[a.ticker, "Cantidad"] * 100

    if df.loc[a.ticker, "Cantidad"] != 0:
        try:
            df.loc[a.ticker, "Cantidad"] = int(df.loc[a.ticker, "Cantidad"])
            df.loc[a.ticker, "Rendimiento"] = round(
                ((df.loc[a.ticker, "Prima"] - abs(df.loc[a.ticker, "PP"])) / df.loc[a.ticker, "PP"]) * 100, 2)
        except ZeroDivisionError:
            df.loc[a.ticker, "Rendimiento"] = 0
    else:
        df.loc[a.ticker, "PP"] = 0
        df.loc[a.ticker, "Rendimiento"] = 0

def actualizar_texto(out=False):
    """
    Actualiza el gráfico ante cambios en los datos
    """
    if out:
        text1.delete("1.0", "end")
        text2.delete("1.0", "end")
        text4.delete("1.0", "end")
    else:
        if mi_contexto.environment == 1:
            text1.insert(tk.INSERT, df.iloc[[x for x in range(1, len(df) - 1, 2)]].to_string())  # Calls
            text2.insert(tk.INSERT, df.iloc[[x for x in range(2, len(df), 2)]].to_string())  # Puts
        else:
            text1.insert(tk.INSERT,
                         df.iloc[[x for x in range(1, len(df)) if df.index[x][3] == "C"]].to_string())  # Calls
            text2.insert(tk.INSERT,
                         df.iloc[[x for x in range(1, len(df)) if df.index[x][3] == "V"]].to_string())  # Puts

        text4.insert(tk.INSERT, "GGAL: \n" + df.loc["GGAL"].to_string())  # GGAL

def guardar_datos(file):
    """
    Guarda la posición en formato .txt
    """
    with open(file,"w",encoding="utf-8") as file:
        if mi_contexto.environment == 1:
            file.write(str(round(subyascente.price,2))+"\n")
        file.write(str(round(mi_cartera.efectivo,2))+"\n")

        for i in list(mi_cartera.tenencia.index):
            renglon = [i]+list(df.loc[i])
            print(renglon)
            for j in renglon:
                file.write(str(j) + " ")
            file.write("\n")
    print("GUARDADO!")

def cargar_datos():

    with open(path, "r", encoding="utf-8") as file:
        try:
            if mi_contexto.environment == 1:
                subyascente.price = float(file.readline())

            mi_cartera.efectivo = float(file.readline())
            for i in file.readlines():
                i = i.split(" ")
                i.remove("\n")
                print("CANT: ",int(i[5]))

                df.loc[i[0]] = [round(float(i[1]), 2), round(float(i[2]), 2), round(float(i[3]), 2),
                                round(float(i[4]), 2), int(i[5]), round(float(i[6]), 2)]
        except:
            print("No pudo cargarse.")
            pass

    mi_cartera.actualizar_tenencia(df.loc[df["Cantidad"] != 0, ["Prima", "Cantidad"]])

def ancho_tabla(num):
    """
    Controla la botonera del gráfico
    """
    global ancho, mostrar_ancho

    if ancho + num in [x*5 for x in range(1,11)]:
        ancho += num
        mostrar_ancho = 1.8
    elif ancho + (num//5) in [x for x in range(2,5)] or ancho == 4:
        ancho += (num//5)
        mostrar_ancho = 1

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
    global lap
    lap = 0
    t1 = time.time()
    while 1:
        print("LAP",lap)
        if lap % 4 == 0:
            actualizar()
            t2 = time.time()
            print(round((t2-t1),2)," seg. en dar una vuelta.")
            t1 = time.time()
        time.sleep(0.5)
        root.update()
        lap += 1

def v_1():
    """
    Variables entorno práctica
    """
    global opciones,subyascente,mi_cartera

    # Creando Objetos
    subyascente = Ggal(125)
    mi_cartera = Cartera(100000)

    df.loc["GGAL"] = [subyascente.price, 0, 0, 0, 0, 0]

    for i in range(98, 189, 3):
        for j in ["C", "V"]:
            new = Opcion(i, j,"GGAL_"+j+"_"+str(i)+"_10",1)
            df.loc[new.ticker] = [new.prima, 0, 0, 0, 0, 0]
            opciones.append(new)

    cargar_datos()

def v_2():
    """
    Variables para entornos que necesitan autenticación con la API
    """
    global opciones, bearer_token, refresh_roken, mi_cartera, subyascente, days_to_opex, hilo

    subyascente = Ggal()
    mi_cartera = Cartera(100000)

    hilo = Hilo_update("update")
    hilo.start()

    time.sleep(5)
    input("Presione Enter cuando se actualice ")

    opc, vto = hilo.opciones, hilo.vencimiento_opc
    days_to_opex = hilo.days_to_opex

    subyascente.price = hilo.ggal

    df.loc["GGAL"] = [subyascente.price, 0, 0, 0, 0, 0]

    for i in opc:
        new = Opcion(float(i[2]),i[0][3],i[0],float(i[1]))
        df.loc[new.ticker] = [new.prima, 0, 0, 0, 0, 0]
        opciones.append(new)

    cargar_datos()

def variables():
    """
    Seteo variables generales
    """
    global x,ticks_x,ticks_y,df,opciones,ancho,mostrar_ancho

    df = pd.DataFrame(columns=["Serie", "Prima", "B&Sch", "Tenencia", "PP", "Cantidad", "Rendimiento"])
    df.set_index("Serie", inplace=True)
    x = [x for x in range(20, 300, 2)]
    ticks_x = ticker.FuncFormatter(lambda x, pos: "{:.0f}".format(x))
    ticks_y = ticker.FuncFormatter(lambda y, pos: "{:.2f}K".format(y / 1000))
    opciones = list()
    ancho, mostrar_ancho = 20,1.8

    if mi_contexto.environment == 1:
        v_1()
    else:
        v_2()

def init_tkinter():
    """
    Creo Objetos en tkinter al iniciar el programa
    """
    global root, text1, text2, text3, text4, parar, figure, ticks_x, ticks_y,opcion

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

    print(df)
    #ubicar_radiobuttons()

    # Botones

    button2 = tk.Button(root, text="Comprar", command=lambda: comprar(opcion.get()))
    button2.place(x="125", y="567")
    button3 = tk.Button(root, text="Vender", command=lambda: comprar(opcion.get(), -1))
    button3.place(x="200", y="567")
    button4 = tk.Button(root, text = "Guardar",command = lambda: guardar_datos(path))
    button4.place(x="1200", y="550")
    button5 = tk.Button(root, text="{:3}".format("+"),command= lambda: ancho_tabla(-5))
    button5.place(x="1670", y="100")
    button6 = tk.Button(root, text=" {:3}".format("-"), command=lambda: ancho_tabla(+5))
    button6.place(x="1670", y="130")



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

def ubicar_radiobuttons():
    global opcion

    opcion = StringVar()
    opcion.set(df.index[0])

    y1, y2 = 30, 30
    for i in range(-1, len(df) - 1):
        if i == -1:
            Radiobutton(root, var=opcion, value="GGAL", command=lambda: clicked(opcion.get())).place(x="1370", y="475")
        else:
            if i % 2 == 0:
                Radiobutton(root, var=opcion, value=df.index[i + 1], command=lambda: clicked(opcion.get())).place(
                    y=str(y1))
                y1 += 16
            else:
                Radiobutton(root, var=opcion, value=df.index[i + 1], command=lambda: clicked(opcion.get())).place(
                    x="570", y=str(y2))
                y2 += 16

def main():
    """
    Defino variables principales
    """
    global mi_contexto,path

    environment = ask_enviroment()
    mi_contexto = Contexto(environment)
    path = "C:/Users/Giuliano/Desktop/CODES/PYTHON/JSON/ENTORNO DE OPCIONES/env" + str(mi_contexto.environment) + "_posicion.txt"

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












main()
root.mainloop()








