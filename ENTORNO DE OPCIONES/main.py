import tkinter as tk
import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from API_data import *
from get_graph import *


class Login:

    def __init__(self):

        self.root = tk.Tk()
        self.root.geometry("600x150")
        self.root.title("Log In")
        self.text, self.text2 = tk.Label(),tk.Label(text = "Cargar mis opciones al ingresar.")
        self.show_excel = tk.IntVar()
        self.checkbutton = tk.Checkbutton(variable=self.show_excel,onvalue=True,offvalue=False)
        self.text.place(x=30,width=540,height=100)
        self.listbox = tk.Listbox(exportselection=0,selectmode=tk.SINGLE)
        self.button_no = tk.Button(text="No",command= self.show_users)
        self.button_yes = tk.Button(text="Sí",command= self.save_and_exit)
        self.button = tk.Button(text="Go!",command=lambda: self.create_user(self.entry_var))
        self.entry_var = tk.StringVar()
        self.entry = tk.Entry(textvariable= self.entry_var)

        self.current_user =  None
        self.from_entry = False
        self.new_user_created = False

        self.button_yes.place(x=200,y=70,width=100,height=20)
        self.button_no.place(x=310,y=70,width=100,height=20)

        
        with open(os.getcwd()+os.sep+"data/users.txt","r",encoding="utf-8") as handler:
            self.users = [x.strip('\n') for x in handler.readlines()]
        self.listbox.insert(0,*self.users)

        if self.users == []:
            self.new_user()
        else:
            self.text["text"] = "¿Eres "+self.users[0]+"?"

            self.text2.place(x=230,y=100)
            self.checkbutton.place(x=200,y=100)

        self.root.mainloop()

    def create_user(self,user):
        df = pd.DataFrame(columns=["Opcion","Side","Strike","Price","Cant"])
        df.set_index("Opcion",inplace=True)
        df.loc["GFGC100OCT"] = ["C",100,5,10]
        df.loc["GFGC120OCT"] = ["C",120,1,3]
        df.loc["GFGV80OCT"] = ["V",80,1,-5]
        df.to_excel("./data/boards/"+user.get()+"_board.xlsx")
        with open(os.getcwd()+os.sep+"data/users.txt","a",encoding="utf-8") as handler:
            text = user.get()
            if len(self.users) != 0:
                text = "\n"+text
            handler.write(text)
        self.users.insert(0,user.get())
        self.listbox.insert(0,self.users[0])
        self.show_users()

    def save_and_exit(self):
        if self.from_entry:
            self.current_user = self.users[self.listbox.curselection()[0]]
        else:
            self.current_user = self.users[0]

        if self.show_excel.get():
            os.chdir(os.getcwd()+os.sep+"data"+os.sep+"boards")
            os.system(self.current_user+"_board.xlsx")
        self.root.destroy()
        App(self.current_user)   
    
    def new_user(self):
        self.listbox.place_forget()
        self.text2.place_forget()
        self.checkbutton.place_forget()
        self.entry.place(x=30,y=70,width=410,height=20)
        self.button.place(x=450,y=70,width=120,height=20)
        self.text["text"] = "Nuevo por aquí? Define un usuario"
        self.new_user_created = True

    def show_users(self):
        if len(self.users) == 1 and self.new_user_created is False:
            self.new_user()
        else:
            self.from_entry = True
            self.entry.place_forget()
            self.button.place_forget()
            self.listbox.place(x=60,y=15,height=120)
            self.listbox.select_set(0)
            self.text["text"] = "Seleccione un usuario >>"
            self.button_yes["text"] = "Iniciar"
            self.button_yes["command"] = self.save_and_exit
            self.button_no["text"] = "No estoy en la lista"
            self.button_no["command"] = self.new_user
            self.text2.place(x=230,y=100)
            self.checkbutton.place(x=200,y=100)
            
class App:

    def __init__(self,user):
        self.user = user
        print(self.user)
        self.root = tk.Tk()
        self.root.geometry("2200x600")
        self.root.title("Entorno de opciones GGAL")
        self.root.pack_propagate(False)

        # Main texts
        self.text1 = tk.Text(self.root)
        self.text1.place(x=30, height=550, width=540)
        self.text2 = tk.Text(self.root)
        self.text2.place(x=600, height=550, width=540)
        self.text4 = tk.Text(self.root)
        self.text4.place(x=1150, y=425, height=90, width=310) #
        self.text6 = tk.Text(self.root)
        self.text6.place(x=1470, y=425, height=150, width=200) #

        #Labels
        self.text3 = tk.Label(self.root, text="")
        self.text3.place(x=1700, y=425)
        self.text5 = tk.Label(self.root, text="Selecciona un activo!")
        self.text5.place(x=300, y=567)

        #Radiobuttons
        self.opcion = tk.StringVar()
        self.cant_operar = tk.IntVar()
        #self.opcion.set(df.index[0])
        self.cant_operar.set(0)
        self.radiobutton = tk.Radiobutton(self.root, var=self.opcion, value="GGAL")
        #self.radiobutton["command"] = lambda:clicked(opcion.get())
        self.radiobutton.place(x=1700, y=482)

        #Buttons
        self.button1 = tk.Button(self.root, text="Simular!")
        #self.button1["command"] = lambda: simular(opcion.get(),cant_operar.get())
        self.button1.place(x="125", y="567")
        self.button2 = tk.Button(self.root, text="(+)")
        #self.button2["command"] = lambda: lambda: clicked(opcion.get(),1))
        self.button2.place(x="200", y="567")
        self.button3 = tk.Button(self.root, text="(-)")
        #self.button3["command"] = lambda: clicked(opcion.get(),-1)
        self.button3.place(x="250", y="567")
        self.button4 = tk.Button(self.root, text = "Guardar")
        #self.button4["command"] = lambda: guardar_datos(path)
        self.button4.place(x="1200", y="550")
        self.button5 = tk.Button(self.root, text="{:3}".format("+"))
        #self.button5["command"] = lambda: ancho_tabla(-5)
        self.button5.place(x="1770", y="500")
        self.button6 = tk.Button(self.root, text=" {:3}".format("-"))
        #self.button5["command"] = lambda: ancho_tabla(+5)
        self.button6.place(x="1770", y="530")
        self.button7 = tk.Button(self.root,text="Actualizar!")
        self.button7["command"] = self.get_options
        self.button7.place(x="700",y="567")
        self.radiobuttons_shown = False
        

        # Grafico
        self.figure = plt.figure(figsize=(5, 4), dpi=100)

        self.ax1 = self.figure.add_subplot(211)
        self.ax7 = self.figure.add_subplot(212)

        #ax1.plot(x, mi_cartera.suma)
        #ax7.plot(hilo.coord[0],hilo.coord[1])
        x,y = get_finish_curve_sumed(get_portfolio("gtamani"))
        self.ax1.plot(x,y)
        self.ax7.plot()

        self.ax1.set_xlabel("Precio GGAL")
        self.ax1.set_xlabel("($) Ganancia")
        """
        self.ticks_x = ticker.FuncFormatter(lambda x, pos: "{:.0f}".format(x))
        self.ticks_y = ticker.FuncFormatter(lambda y, pos: "{:.2f}K".format(y / 1000))
        self.ax1.xaxis.set_major_formatter(ticks_x)
        self.ax1.yaxis.set_major_formatter(ticks_y)
        """
        self.chart = FigureCanvasTkAgg(self.figure, self.root)
        self.chart.get_tk_widget().place(x=1150)

        #self.plot_options()


        #OPCIONES DISPONIBLES
        self.options_list = []
        self.stock_price = 0
        self.df = pd.DataFrame(columns=["Serie", "Prima", "B&Sch", "Tenencia", "PP", "Cantidad", "Rendimiento"])
        self.df.set_index("Serie", inplace=True)
        self.get_options()

    def plot_options(self):
        y1, y2 = 30, 30
        for i in self.options_list:
                if i.side == "C":
                    self.botons_and_colors(i.ticker, y1, i.side, i.estado)
                    y1 += 16
                else:
                    self.botons_and_colors(i.ticker, y2, i.side, i.estado)
                    y2 += 16
        
        self.radiobuttons_shown = True
        self.opcion.set(self.options_list[0].ticker)
        if not self.radiobuttons_shown:
            self.text4.insert(tk.INSERT,"GGAL : $"+str(self.stock_price))


    def botons_and_colors(self,ticker,y,side,itm):
        """
        Maneja los Botones y los colores
        """
        renglon = ((y - 30) / 16) -1
        colors = {"itm":"#76D7C4","atm":"#FFE4B5","otm":"#F1948A"}

        inicio, fin, etiqueta =  str(renglon+4), str(renglon+5),"et" + str(renglon) + side

        if side == "C":
            x = 0
            self.text1.tag_add(etiqueta, inicio, fin)
            self.text1.tag_config(etiqueta, background=colors[itm], foreground="black")
        else:
            x = 570
            self.text2.tag_add(etiqueta, inicio, fin)
            self.text2.tag_config(etiqueta, background=colors[itm], foreground="black")

        if not self.radiobuttons_shown:
            self.rb = tk.Radiobutton(self.root, var=self.opcion, value=ticker) #"""var=opcion,"""
            self.rb.place(x=x, y=y)
            self.rb["command"] = lambda: print(self.opcion.get())
            

    def get_options(self):
        self.text1.delete("1.0","end")
        self.text2.delete("1.0","end")

        self.stock_price = get_equity("ggal")
        for x in get_options()[0]:
            self.options_list.append(Opcion(x[0],x[1],x[2],x[3],self.stock_price))
            #["Serie", "Prima", "B&Sch", "Tenencia", "PP", "Cantidad", "Rendimiento"]
            self.df.loc[x[2]] = [x[3], 0, 0, 0, 0, 0]

        self.text1.insert(tk.INSERT,self.df.iloc[[x for x in range(1, len(self.df)) if self.df.index[x][3] == "C"]].to_string())  # Calls
        self.text2.insert(tk.INSERT,self.df.iloc[[x for x in range(1, len(self.df)) if self.df.index[x][3] == "V"]].to_string())  # Puts

        print(self.stock_price)
        self.plot_options()

class Opcion:

    def __init__(self,base,side,ticker,price,subyascente):
        self.base = float(base)
        self.side = side
        self.price = float(price)
        self.ticker = "GGAL_" + self.side + "_" + str(self.base) + "_10"
        self.sigma = 0
        self.subyascente = subyascente

        if self.side == "C":
            if self.subyascente >= self.base + 1.6:
                self.estado = "itm"
            elif self.subyascente <= self.base - 1.6:
                self.estado = "otm"
            else:
                self.estado = "atm"
        else:
            if self.subyascente <= self.base - 1.6:
                self.estado = "itm"
            elif self.subyascente >= self.base + 1.6:
                self.estado = "otm"
            else:
                self.estado = "atm"

    def __str__(self):
        return self.ticker

if __name__ == "__main__":
    Login()
