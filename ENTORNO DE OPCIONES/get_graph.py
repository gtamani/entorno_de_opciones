import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

def call(x,base,prima,cant):
    if x < (base-prima):
        return -prima*cant
    else:
        return (x-base)*cant

def put(x,base,prima,cant):
    if x > (base+prima):
        return -prima*cant
    else:
        return -(x-base)*cant


def get_finish_curve(side,base,prima,cant,presition=50):
    x = np.linspace(10,200,presition)
    if side == "C":
        return x,[call(i,base,prima,cant) for i in x]
    return x,[put(i,base,prima,cant) for i in x]

def get_finish_curve_sumed(df,presition=50):
    y = [0]*presition
    for index,row in df.iterrows():
        x,curve = get_finish_curve(row.Side,float(row.Strike),float(row.Price),int(row.Cant),presition=presition)
        y = [sum(i) for i in zip (y,curve)]
    return x,y


def get_portfolio(user):
    path = os.getcwd()+os.sep+"data"+os.sep+"boards"+os.sep+user+"_board.xlsx"
    df = pd.read_excel(path)
    df.set_index("Opcion",inplace=True)
    return df


if __name__ == "__main__":
    x,y = get_finish_curve_sumed(get_portfolio("gtamani"))
    plt.plot(x,y)
    plt.plot(x,[0 for x in y],":",c="black")
    plt.grid()
    plt.show()

