import tkinter as tk
import tkinter.ttk
from tkinter import messagebox
import threading
from concurrent.futures import ThreadPoolExecutor
import os,time
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
        self.progressbar = tk.ttk.Progressbar(self.root,orient= tk.HORIZONTAL,length=200,value=0)
    

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
        df.loc["GFGC120OCT"] = ["C",120,2.5,5]
        df.loc["GFGV120OCT"] = ["V",120,5,5]
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
        t0 = time.time()
        self.user = user
        print(self.user)
        self.root = tk.Tk()
        self.root.geometry("2200x600")
        self.root.title("Entorno de opciones GGAL")
        self.root.pack_propagate(False)

        # Menu
        self.menu_bar = tk.Menu(self.root)
        self.menu_bar.add_separator()
        self.menu_bar.add_command(label="Cargar Datos",command=lambda:print("Loaded!"))
        self.menu_bar.add_separator()
        self.menu_bar.add_command(label="Guardar",command=lambda:print("Saved!"))
        self.menu_bar.add_separator()
        self.menu_bar.add_command(label="Configuraciones",command=lambda:threading.Thread(target=Settings()).start())
        self.menu_bar.add_separator()
        self.menu_bar.add_command(label="Cambiar de usuario",command=lambda:print("Changed!"))
        self.menu_bar.add_separator()
        self.menu_bar.add_command(label="Salir",command=self.on_closing)
        #self.menu.add_cascade(label="File",menu=self.menu_bar)
        self.root.config(menu=self.menu_bar)

        # Main texts
        self.text1 = tk.Text(self.root)
        self.text1.place(x=30, height=550, width=540)
        self.text2 = tk.Text(self.root)
        self.text2.place(x=600, height=550, width=540)
        self.text4 = tk.Text(self.root)
        #self.text4.place(x=1150, y=425, height=90, width=310) #
        self.text6 = tk.Text(self.root)
        #self.text6.place(x=1470, y=425, height=150, width=200) #

        #Entry
        self.entry_var = tk.StringVar()
        self.entry = tk.Entry(textvariable=self.entry_var,justify=tk.CENTER)
        self.entry.place(x=240,y=567,width=50)

        #Radiobuttons
        self.opcion = tk.StringVar()
        self.opcion.set("")
        self.cant_operar = tk.IntVar()
        #self.opcion.set(df.index[0])
        self.cant_operar.set(0)
        self.radiobutton = tk.Radiobutton(self.root, var=self.opcion, value="GGAL")
        #self.radiobutton["command"] = lambda:clicked(opcion.get())
        self.radiobutton.place(x=1700, y=482)

        #Labels
        self.text3 = tk.Label(self.root, text="")
        self.text3.place(x=1700, y=425)
        self.text5 = tk.Label(self.root)
        self.text5.place(x=300, y=567)

        #Buttons
        self.button1 = tk.Button(self.root, text="Simular!")
        #self.button1["command"] = lambda: simular(opcion.get(),cant_operar.get())
        #self.button1.place(x="125", y="567")
        #self.button2 = tk.Button(self.root, text="(+)")
        #self.button2["command"] = lambda: lambda: clicked(opcion.get(),1))
        #self.button2.place(x="200", y="567")
        #self.button3 = tk.Button(self.root, text="(-)")
        #self.button3["command"] = lambda: clicked(opcion.get(),-1)
        #self.button3.place(x="250", y="567")
        self.button4 = tk.Button(self.root, text = "Guardar")
        #self.button4["command"] = lambda: guardar_datos(path)
        #self.button4.place(x="1200", y="550")
        self.button5 = tk.Button(self.root, text="{:3}".format("+"))
        #self.button5["command"] = lambda: ancho_tabla(-5)
        self.button5.place(x="1770", y="500")
        self.button6 = tk.Button(self.root, text=" {:3}".format("-"))
        #self.button5["command"] = lambda: ancho_tabla(+5)
        self.button6.place(x="1770", y="530")
        self.button7 = tk.Button(self.root,text="Actualizar!")
        self.button7["command"] = lambda: threading.Thread(target=self.get_options).start()
        #self.button7.place(x="700",y="567")
        self.radiobuttons_shown = False
        
        

        # Grafico
        self.fig, self.ax = plt.subplots(1,1,figsize=(7, 4), dpi=100)


        #ax[0].plot(x, mi_cartera.suma)
        #ax[1].plot(hilo.coord[0],hilo.coord[1])
        x,y,y2 = get_curves_sumed(get_portfolio("gtamani"))
        self.ax.plot(x,y)
        self.ax.plot(x,y2)

        self.ax.set_xlabel("Precio GGAL")
        self.ax.set_xlabel("($) Ganancia")
        self.ax.grid()
        self.ax.set_xlim(100,140)
        
        
        """
        self.ticks_x = ticker.FuncFormatter(lambda x, pos: "{:.0f}".format(x))
        self.ticks_y = ticker.FuncFormatter(lambda y, pos: "{:.2f}K".format(y / 1000))
        self.ax[0].xaxis.set_major_formatter(ticks_x)
        self.ax[0].yaxis.set_major_formatter(ticks_y)
        """
        self.chart = FigureCanvasTkAgg(self.fig, self.root)
        self.chart.get_tk_widget().place(x=1150)

        #self.plot_options()

        #EVENTOS
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
        #OPCIONES DISPONIBLES
        self.options_list = []
        self.stock_price = 0
        self.df = pd.DataFrame(columns=["Serie", "Prima", "B&Sch", "Tenencia", "PP", "Cantidad", "Rendimiento"])
        self.df.set_index("Serie", inplace=True)
        self.get_options()

        #Hilos y cierre del loop

        self.root.after(1,lambda: threading.Thread(target=self.update).start())
        t1 = time.time()
        print(t1-t0)
        self.root.mainloop()


    def plot_options(self):
        y1, y2 = 30, 30
        for i in self.options_list:
                print(i.ticker)
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

        self.stock_price = get_equity("ggal")
        self.options_list = []
        
        for x in get_options()[0]:
            self.options_list.append(Opcion(x[0],x[1],x[2],x[3],self.stock_price))
            #["Serie", "Prima", "B&Sch", "Tenencia", "PP", "Cantidad", "Rendimiento"]
            self.df.loc[x[2]] = [x[3], 0, 0, 0, 0, 0]

        self.text1.delete("1.0","end")
        self.text2.delete("1.0","end")
        self.text1.insert(tk.INSERT,self.df.iloc[[x for x in range(0, len(self.df)) if self.df.index[x][3] == "C"]].to_string())  # Calls
        self.text2.insert(tk.INSERT,self.df.iloc[[x for x in range(1, len(self.df)) if self.df.index[x][3] == "V"]].to_string())  # Puts

        print(self.df)
        print(self.stock_price)
        self.plot_options()

    def update(self):
        a = str(self.opcion.get())
        try:
            cant = int(self.entry_var.get())
            sell_or_buy = "Comprar" if cant > 0 else "Vender"
            text = sell_or_buy+ " " + str(abs(int(self.entry_var.get())))
            text += " lotes "+ a
            text += " a $" + str(float(self.df.loc[a,"Prima"]) * abs(cant)*100)
        except:
            text = "<----   Seleccione una cantidad de " + a
        self.text5["text"] = text+"!"
        
        #print(self.df)

        self.root.after(5,self.update)

    def on_closing(self):
        response = tk.messagebox.askyesnocancel(title="Salir",message="Quiere guardar los cambios?")
        print(response)
        
        if response is not None:
            if response:
                print("Guardado!")
            self.root.destroy()
        

class Settings:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("500x330")
        self.root.title("Settings")
        self.root.pack_propagate(False)

        #1. Actualizacion automatica o manual
        tk.Label(self.root,text="Actualización manual").place(x=45,y=30)
        self.label_value4 = tk.IntVar()
        tk.Checkbutton(self.root,variable= self.label_value4,onvalue=True,offvalue=False).place(x=15,y=30)
        tk.Label(self.root,text="Actualización automatica").place(x=45,y=60)
        self.label_value5 = tk.IntVar()
        tk.Checkbutton(self.root,variable= self.label_value5,onvalue=True,offvalue=False).place(x=15,y=60)
        tk.Label(self.root,text="Cada"+" "*23+"segundos").place(x=210,y=60)
        self.spinbox = tk.ttk.Spinbox(self.root,values=[5,7,10,15,20,30,60],format="%3.0f",width=5)
        self.spinbox.set(10)
        self.spinbox.place(x=250,y=62)
        tk.ttk.Separator(self.root,orient = tk.HORIZONTAL).place(y=100,relx=0.05,relwidth=0.9)

        #2. Mostrar opciones de GGAL
        tk.Label(self.root,text="Mostrar opciones de").place(x=45,y=120)
        self.combobox = tk.ttk.Combobox(self.root,justify="center",values=("GGAL - Galicia","ALUA - Aluar","COME - Comercial del Plata","PAMP Pampa Energía","YPFD - YPF"),state="enabled",width=25)
        self.combobox.set("GGAL - Galicia")
        self.combobox.place(x=180,y=120)
        tk.Label(self.root,text="Mostrar Subyascente").place(x=45,y=150)
        self.label_value = tk.IntVar()
        tk.Checkbutton(self.root,variable= self.label_value,onvalue=True,offvalue=False).place(x=15,y=150)
        tk.ttk.Separator(self.root,orient = tk.HORIZONTAL).place(y=190,relx=0.05,relwidth=0.9)

        #3. Grafico
        #3.1 Agregar resultado finish
        tk.Label(self.root,text="Agregar Resultado Finish").place(x=45,y=210)
        self.label_value1 = tk.IntVar()
        tk.Checkbutton(self.root,variable= self.label_value1,onvalue=True,offvalue=False).place(x=15,y=210)
        #3.2 Mostrar esperado
        tk.Label(self.root,text="Mostrar influencia de la posición a armar sobre mi tenencia").place(x=45,y=240)
        self.label_value2 = tk.IntVar()
        tk.Checkbutton(self.root,variable= self.label_value2,onvalue=True,offvalue=False).place(x=15,y=240)
        #3.3 Agregar lineas de rango
        tk.Label(self.root,text="Agregar líneas de rango").place(x=45,y=270)
        self.label_value3 = tk.IntVar()
        tk.Checkbutton(self.root,variable= self.label_value3,onvalue=True,offvalue=False).place(x=15,y=270)

        tk.Button(self.root,text="Guardar y salir",command=lambda:self.root.destroy()).place(relx=0.8,y=285)

        """
        self.spinbox= tk.ttk.Spinbox(self.root,from_=5,to=40,increment=1,format="%3.0f",width=5).place(x=10,y=10)
        self.combobox = tk.ttk.Combobox(self.root,justify="center",values=("Automático","Manual"),state="disabled").place(x=10,y=40)
        self.progressbar = tk.ttk.Progressbar(self.root,orient= tk.HORIZONTAL,length=200,value=0)
        self.progressbar.place(x=10,y=70)
        self.pogressbar_button = tk.Button(self.root,text="More power!" ,command= lambda:self.progressbar.step(10)).place(x=250,y=70)
        """
        self.root.mainloop()


class Opcion:

    def __init__(self,base,side,ticker,price,subyascente):
        self.base = float(base)
        self.side = side
        self.price = float(price)
        self.ticker = ticker
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
    
    login = Login()

    def check():
        app = None
        while app is None:
            if login.current_user:
                print("a")
                app = App(login.current_user)

    threading.Thread(target=check).start()
    



"""
import tkinter as tk


class interfaz_dinamica:


    def __init__(self):

        # Se crea la ventana
        self.ventana = tk.Tk() 


        # Se crean los botones
        self.b1 = tk.Button(self.ventana, text='opcion 1', command=self.text1).grid(row=3, column=1, sticky=tk.W, pady=4)
        self.b2 = tk.Button(self.ventana, text='opcion 2', command=self.text2).grid(row=3, column=2, sticky=tk.W, pady=4)


        # Se crea la etiqueta pero no se le asigna ningun valor
        self.etiqueta = tk.Label(self.ventana)
        # Valor de la etiqueta 
        self.valor = "valor por defecto"

        # se invoca la función dinamica la cual será como un bucle que se ejecuta una y otra vez
        self.funcion_dinamica()
        self.ventana.mainloop()


    # funciones de los botones la cual cambia el contenido de valor
    def text1 (self):
        self.valor = "opcion1"

    def text2 (self):
        self.valor = "opcion2"
        


    def funcion_dinamica(self):


        #se configura la etiqueta con el texto que hay en valor
        self.etiqueta.configure(text = self.valor)
        self.etiqueta.grid(row=1, column=1, sticky=tk.W,pady=4)

        # se repite nuevamente la funcion dinamica, como si fuera un bucle infinito
        self.etiqueta.after(1,self.funcion_dinamica)



if __name__ == "__main__":
    GUI = interfaz_dinamica()
"""