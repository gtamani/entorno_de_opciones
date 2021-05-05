import threading,time

from Login import Login
from App import App
from Settings import Settings

def logged_in():
        app = None
        while app is None:
            if login.current_user:
                return App(login.current_user)
        


if __name__ == "__main__":

    login = Login()
    app = logged_in() #Main thread



    



