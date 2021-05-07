import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time, threading
from datetime import datetime

from API_data import *
from get_graph import *

from Settings import Settings
from Login import Login
from pg_database import Postgres_database


class App:

    def __init__(self,user):
        t0 = time.time()
        self.user = user
        self.root = tk.Tk()
        self.database = Postgres_database()
        self.settings= False
        self.closed = False
        self.all_stocks = {"ggal":"Galicia","alua":"Aluar", "come":"Comercial del Plata","pamp":"Pampa Energia","ypfd":"YPF"}
        
        
        self.load_settings()
        self.current_stock = self.equity.get()[:4].lower()

        self.root.geometry("2200x600")
        self.root.title("Entorno de opciones "+self.current_stock.upper())
        self.root.pack_propagate(False)


        

        # Menu
        self.menu_bar = tk.Menu(self.root)
        self.menu_bar.add_separator()
        self.menu_bar.add_command(label="Cargar Datos",command=self.load_excel)

        

        self.menu_bar.add_separator()
        self.menu_bar.add_command(label="Guardar",command=lambda:threading.Thread(target=self.save_changes).start())
        self.menu_bar.add_separator()
        self.menu_bar.add_command(label="Configuraciones",command=lambda:threading.Thread(target=self.init_settings).start())
        self.menu_bar.add_separator()
        self.menu_bar.add_command(label="Cambiar de usuario",command=self.change_user)
        self.menu_bar.add_separator()
        self.menu_bar.add_command(label="Salir",command=self.on_closing)
        #self.menu.add_cascade(label="File",menu=self.menu_bar)
        self.root.config(menu=self.menu_bar)

        # Main texts
        self.text1 = tk.Text(self.root)
        self.text1.place(x=30, height=550, width=540)
        self.text2 = tk.Text(self.root)
        self.text2.place(x=600, height=550, width=540)
        self.text4 = tk.Label(self.root,font=("Verdana",16))
        self.text4.place(x=1150, y=400, height=90, width=310) #
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
        #self.radiobutton.place(x=1700, y=482)

        #Labels
        self.text3 = tk.Label(self.root, text="")
        self.text3.place(x=1700, y=425)
        self.text5 = tk.Label(self.root)
        self.text5.place(x=300, y=567)

        #Buttons
        self.button1 = tk.Button(self.root, text="Operar!",command=self.buy)
        self.button1.place(x="125", y="567")
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
        self.button7.place(x="700",y="567")
        self.radiobuttons_shown = False

        if self.is_auto.get():
            self.button7["state"] = "disabled"
        
        

        # Grafico
        self.fig, self.ax = plt.subplots(1,1,figsize=(7, 4), dpi=100)
        x,y,y2 = get_curves_sumed(get_portfolio("gtamani"))
        self.ax.plot(x,y)
        self.ax.plot(x,y2)

        self.ax.set_xlabel("Precio "+self.current_stock.upper())
        self.ax.set_xlabel("($) Ganancia")
        self.ax.grid()
        self.ax.set_xlim(100,140)
        
        self.chart = FigureCanvasTkAgg(self.fig, self.root)
        self.chart.get_tk_widget().place(x=1150)

        #self.plot_options()

        #EVENTOS
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
        #OPCIONES DISPONIBLES
        self.options_dict = {}
        self.stock_price = 0
        self.df = pd.DataFrame(columns=["Serie", "Prima", "B&Sch", "Tenencia", "PP", "Cantidad", "Rendimiento"])
        self.df.set_index("Serie", inplace=True)


        #Hilos y cierre del loop

        self.threads = []
        self.get_options_thread = threading.Thread(target=self.get_options,name="get_options")
        self.get_options_thread.start()
        self.threads.append(self.get_options_thread)
        self.update_thread = threading.Thread(target=self.update,name="update_info")
        self.update_thread.start()
        self.threads.append(self.update_thread)


        self.root.mainloop()
        

    

    def plot_options(self):
        y1, y2 = 30, 30
        last = ""
        for i in self.options_dict.values():
                if i.side == "C":
                    self.botons_and_colors(i.ticker, y1, i.side, i.estado)
                    y1 += 16
                else:
                    self.botons_and_colors(i.ticker, y2, i.side, i.estado)
                    y2 += 16
                    last = i
                
        
        
        self.opcion.set(last)
        
        self.text4["text"] = self.current_stock.upper()+" : $ "+str(self.stock_price)


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
        print("Actualizar!",type(self.is_auto.get()),self.is_auto.get() == False)

        loop = True
        while loop:
            print("entra")
            self.stock_price = get_equity(self.current_stock)
            self.options_dict = {}
            
            for x in get_options(self.current_stock)[0]:
                option = Opcion(x[0],x[1],x[2],x[3],self.stock_price)
                self.options_dict[option.ticker] = option
                #["Serie", "Prima", "B&Sch", "Tenencia", "PP", "Cantidad", "Rendimiento"]
                self.df.loc[x[2]] = [x[3], 0, 0, 0, 0, 0]

            print(self.df)

            self.text1.delete("1.0","end")
            self.text2.delete("1.0","end")
            self.text1.insert(tk.INSERT,self.df.iloc[[x for x in range(0, len(self.df)) if self.df.index[x][3] == "C"]].to_string())  # Calls
            self.text2.insert(tk.INSERT,self.df.iloc[[x for x in range(0, len(self.df)) if self.df.index[x][3] == "V"]].to_string())  # Puts

            self.plot_options()


            loop = True if self.is_auto.get() else False
            print("loop: ",loop)

            if loop:
                for seconds in range(self.iter_aut.get()*2):
                    print(seconds/2,self.is_auto.get())
                    time.sleep(0.5)
                    if self.closed:
                        break

            
 
    def update(self):
        while not self.closed:
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
            
            time.sleep(0.05)
            
    


    def load_excel(self):
        os.chdir(os.getcwd()+os.sep+"data"+os.sep+"boards")
        os.system(self.user+"_board.xlsx")
        os.chdir("..")
        os.chdir("..")


    def load_settings(self):

        with open("data/settings_values.txt","r",encoding="utf-8") as handler:          
            self.settings_values = handler.read().split(",")

        

        print(self.settings_values)
        self.is_auto = tk.IntVar()
        self.is_auto.set(int(self.settings_values[0]))
        self.iter_aut = tk.IntVar()
        self.iter_aut.set(int(self.settings_values[1])) 
        self.equity = tk.StringVar()
        self.equity.set(self.settings_values[2])
        self.show_equity = tk.IntVar()
        self.show_equity.set(int(self.settings_values[3]))

        self.add_result_finish = tk.IntVar()
        self.add_result_finish.set(int(self.settings_values[4]))
        self.show_gost = tk.IntVar()
        self.show_gost.set(int(self.settings_values[5]))
        self.range = tk.IntVar()
        self.range.set(int(self.settings_values[6]))
        self.range_lines = tk.IntVar()
        self.range_lines.set(int(self.settings_values[7]))
        self.presition = tk.IntVar()
        self.presition.set(int(self.settings_values[8]))
        self.add_range_lines = tk.IntVar()
        self.add_range_lines.set(int(self.settings_values[9]))
        self.range_line = tk.IntVar()
        self.range_line.set(int(self.settings_values[10]))
        self.range_line2 = tk.IntVar()
        self.range_line2.set(int(self.settings_values[11]))
        self.range_line3 = tk.IntVar()
        self.range_line3.set(int(self.settings_values[12]))



    def init_settings(self):
        self.settings = tk.Toplevel()

        self.settings.geometry("500x500")
        self.settings.title("Settings")
        self.settings.pack_propagate(False)

        #1. Actualizacion automatica o manual
        self.manual = tk.Label(self.settings,text="Actualización manual")
        self.manual.place(x=45,y=30)
        tk.Radiobutton(self.settings,var= self.is_auto, value=0, command=lambda:self.checkbutton(0)).place(x=15,y=30)
        self.auto = tk.Label(self.settings,text="Actualización automatica")
        self.auto.place(x=45,y=60)
        tk.Radiobutton(self.settings,var= self.is_auto, value=1, command=lambda:self.checkbutton(1)).place(x=15,y=60)


        self.auto_iter = tk.Label(self.settings,text="Cada"+" "*23+"segundos")
        self.auto_iter.place(x=210,y=60)
        self.spinbox = tk.ttk.Spinbox(self.settings,textvariable = self.iter_aut,values=[5,7,10,15,20,30,60],format="%3.0f",width=5, command=lambda:print(self.iter_aut.get()))
        self.spinbox.set(self.iter_aut.get())
        self.spinbox.place(x=250,y=62)
        tk.ttk.Separator(self.settings,orient = tk.HORIZONTAL).place(y=100,relx=0.05,relwidth=0.9)
        self.checkbutton(0)

        #2. Mostrar opciones de GGAL
        last_equity_value = self.equity.get()
        tk.Label(self.settings,text="Mostrar opciones de").place(x=45,y=120)
        self.combobox = tk.ttk.Combobox(self.settings,textvariable= self.equity,justify="center",values=(tuple([key.upper()+" - "+value for key, value in self.all_stocks.items()])),state="enabled",width=25)
        self.combobox.set(last_equity_value)
        self.combobox.place(x=180,y=120)
        tk.Label(self.settings,text="Mostrar Subyascente").place(x=45,y=150)
        tk.Checkbutton(self.settings,variable= self.show_equity,onvalue=True,offvalue=False, command=lambda:print(self.show_equity.get())).place(x=15,y=150)
        self.checkbutton(self.is_auto.get())
        tk.ttk.Separator(self.settings,orient = tk.HORIZONTAL).place(y=190,relx=0.05,relwidth=0.9)

        #3. Grafico
        #3.1 Agregar resultado finish
        tk.Label(self.settings,text="Agregar Resultado Finish").place(x=45,y=210)
        tk.Checkbutton(self.settings,variable= self.add_result_finish,onvalue=True,offvalue=False, command=lambda:print(self.add_result_finish.get())).place(x=15,y=210)

        #3.2 Mostrar esperado
        tk.Label(self.settings,text="Mostrar influencia de la posición a armar sobre mi tenencia").place(x=45,y=240)
        tk.Checkbutton(self.settings,variable= self.show_gost,onvalue=True,offvalue=False, command=lambda:print(self.show_gost.get())).place(x=15,y=240)

        #3.3 Mostrar Rango 
        tk.Label(self.settings,text="Mostrar Rango").place(x=45,y=270)
        self.spinbox2 = tk.ttk.Spinbox(self.settings,textvariable= self.range,justify="center",width=5,from_=10,to=30,increment=1)
        self.spinbox2.set(self.range.get())
        self.spinbox2.place(x=200,y=270)

        #3.4 Presición de la curva
        tk.Label(self.settings,text="Presición del gráfico").place(x=45,y=300)
        self.spinbox3 = tk.ttk.Spinbox(self.settings,textvariable= self.presition,justify="center",width=5,values=[50,60,80,100,120,150])
        self.spinbox3.set(self.presition.get())
        self.spinbox3.place(x=200,y=300)


        #3.5 Agregar lineas de rango
        self.add_ranges = tk.Label(self.settings,text="Agregar líneas de rango")
        self.add_ranges.place(x=45,y=330)
        tk.Checkbutton(self.settings,variable= self.add_range_lines,onvalue=True,offvalue=False, command=self.checkbutton_controller).place(x=15,y=330)
        self.spinbox4 = tk.ttk.Spinbox(self.settings,textvariable= self.range_lines,justify="center",width=5,values=(1,2,3),command=lambda:self.spinbox_controller(self.range_lines.get()))
        self.spinbox4.set(self.range_lines.get())
        self.spinbox4.place(x=200,y=330)

        self.first_range = tk.Label(self.settings,text="Primer rango")
        self.first_range.place(x=85,y=360)

        self.spinbox = tk.ttk.Spinbox(self.settings,textvariable = self.iter_aut,values=[5,7,10,15,20,30,60],format="%3.0f",width=5, command=lambda:print(self.iter_aut.get()))
        self.spinbox.set(self.iter_aut.get())
        self.spinbox.place(x=250,y=62)

        self.spinbox6 = tk.ttk.Spinbox(self.settings,textvariable= self.range_line,justify="center",width=5,from_=5,to=30)
        self.spinbox6.set(self.range_line.get())
        self.spinbox6.place(x=200,y=360)

        self.second_range = tk.Label(self.settings,text="Segundo rango")
        self.second_range.place(x=85,y=390)
        self.spinbox7 = tk.ttk.Spinbox(self.settings,textvariable= self.range_line2,justify="center",width=5,from_=5,to=30)
        self.spinbox7.set(self.range_line2.get())
        self.spinbox7.place(x=200,y=390)

        self.third_range =tk.Label(self.settings,text="Tercer rango")
        self.third_range.place(x=85,y=420)
        self.spinbox8 = tk.ttk.Spinbox(self.settings,textvariable= self.range_line3,justify="center",width=5,from_=5,to=30)
        self.spinbox8.set(self.range_line3.get())
        self.spinbox8.place(x=200,y=420)

        self.checkbutton_controller()
        self.spinbox_controller(self.range_lines.get())

        tk.Button(self.settings,text="Guardar y salir",command=lambda:self.apply_settings(last_equity_value != self.equity.get())).place(relx=0.8,rely=0.9)


    def apply_settings(self,equity_changed):
        print("Aplicando cambios!")
        print(equity_changed)

        if self.is_auto.get():
            print("Automatico!")
            print("is alive? ",self.update_thread.is_alive())
            if not self.update_thread.is_alive():
                self.update_thread = threading.Thread(target=self.get_options)
                self.update_thread.start()
            self.button7["state"] = "disabled"
        else:
            self.button7["state"] = "normal"

        if equity_changed:
            print("cambio")
            self.on_closing()
            print("se cerró")
            App(self.user)

        if not self.show_equity.get():
            self.text4["state"] = "disabled"
        else:
            self.text4["state"] = "normal"




        self.settings.destroy()

    def checkbutton(self,option):
        state = "normal" if option == 1 else "disabled"
        for i in [self.auto_iter,self.spinbox]:
            print(state)
            i["state"] = state

    def spinbox_controller(self,lines):
        widgets = [self.spinbox6,self.first_range,self.spinbox7,self.second_range,self.spinbox8,self.third_range]
        for i in range(len(widgets)):
            state = "normal" if i < lines*2 else "disabled"
            widgets[i]["state"] = state
    
    def checkbutton_controller(self):
        state = "normal" if self.add_range_lines.get() else "disabled"
        for i in [self.spinbox4,self.spinbox6,self.first_range,self.spinbox7,self.second_range,self.spinbox8,self.third_range]:
            i["state"] = state
        if self.add_range_lines.get():
            self.spinbox_controller(self.range_lines.get())

    def on_closing(self):
        response = tk.messagebox.askyesnocancel(title="Salir",message="Quiere guardar los cambios?")
        print(response)
        
        if response is not None:
            if response:
                self.save_changes()
            self.closed = True
            time.sleep(1)
            print(self.update_thread.is_alive(),self.get_options_thread.is_alive())
            self.root.destroy()
        self.database.update("users","last_login","to_timestamp("+str(datetime.timestamp(datetime.now()))+")")

    def save_changes(self):
        self.total_settings = [str(self.is_auto.get()),str(self.iter_aut.get()),str(self.equity.get()),str(self.show_equity.get()),str(self.add_result_finish.get()),str(self.show_gost.get()),
                            str(self.range.get()),str(self.range_lines.get()),str(self.presition.get()),str(self.add_range_lines.get()),str(self.range_line.get()),str(self.range_line2.get()),str(self.range_line3.get())]

        with open("data/settings_values.txt","w",encoding="utf-8") as handler:
            handler.write(",".join(self.total_settings))
            print("Guardado!")

    def change_user(self):
        self.on_closing()
        Login()

    def buy(self):
        print("aaaaaaaaaaaaaaa")
        print(self.opcion.get(),self.entry_var.get())
        cant = int(self.entry_var.get())
        a = "buy" if cant > 0 else "sell"
        op = self.options_dict[self.opcion.get()]
        print(op.ticker,op.price,op.side,op.base,op.subyascente)
        now = "to_timestamp("+str(datetime.timestamp(datetime.now()))+")"
        self.database.insert_into("historial",[now,a,abs(cant),op.price,(-cant)*op.price,op.ticker])


        

        



class Opcion:

    def __init__(self,base,side,ticker,price,subyascente):
        try:
            self.base = float(base)
        except ValueError: #Notación cientifica
            self.base = float(base.replace(",",""))
            print(self.base)
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


