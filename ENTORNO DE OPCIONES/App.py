import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time, threading

from API_data import *
from get_graph import *

from Settings import Settings


class App:

    def __init__(self,user):
        t0 = time.time()
        self.user = user
        self.root = tk.Tk()
        self.root.geometry("2200x600")
        self.root.title("Entorno de opciones GGAL")
        self.root.pack_propagate(False)
        self.settings=False
        
        self.load_settings()

        # Menu
        self.menu_bar = tk.Menu(self.root)
        self.menu_bar.add_separator()
        self.menu_bar.add_command(label="Cargar Datos",command=self.load_excel)

        

        self.menu_bar.add_separator()
        self.menu_bar.add_command(label="Guardar",command=lambda:threading.Thread(target=self.save_changes).start())
        self.menu_bar.add_separator()
        self.menu_bar.add_command(label="Configuraciones",command=lambda:threading.Thread(target=self.init_settings).start())
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
        self.button7.place(x="700",y="567")
        self.radiobuttons_shown = False
        
        

        # Grafico
        self.fig, self.ax = plt.subplots(1,1,figsize=(7, 4), dpi=100)
        x,y,y2 = get_curves_sumed(get_portfolio("gtamani"))
        self.ax.plot(x,y)
        self.ax.plot(x,y2)

        self.ax.set_xlabel("Precio GGAL")
        self.ax.set_xlabel("($) Ganancia")
        self.ax.grid()
        self.ax.set_xlim(100,140)
        
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

        self.update_thread = threading.Thread(target=self.get_options)
        self.update_thread.start()

        #Hilos y cierre del loop

        self.root.after(1,lambda: threading.Thread(target=self.update).start())
        self.root.mainloop()
        



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
        print("Actualizar!",type(self.is_auto.get()),self.is_auto.get() == False)

        loop = True
        while loop:
            print("entra")
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

            self.plot_options()


            loop = True if self.is_auto.get() else False
            print("loop: ",loop)

            if loop:
                for seconds in range(self.iter_aut.get()):
                    print(seconds,self.is_auto.get())
                    time.sleep(1)

            
 
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
        tk.Label(self.settings,text="Mostrar opciones de").place(x=45,y=120)
        self.combobox = tk.ttk.Combobox(self.settings,textvariable= self.equity,justify="center",values=("GGAL - Galicia","ALUA - Aluar","COME - Comercial del Plata","PAMP Pampa Energia","YPFD - YPF"),state="enabled",width=25)
        self.combobox.set(self.equity.get())
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

        tk.Button(self.settings,text="Guardar y salir",command=self.apply_settings).place(relx=0.8,rely=0.9)


    def apply_settings(self):
        print("Aplicando cambios!")
        if self.is_auto:
            print("Automatico!")
            if not self.update_thread.is_alive():
                self.update_thread = threading.Thread(target=self.get_options)
                self.update_thread.start()


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
            self.root.destroy()

    def save_changes(self):
        self.total_settings = [str(self.is_auto.get()),str(self.iter_aut.get()),str(self.equity.get()),str(self.show_equity.get()),str(self.add_result_finish.get()),str(self.show_gost.get()),
                            str(self.range.get()),str(self.range_lines.get()),str(self.presition.get()),str(self.add_range_lines.get()),str(self.range_line.get()),str(self.range_line2.get()),str(self.range_line3.get())]

        with open("data/settings_values.txt","w",encoding="utf-8") as handler:
            handler.write(",".join(self.total_settings))
            print("Guardado!")


        

        



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


