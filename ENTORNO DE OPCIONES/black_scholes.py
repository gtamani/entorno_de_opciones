import numpy as np
from scipy.stats import norm
from math import sqrt

def N(d):
    """
    Probabilidad de que que la accion se posicione por debajo de "d" conforme a una distribución normal
    """
    return norm.cdf(d,0,1)

def get_blackscholes(spot,strike,days_to_opex,type = "C",sigma = 0.3,interes=0.4):
    """
    Cálculo teórico de valuación de opciones financieras.
    Parte del DataFrame.
    """
    #maturity
    T = days_to_opex/365
    d1 = (np.log(spot/strike) + (interes + sigma**2/2)*T)/(sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    #delta_c = N(d1)
    #vega = spot * delta_c * np.sqrt(T)
    try:
        if type == "C":
            price = spot * N(d1) - strike*np.exp(-interes*T) * N(d2)
        elif type == "V":
            price = strike * np.exp(-interes*T) * N(-d2) - spot*N(-d1)
        return round(price,2)#,d1,d2,vega
    except:
        return "Error"
"""
def vega(spot,strike,tiempo_al_vencimiento,interes,sigma):
    spot = float(spot)
    d1 = (np.log(spot/strike) + (interes + 0.5 * sigma**2)*tiempo_al_vencimiento)/(sigma*np.sqrt(tiempo_al_vencimiento))
    return spot * N(d1) * sqrt(tiempo_al_vencimiento)

def vi(spot,strike,tiempo_al_vencimiento,prima,type = "C",interes=0.35):
   
    ARREGLAR
    
    sigma_est = 0.5
    for i in range(100):
        sigma_est -= (get_blackscholes(spot,strike,tiempo_al_vencimiento,type,sigma_est,interes)-prima) / vega(spot,strike,tiempo_al_vencimiento,interes,sigma_est)
    #print(strike,round(sigma_est * 100,2))


    return round(sigma_est * 100,2)
"""

print(get_blackscholes(116,100,30,"C",sigma=0.3,interes=0.3))