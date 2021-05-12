import tkinter as tk

class Settings:
    def __init__(self,settings_values = [0,10,"GGAL - Galicia",1,0,1,15,0,50,1,5,10,15]):
        self.root = tk.Tk()
        self.root.geometry("500x500")
        self.root.title("Settings")
        self.root.pack_propagate(False)
        self.saved = False

        self.is_auto = tk.IntVar()
        self.is_auto.set(settings_values[0])
        self.iter_aut = tk.IntVar()
        self.iter_aut.set(settings_values[1])
        self.equity = tk.StringVar()
        self.equity.set(settings_values[2])
        self.show_equity = tk.IntVar()
        self.show_equity.set(settings_values[3])
        self.add_result_finish = tk.IntVar()
        self.add_result_finish.set(settings_values[4])
        self.show_gost = tk.IntVar()
        self.show_gost.set(settings_values[5])
        self.range = tk.IntVar()
        self.range.set(settings_values[6])
        self.range_lines = tk.IntVar()
        self.range_lines.set(settings_values[7])
        self.presition = tk.IntVar()
        self.presition.set(settings_values[8])
        self.add_range_lines = tk.IntVar()
        self.add_range_lines.set(settings_values[9])
        self.range_line = tk.IntVar()
        self.range_line.set(settings_values[10])
        self.range_line2 = tk.IntVar()
        self.range_line2.set(settings_values[11])
        self.range_line3 = tk.IntVar()
        self.range_line3.set(settings_values[12])

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.show_widgets()

    def __str__(self):
        return [self.is_auto,self.iter_aut,self.equity,self.show_equity,self.add_result_finish,
        self.show_gost,self.range,self.range_lines,self.range_line,self.range_line2,self.range_line3]

    def show_widgets(self):

        #1. Actualizacion automatica o manual
        self.manual = tk.Label(self.root,text="Actualización manual")
        self.manual.place(x=45,y=30)
        tk.Radiobutton(self.root,var= self.is_auto, value=0, command=lambda:self.checkbutton(0)).place(x=15,y=30)
        self.auto = tk.Label(self.root,text="Actualización automatica")
        self.auto.place(x=45,y=60)
        tk.Radiobutton(self.root,var= self.is_auto, value=1, command=lambda:self.checkbutton(1)).place(x=15,y=60)
        self.auto_iter = tk.Label(self.root,text="Cada"+" "*23+"segundos")
        self.auto_iter.place(x=210,y=60)
        self.spinbox = tk.ttk.Spinbox(self.root,textvariable = self.iter_aut,values=[5,7,10,15,20,30,60],format="%3.0f",width=5, command=lambda:print(self.iter_aut.get()))
        self.spinbox.set(10)
        self.spinbox.place(x=250,y=62)
        tk.ttk.Separator(self.root,orient = tk.HORIZONTAL).place(y=100,relx=0.05,relwidth=0.9)
        self.checkbutton(0)

        #2. Mostrar opciones de GGAL
        tk.Label(self.root,text="Mostrar opciones de").place(x=45,y=120)
        self.combobox = tk.ttk.Combobox(self.root,textvariable= self.equity,justify="center",values=("GGAL - Galicia","ALUA - Aluar","COME - Comercial del Plata","PAMP Pampa Energía","YPFD - YPF"),state="enabled",width=25)
        self.combobox.set("GGAL - Galicia")
        self.combobox.place(x=180,y=120)
        tk.Label(self.root,text="Mostrar Subyascente").place(x=45,y=150)
        tk.Checkbutton(self.root,variable= self.show_equity,onvalue=True,offvalue=False, command=lambda:print(self.show_equity.get())).place(x=15,y=150)
        self.checkbutton(self.is_auto.get())
        tk.ttk.Separator(self.root,orient = tk.HORIZONTAL).place(y=190,relx=0.05,relwidth=0.9)

        #3. Grafico
        #3.1 Agregar resultado finish
        tk.Label(self.root,text="Agregar Resultado Finish").place(x=45,y=210)
        tk.Checkbutton(self.root,variable= self.add_result_finish,onvalue=True,offvalue=False, command=lambda:print(self.add_result_finish.get())).place(x=15,y=210)

        #3.2 Mostrar esperado
        tk.Label(self.root,text="Mostrar influencia de la posición a armar sobre mi tenencia").place(x=45,y=240)
        tk.Checkbutton(self.root,variable= self.show_gost,onvalue=True,offvalue=False, command=lambda:print(self.show_gost.get())).place(x=15,y=240)

        #3.3 Mostrar Rango 
        tk.Label(self.root,text="Mostrar Rango").place(x=45,y=270)
        self.spinbox2 = tk.ttk.Spinbox(self.root,textvariable= self.range,justify="center",width=5,from_=10,to=30,increment=1)
        self.spinbox2.set(10)
        self.spinbox2.place(x=200,y=270)

        #3.4 Presición de la curva
        tk.Label(self.root,text="Presición del gráfico").place(x=45,y=300)
        self.spinbox3 = tk.ttk.Spinbox(self.root,textvariable= self.presition,justify="center",width=5,values=[50,60,80,100,120,150])
        self.spinbox3.set(100)
        self.spinbox3.place(x=200,y=300)


        #3.5 Agregar lineas de rango
        self.add_ranges = tk.Label(self.root,text="Agregar líneas de rango")
        self.add_ranges.place(x=45,y=330)
        tk.Checkbutton(self.root,variable= self.add_range_lines,onvalue=True,offvalue=False, command=self.checkbutton_controller).place(x=15,y=330)
        self.spinbox4 = tk.ttk.Spinbox(self.root,textvariable= self.range_lines,justify="center",width=5,values=(1,2,3),command=lambda:self.spinbox_controller(self.range_lines.get()))
        self.spinbox4.set(1)
        self.spinbox4.place(x=200,y=330)

        self.first_range = tk.Label(self.root,text="Primer rango")
        self.first_range.place(x=85,y=360)

        self.spinbox = tk.ttk.Spinbox(self.root,textvariable = self.iter_aut,values=[5,7,10,15,20,30,60],format="%3.0f",width=5, command=lambda:print(self.iter_aut.get()))
        self.spinbox.set(10)
        self.spinbox.place(x=250,y=62)

        self.spinbox6 = tk.ttk.Spinbox(self.root,textvariable= self.range_line,justify="center",width=5,from_=5,to=30)
        self.spinbox6.set(5)
        self.spinbox6.place(x=200,y=360)

        self.second_range = tk.Label(self.root,text="Segundo rango")
        self.second_range.place(x=85,y=390)
        self.spinbox7 = tk.ttk.Spinbox(self.root,textvariable= self.range_line2,justify="center",width=5,from_=5,to=30)
        self.spinbox7.set(10)
        self.spinbox7.place(x=200,y=390)

        self.third_range =tk.Label(self.root,text="Tercer rango")
        self.third_range.place(x=85,y=420)
        self.spinbox8 = tk.ttk.Spinbox(self.root,textvariable= self.range_line3,justify="center",width=5,from_=5,to=30)
        self.spinbox8.set(15)
        self.spinbox8.place(x=200,y=420)

        self.checkbutton_controller()
        self.spinbox_controller(self.range_lines.get())

        tk.Button(self.root,text="Guardar y salir",command=lambda:self.root.destroy()).place(relx=0.8,rely=0.9)


        self.root.mainloop()

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
        print("Saliendo!")
        self.root.destroy()


