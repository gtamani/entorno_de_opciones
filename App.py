import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import style, dates as mdates

import time, threading
from datetime import datetime

from API_data import Data_market
from get_graph import *

from Settings import Settings
from Login import Login
from pg_database import Postgres_database


class App:

    def __init__(self,user):
        self.user = user
        self.root = tk.Tk()
        self.database = Postgres_database()
        self.market_data = Data_market()
        self.settings= False
        self.portfolio = False
        self.historial = False
        self.closed = False
        self.new_changes = True
        self.equity_changed = True
        self.restart_update = False
        self.all_stocks = {"ggal":"Galicia","alua":"Aluar", "come":"Comercial del Plata","pamp":"Pampa Energia","ypfd":"YPF"}
        
        
        self.load_settings()
        self.current_stock = self.equity.get()[:4].lower()

        self.root.geometry("1870x600")
        self.root.title("Entorno de opciones "+self.current_stock.upper())
        self.root.pack_propagate(False)
        self.root.resizable(False,False)

        # Menu
        self.menu_bar = tk.Menu(self.root)
        self.menu_bar.add_separator()
        self.menu_bar.add_command(label="Cargar Datos",command=self.load_excel)
        self.menu_bar.add_separator()
        self.menu_bar.add_command(label="Guardar",command=lambda:threading.Thread(target=self.save_changes).start())
        self.menu_bar.add_separator()
        self.menu_bar.add_command(label="Tenencia",command=lambda:threading.Thread(target=self.tk_portfolio).start())
        self.menu_bar.add_separator()
        self.menu_bar.add_command(label="Historial",command=lambda:threading.Thread(target=self.tk_historial).start())
        self.menu_bar.add_separator()
        self.menu_bar.add_command(label="Configuraciones",command=lambda:threading.Thread(target=self.init_settings).start())
        self.menu_bar.add_separator()
        self.menu_bar.add_command(label="Cambiar de usuario",command=self.change_user)
        self.menu_bar.add_separator()
        self.menu_bar.add_command(label="Salir",command=self.on_closing)
        self.root.config(menu=self.menu_bar)

        # Main texts
        self.text1 = tk.Text(self.root)
        self.text1.place(x=30, height=550, width=540)
        self.text2 = tk.Text(self.root)
        self.text2.place(x=600, height=550, width=540)
        self.text4 = tk.Label(self.root,font=("Verdana",16))
        self.text4.place(x=850, y=560) #
        

        #Entry
        self.entry_var = tk.StringVar()
        self.entry = tk.Entry(textvariable=self.entry_var,justify=tk.CENTER)
        self.entry.place(x=240,y=567,width=50)

        #Radiobuttons
        self.opcion = tk.StringVar()
        self.opcion.set("")
        
        #Labels
        self.text3 = tk.Label(self.root, text="")
        self.text3.place(x=1700, y=425)
        self.text5 = tk.Label(self.root)
        self.text5.place(x=300, y=567)

        #Buttons
        self.button1 = tk.Button(self.root, text="Operar!",command=self.buy)
        self.button1.place(x="125", y="567")
        self.button7 = tk.Button(self.root,text="Actualizar!")
        self.button7["command"] = lambda: threading.Thread(target=self.get_options,name="update_thread").start()
        self.button7.place(x="700",y="567")
        self.radiobuttons_shown = False

        if self.is_auto.get():
            self.button7["state"] = "disabled"

        #Available options
        self.options_dict = {}
        self.df = pd.DataFrame(columns=["Serie", " "*3+"Prima", "B&Sch", " "*7+"Delta", "Gamma", "Tetha", "Vega"])
        self.df.set_index("Serie", inplace=True)

        # Graph
        self.x,self.y,self.y2 = np.nan,np.nan,np.nan
        style.use("Solarize_Light2")
        self.fig, self.ax = plt.subplots(2,1,figsize=(7, 5.5), dpi=100)
        self.ax[0].plot(0,0,0,0)
        self.ax[0].set_xlabel("Precio ")
        self.ax[0].set_xlabel("($) Ganancia")
        self.ax[0].grid()
        self.stock_price = self.market_data.get_equity(self.current_stock)
        print("SELF STOCK: ",self.stock_price)
        threading.Thread(self.get_historical_volatility()).start()
        self.animation= FuncAnimation(self.fig,func=self.update_graph,interval= 1000)
        self.chart = FigureCanvasTkAgg(self.fig, self.root)
        self.chart.draw()
        self.chart.get_tk_widget().place(x=1150)

        #Events
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        #Threads and loops
        self.threads = []
        self.get_options_thread = threading.Thread(target=self.get_options,name="get_options")
        self.get_options_thread.start()
        self.threads.append(self.get_options_thread)
        self.update_thread = threading.Thread(target=self.update,name="update_info")
        self.update_thread.start()
        self.threads.append(self.update_thread)
        self.root.mainloop()
    
    def get_historical_volatility(self):
        self.ax[1].clear()

        data = self.market_data.get_volatilidad_historica(self.current_stock,data=self.daysgraph2.get(),last=self.volatility_days.get())
        x,y,stocky,last = data[0][0],data[0][1],data[0][2],data[1]
        self.stock_close = stocky[-1]
        print("CLOSEEEEEEEE:",self.stock_close)
        print(stocky)

        if str(self.stock_close) != "nan":
            ret = round((((self.stock_price-self.stock_close)/self.stock_price)*100),2)
            ret_color = "red" if ret < 0 else "green"
            self.text8 = tk.Label(self.root,text=f" {ret}%",font=("Verdana",16),fg=ret_color)
            self.text8.place(x=1080, y=560) #

        self.ax[1].plot(x,y)
        self.ax[1].plot([x[0],x[-1]],[last,last],ls="--",linewidth=0.5,label=f"VI: {round(last*100,2)}%")
        

        self.ax[1].legend()
        

        fmt_half_year = mdates.MonthLocator(interval=1)
        self.ax[1].xaxis.set_major_locator(fmt_half_year)
        #self.ax[1].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        self.fig.autofmt_xdate()
        


    def update_graph(self,i):

        if self.new_changes or self.equity_changed:
            self.ax[0].clear()
            self.fig.legends = []
            self.ax[0].axhline(y=0,ls="--",c="black",linewidth=0.3)
            

            if self.new_changes:
                query = "SELECT options.ticker, options.strike, options.price, tenencia.quant,\
                            options.opex FROM tenencia INNER JOIN options \
                            ON tenencia.options = options.ticker;"
                self.x,self.y,self.y2 = get_curves_sumed(self.database.query(query),presition=self.presition.get())
                print("YYYYY",self.y)
                print("YYY222",self.y2)
                self.ax[0].plot(self.x,self.y)
                if self.add_result_finish.get():
                    self.ax[0].plot(self.x,self.y2)
                self.new_changes = False

            if self.equity_changed:
                self.ax[0].plot(self.x,self.y)
                if self.add_result_finish.get():
                    self.ax[0].plot(self.x,self.y2)            
                self.ax[0].axvline(self.stock_price,linewidth=0.7)

                if self.add_range_lines.get():
                    range_lines =  {0:{"line":self.range_line,"color":"#1D8348"},
                                    1:{"line":self.range_line2,"color":"#9A7D0A"},
                                    2:{"line":self.range_line3,"color":"#935116"}}

                    for i in range(self.range_lines.get()):
                        print(i," added")
                        percentage = range_lines[i]["line"].get()/100
                        legend= "Rango "+str(percentage)+"- ("+str(round((1-percentage)*self.stock_price,2))+","+str(round((1+percentage)*self.stock_price,2))+")"
                        range_lines[i]["legend"] = legend 
                        self.ax[0].axvline(self.stock_price * (1+percentage),ls="--",linewidth=0.5, c=range_lines[i]["color"])
                        self.ax[0].axvline(self.stock_price * (1-percentage),ls="--",linewidth=0.5, c=range_lines[i]["color"])
                    self.fig.legend([range_lines[x]["legend"] for x in range(self.range_lines.get())])


                self.ax[0].set_xlim([self.stock_price*(1-(self.range.get()/100)),self.stock_price*(1+(self.range.get()/100))])
            

                self.equity_changed = False

        return self.ax[0],
    
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
            self.stock_price = self.market_data.get_equity(self.current_stock)
            self.equity_changed = True
            self.options_dict = {}
            
            data_set_into = []
            data_update = {}
            opex_timestamp = datetime.timestamp(self.market_data.dt_opex)


            for x in self.market_data.get_options(self.current_stock):
                x[0] = float(x[0].replace(",",""))
                greeks = get_greeks(self.stock_price,x[0],self.rate.get()/100,self.market_data.days_to_opex/365,self.sigma.get()/100,x[1])
                print(self.stock_price,x[0],self.rate.get(),self.market_data.days_to_opex/365,self.sigma.get(),x[1])
                #print("GREEKS: ",greeks)
                option = Opcion(x[0],x[1],x[2],x[3],self.stock_price,opex_timestamp)
                self.options_dict[option.ticker] = option
                #["Serie", "Prima", "B&Sch", "Delta", "Gamma", "Tetha", "Vega"]
                self.df.loc[x[2]] = [x[3], round(greeks["bsch"],3), round(greeks["delta"],3), round(greeks["gamma"],3), round(greeks["theta"],3), round(greeks["vega"],3)]
                data_set_into.append([option.subyascente,option.ticker,option.price,option.base,"to_timestamp("+str(opex_timestamp)+")"])
                data_update[option.ticker] = option.price
                
            

            self.database.query("TRUNCATE TABLE options")
            self.database.insert_into("options",data_set_into)
            self.database.multiple_update("tenencia","current_price","options",data_update)

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
                    print(seconds)
                    if self.closed or self.restart_update:
                        self.restart_update = False
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
            #print(self.threads)            
            time.sleep(0.05)         
        
    
    def load_excel(self):
        os.chdir(os.getcwd()+os.sep+"data"+os.sep+"boards")
        os.system(self.user+"_board.xlsx")
        os.chdir("..")
        os.chdir("..")


    def load_settings(self):

        with open("data/settings_values.txt","r",encoding="utf-8") as handler:          
            self.settings_values = handler.read().split(",")

        

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
        self.add_range_lines = tk.IntVar()
        self.add_range_lines.set(int(self.settings_values[7]))
        self.presition = tk.IntVar()
        self.presition.set(int(self.settings_values[8]))
        self.range_lines = tk.IntVar()
        self.range_lines.set(int(self.settings_values[9]))
        self.range_line = tk.IntVar()
        self.range_line.set(int(self.settings_values[10]))
        self.range_line2 = tk.IntVar()
        self.range_line2.set(int(self.settings_values[11]))
        self.range_line3 = tk.IntVar()
        self.range_line3.set(int(self.settings_values[12]))
        self.daysgraph2 = tk.IntVar()
        self.daysgraph2.set(int(self.settings_values[13]))
        self.volatility_days = tk.IntVar()
        self.volatility_days.set(int(self.settings_values[14]))
        self.sigma = tk.IntVar()
        self.sigma.set(int(self.settings_values[15]))
        self.rate = tk.IntVar()
        self.rate.set(int(self.settings_values[16]))



    def init_settings(self):
        self.settings = tk.Toplevel()

        self.settings.geometry("500x670")
        self.settings.title("Settings")
        self.settings.pack_propagate(False)
        self.settings.resizable(False,False)

        last_values = {"equity":self.equity.get(),"sigma":self.sigma.get(),"rate":self.rate.get(),"days_graph2":self.daysgraph2.get(),"vi_days":self.volatility_days.get()}
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
        tk.Label(self.settings,text="Mostrar opciones de").place(x=45,y=120)
        self.combobox = tk.ttk.Combobox(self.settings,textvariable= self.equity,justify="center",values=(tuple([key.upper()+" - "+value for key, value in self.all_stocks.items()])),state="enabled",width=25)
        self.combobox.set(last_values["equity"])
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

        tk.ttk.Separator(self.settings,orient = tk.HORIZONTAL).place(y=460,relx=0.05,relwidth=0.9)

        self.third_range =tk.Label(self.settings,text="Días p/ cálculo del gráfico")
        self.third_range.place(x=45,y=490)
        self.spinbox9 = tk.ttk.Spinbox(self.settings,textvariable= self.daysgraph2,justify="center",width=5,values=(70,100,180,200,250,300,365))
        self.spinbox9.set(self.daysgraph2.get())
        self.spinbox9.place(x=270,y=490)

        self.third_range =tk.Label(self.settings,text="Ruedas para el cálculo de la volatilidad")
        self.third_range.place(x=45,y=520)
        self.spinbox10 = tk.ttk.Spinbox(self.settings,textvariable= self.volatility_days,justify="center",width=5,values=(20,30,40,50,60,70))
        self.spinbox10.set(self.volatility_days.get())
        self.spinbox10.place(x=270,y=520)

        tk.ttk.Separator(self.settings,orient = tk.HORIZONTAL).place(y=560,relx=0.05,relwidth=0.9)

        self.third_range =tk.Label(self.settings,text="Sigma - Volatilidad")
        self.third_range.place(x=45,y=590)
        self.spinbox11 = tk.ttk.Spinbox(self.settings,textvariable= self.sigma,justify="center",width=5,from_=1,to=100)
        self.spinbox11.set(self.sigma.get())
        self.spinbox11.place(x=200,y=590)

        self.third_range =tk.Label(self.settings,text="Tasa libre de riesgo")
        self.third_range.place(x=45,y=620)
        self.spinbox12 = tk.ttk.Spinbox(self.settings,textvariable= self.rate,justify="center",width=5,from_=1,to=100)
        self.spinbox12.set(self.rate.get())
        self.spinbox12.place(x=200,y=620)
        



        tk.Button(self.settings,text="Guardar y salir",command=lambda:self.apply_settings(last_values)).place(relx=0.8,rely=0.9)


    def apply_settings(self,last_values):
        print("Aplicando cambios!")
        print(last_values)

        if self.is_auto.get():
            print("Automatico!")
            print("is alive? ",self.get_options_thread.is_alive())
            if not self.get_options_thread.is_alive():
                self.get_options_thread = threading.Thread(target=self.get_options)
                self.get_options_thread.start()
            self.button7["state"] = "disabled"
        else:
            self.button7["state"] = "normal"

        if last_values["equity"] != self.equity.get():
            print("cambio")
            self.on_closing()
            print("se cerró")
            App(self.user)

        if not self.show_equity.get():
            self.text4["state"] = "disabled"
        else:
            self.text4["state"] = "normal"

        if last_values["sigma"] != self.sigma.get() or last_values["rate"] != self.rate.get():
            if not self.get_options_thread.is_alive():
                self.get_options()
            #self.new_changes = True
            

            

        if last_values["vi_days"] != self.volatility_days.get() or last_values["days_graph2"] != self.daysgraph2.get():
            print("cambios detectados")
            threading.Thread(target=self.get_historical_volatility).start()

        self.equity_changed = True
        self.new_changes = True




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
        self.database.update("users","last_login","to_timestamp("+str(datetime.timestamp(datetime.now()))+")","username",self.user)

    def tk_portfolio(self):
        print("portfolio!")
        self.portfolio = tk.Toplevel()
        self.portfolio.title("Tenencia")
        self.portfolio.geometry("1200x400")
        self.portfolio.pack_propagate(False)
        self.portfolio.resizable(False,False)

        frame = tk.Frame(self.portfolio)
        frame.pack()
        scrollbar = ttk.Scrollbar(frame)
        my_tree = ttk.Treeview(frame,height=5,yscrollcommand=scrollbar.set)

        
        scrollbar.pack(side=tk.RIGHT,fill=tk.Y)
        scrollbar.config(command=my_tree.yview)
    

        columns = ("Opcion","Cantidad","Avg. Price","Precio Actual","Valorizado","Turnover")
        my_tree["columns"] = columns
        
        my_tree.column("#0",width=10)
        my_tree.heading("#0",text="")
        for c in columns:
            #my_tree.column(c,width=10)
            my_tree.heading(c,text=c)
        
        try:
            query= self.database.select("tenencia",columns='("options","quant","avg_price","current_price","total_value",((("current_price"/"avg_price")-1))*100)')
        except:
            query= self.database.select("tenencia",columns='("options","quant","avg_price","current_price","total_value","current_price"-"avg_price")')
            
        print("QUERY: ",query)
        for values in query:
            values = values[0].replace("(","").replace(")","").split(",")
            values[-1] = round(float(values[-1]),2)
            print(values)
            my_tree.insert(parent="",index="end",values=values,)

        """
        my_tree.tag_a
        self.text1.tag_add(etiqueta, inicio, fin)
            self.text1.tag_config(etiqueta, background=colors[itm], foreground="black"
        """
        my_tree.pack()


        tk.Button(self.portfolio,text="Salir").place(relx=0.8,rely=0.9)
        

    def tk_historial(self):
        print("historial!")
        self.historial = tk.Toplevel()
        self.historial.title("Historial")
        self.historial.geometry("1200x400")
        self.historial.pack_propagate(False)
        self.historial.resizable(False,False)

        my_tree = ttk.Treeview(self.historial,height=5)
        columns = ("Fecha","Side","Cantidad","Precio","Total","Opcion")
        my_tree["columns"] = columns
        
        my_tree.column("#0",width=10)
        my_tree.heading("#0",text="")
        for c in columns:
            #my_tree.column(c,width=10)
            my_tree.heading(c,text=c)
        for values in self.database.select("historial"):
            my_tree.insert(parent="",index="end",values=values[1:],)
        my_tree.pack()


        tk.Button(self.historial,text="Salir").place(relx=0.8,rely=0.9)
        

    def save_changes(self):
        self.total_settings = [str(self.is_auto.get()),str(self.iter_aut.get()),str(self.equity.get()),str(self.show_equity.get()),str(self.add_result_finish.get()),str(self.show_gost.get()),
                            str(self.range.get()),str(self.range_lines.get()),str(self.presition.get()),str(self.add_range_lines.get()),str(self.range_line.get()),str(self.range_line2.get()),
                            str(self.range_line3.get()),str(self.daysgraph2.get()),str(self.volatility_days.get()),str(self.sigma.get()),str(self.rate.get())]

        with open("data/settings_values.txt","w",encoding="utf-8") as handler:
            handler.write(",".join(self.total_settings))
            print("Guardado!")

    def change_user(self):
        self.on_closing()
        Login()

    def buy(self):
        print("aaaaaaaaaaaaaaa")
        self.lote = 100
        print(self.opcion.get(),self.entry_var.get())
        cant = int(self.entry_var.get())
        a = "buy" if cant > 0 else "sell"
        op = self.options_dict[self.opcion.get()]
        print(op.ticker,op.price,op.side,op.base,op.subyascente)
        now = "to_timestamp("+str(datetime.timestamp(datetime.now()))+")"
        self.database.insert_into("historial",[[now,a,abs(cant),op.price,round((-cant)*op.price*self.lote,2),op.ticker]])

        self.equity_changed = True
        

        try:
            data = self.database.select("tenencia",columns="(quant,avg_price)",condition="options = '"+op.ticker+"'")[0][0]
            data = data.replace("(","").replace(")","")
            cant_ant, avg_ant = data.split(",")
            cant_ant,avg_ant = int(cant_ant),float(avg_ant)
            exists = True

        except:
            cant_ant, avg_ant= 0,0
            exists = False
            

        #if (cant_ant - cant) < 0 and op.side == "V":
        #    print("Lanzado en descubierto!")
        cant_total = cant_ant+cant

        if cant_total:
            if a == "buy":
                print("entra por buy")
                total_value = (cant_ant*avg_ant+cant*op.price)*self.lote
                avg_price = (total_value/self.lote)/cant_total
            else:
                if cant_ant:
                    print("entra por else")
                    avg_price = avg_ant
                else:
                    print("entra por else2")

                    avg_price = op.price

                total_value = cant_total*avg_price*100
            print("DATA DEL TABLE: ",avg_price,total_value,cant_total,cant,cant_total,cant_ant)


            
            if not exists:
                self.database.insert_into("tenencia",[[op.ticker,cant_total,avg_price,op.price,round(total_value,2)]])
            else:
                self.database.update("tenencia","quant",cant_total,"options",op.ticker)
                self.database.update("tenencia","avg_price",avg_price,"options",op.ticker)
                self.database.update("tenencia","total_value",total_value,"options",op.ticker)
        else:
            self.database.delete("tenencia", "options",op.ticker)

        self.new_changes = True



        

        



class Opcion:

    def __init__(self,base,side,ticker,price,subyascente,opex):
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
        self.opex = opex

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


