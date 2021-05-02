import tkinter as tk
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()


class Login:

    def __init__(self):

        self.root = tk.Tk()
        self.root.geometry("600x300")
        self.root.title("Log In")
        self.text = tk.Label()
        self.text.place(x=30,width=540,height=100)
        self.current_user = ""
        
        with open(os.getcwd()+os.sep+"data"+os.sep+"users.txt","r",encoding="utf-8") as handler:
            self.users = [x.strip('\n') for x in handler.readlines()]

        if self.users == []:
            self.new_user()
        else:
            self.text["text"] = "¿Eres "+self.users[0]+"?"
            self.button_yes = tk.Button(text="Sí",command= self.save_and_exit).place(x=200,y=60,width=100,height=20)
            self.button_no = tk.Button(text="No",command= self.show_users).place(x=310,y=60,width=100,height=20)

            

        self.root.mainloop()

    def get_user(self,user):
        print(user.get())
        pd.DataFrame(columns=["Opcion","Side","Base","Precio","Strike"]).to_excel("./data/boards/"+user.get()+"_board.xlsx")

    def save_and_exit(self):
        self.current_user = self.users[0]
        print("save")
        pass
    
    def new_user(self):
        self.entry_var = tk.StringVar()
        self.entry = tk.Entry(textvariable= self.entry_var).place(x=30,y=60,width=410,height=20)
        self.button = tk.Button(text="Go!",command=lambda: self.get_user(self.entry_var)).place(x=450,y=60,width=120,height=20)
        self.text["text"] = "Nuevo por aquí? Define un usuario"


    def show_users(self):
        print("show")
        if len(self.users) == 1:
            self.new_user()
        else:
            pass


Login()
