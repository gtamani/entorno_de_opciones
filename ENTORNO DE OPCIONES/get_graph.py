import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
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
    """
    results = []
    T = days_to_opex/365

    for i in x:
        d1 = bs_d1(x,strike,interes,T,sigma)
        d2 = bs_d2(d1,sigma,T)
        bsch = get_blackscholes(d1,d2,x,strike,T,side)
        
        print("bsch: ",bsch)
        if side == "C":
            results.append((-prima + bsch)*cant)
        else:
            results.append((prima + bsch)*cant)
    """
    return x, [0 for x in x]

def get_curves_sumed(query,presition=100):
    y,y2 = [0]*presition,[0]*presition

    print("QUERY: ",query)
    if any(query):
        opex = query[0][-1]
        faltan = datetime.today() - opex
        days_to_opex = faltan.days
        

        for d in query:
            opex = d[4]
            x,curve = get_finish_curve(d[0][3],float(d[1]),float(d[2]),cant= int(d[3]),presition=presition)
            x2,curve2 = get_teoric_curve(d[0][3],float(d[1]),float(d[2]),cant = int(d[3]), days_to_opex=days_to_opex,sigma=0.3,rate=0.35,presition=100)
            y = [sum(i) for i in zip (y,curve)]
            y2 = [sum(i) for i in zip (y2,curve2)]
        return x,y,y2
    return [0,10000],[-100,200],[0,0]


if __name__ == "__main__":
    pass

