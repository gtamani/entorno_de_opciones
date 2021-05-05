import tkinter as tk
import tkinter.ttk
import os
import pandas as pd

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

