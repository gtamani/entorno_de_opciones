import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
from black_scholes import *

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


def get_finish_curve(side,base,prima,cant=1,presition=100,subyascente=116):
    x = np.linspace(subyascente/1.5,subyascente*1.5,presition)
    if side == "C":
        return x,[call(i,base,prima,cant) for i in x]
    return x,[put(i,base,prima,cant) for i in x]

def get_teoric_curve(side,base,prima,days_to_opex,cant=1,sigma=0.3,rate=0.35,presition=100,subyascente=116):
    x = np.linspace(subyascente/1.5,subyascente*1.5,presition)
    if side == "C":
        return x, [(-prima + get_blackscholes(i,base,days_to_opex,side,sigma,rate))*cant for i in x]
    return x,[(prima + get_blackscholes(i,base,days_to_opex,side,sigma,rate))*cant for i in x]


def get_curves_sumed(df,presition=100):
    y,y2 = [0]*presition,[0]*presition
    for index,row in df.iterrows():
        x,curve = get_finish_curve(row.Side,float(row.Strike),float(row.Price),int(row.Cant),presition=presition)
        x2,curve2 = get_teoric_curve(row.Side,float(row.Strike),float(row.Price),days_to_opex=0,cant=1,sigma=0.3,rate=0.35,presition=100)
        y = [sum(i) for i in zip (y,curve)]
        y2 = [sum(i) for i in zip (y2,curve2)]
    return x,y,y2


def get_portfolio(user):
    path = os.getcwd()+os.sep+"data"+os.sep+"boards"+os.sep+user+"_board.xlsx"
    df = pd.read_excel(path)
    df.set_index("Opcion",inplace=True)
    return df

if __name__ == "__main__":
    x,y,y2 = get_curves_sumed(get_portfolio("gtamani"))
    """
    x,y = get_teoric_curve("V",120,3.4,days_to_opex=60,cant=1)
    x2,y2 = get_finish_curve("V",120,3.4,cant=1)
    """
    plt.plot(x,y)
    plt.plot(x,y2)
    plt.plot(x,[0 for x in y],":",c="black")
    plt.grid()
    plt.show()

