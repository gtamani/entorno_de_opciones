import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import os
from black_scholes import *

def call(x,base,prima,cant,lote = 100):
    if x < base:
        return -prima*cant*lote
    else:
        return ((x-base)-prima)*cant*lote

def put(x,base,prima,cant,lote = 100):
    if x > base:
        return -prima*cant*lote
    else:
        return (-(x-base)-prima)*cant*lote


def get_finish_curve(side,base,prima,cant=1,presition=100,subyascente=116):
    x = np.linspace(subyascente/1.5,subyascente*1.5,presition)
    if side == "C":
        print(x,[call(i,base,prima,cant) for i in x])
        return x,[call(i,base,prima,cant) for i in x]
    return x,[put(i,base,prima,cant) for i in x]


def get_teoric_curve(side,base,prima,days_to_opex,cant=1,sigma=0.3,rate=0.35,presition=100,subyascente=116,lote=100):
    x = np.linspace(subyascente/1.5,subyascente*1.5,presition)
    
    results = []
    T = days_to_opex/365

    for i in x:
        print("PARAMETROSSS",i,base,prima,T,cant,sigma,rate,presition,subyascente)
        d1 = bs_d1(i,base,rate,T,sigma)
        d2 = bs_d2(d1,sigma,T)
        bsch = get_blackscholes(d1,d2,i,base,T,side,rate)
        
        if side == "C":
            print((-prima + bsch)*100)
            results.append((-prima + bsch)*100)
        else:
            results.append((prima + bsch)*100)
    
    return x, results

def get_curves_sumed(query,presition=100):
    y,y2 = [0]*presition,[0]*presition

    print("QUERY: ",query)
    if any(query):
        opex = query[0][-1]
        faltan = opex - datetime.today()
        days_to_opex = faltan.days
        

        for d in query:
            opex = d[4]
            x,y = get_finish_curve(d[0][3],float(d[1]),float(d[2]),cant= int(d[3]),presition=presition)
            x,y2 = get_teoric_curve(d[0][3],float(d[1]),float(d[2]),cant = int(d[3]), days_to_opex=days_to_opex,sigma=0.3,rate=0.35,presition=presition)
        return x,y,y2
    return np.nan,np.nan,np.nan


if __name__ == "__main__":
    pass

