import numpy as np
from scipy.stats import norm
from math import sqrt
import time

def N(d):
    """
    Probabilidad de que que la accion se posicione por debajo de "d" conforme a una distribución normal
    """
    return norm.cdf(d,0,1)

def bs_d1(spot,strike,interes,T,sigma):
    return (np.log(spot/strike) + (interes + sigma**2/2)*T)/(sigma*np.sqrt(T))

def bs_d2(d1,sigma,T):
    return d1 - sigma*np.sqrt(T)

def get_blackscholes(d1,d2,spot,strike,T,type = "C",interes=0.4):
    """
    Cálculo teórico de valuación de opciones financieras.
    Parte del DataFrame.
    """

    if type == "C":
        price = spot * N(d1) - strike*np.exp(-interes*T) * N(d2)
    elif type == "V":
        price = strike * np.exp(-interes*T) * N(-d2) - spot*N(-d1)
    return price#,bs_d1,bs_d2,vega
    

def vi():
    pass

def N_gamma(d):
    return (1/np.sqrt(2*np.pi))*np.exp((-d**2)/2)

def get_gamma(d,spot,sigma,T):
    return N_gamma(d)/(spot*sigma*np.sqrt(T))

def tetha1(spot,bs_d1,sigma,T):
    return -((spot*N(bs_d1)*sigma)/(2*np.sqrt(T)))

def tetha2(interes,strike,T):
    return (interes*strike*np.exp(-interes*T))

def theta_call(spot,sigma,T,interes,strike,bs_d1,d2):
    return tetha1(spot,bs_d1,sigma,T)   -  tetha2(interes,strike,T)   *  (N(d2))

def theta_put(spot,sigma,T,interes,strike,bs_d1,d2):
    return tetha1(spot,bs_d1,sigma,T)  + tetha2(interes,strike,T) * N(-d2)

def get_vega(spot,T,d1):
    return (spot*np.sqrt(T)*N_gamma(d1))/100

def get_greeks(spot,strike,interes,T,sigma,side):

    d1 = bs_d1(spot,strike,interes,T,sigma)
    d2 = bs_d2(d1,sigma,T)

    bsch = get_blackscholes(d1,d2,spot,strike,T,side,interes)
    if side == "C":
        delta = N(d1)
        theta = (theta_call(spot,sigma,T,interes,strike,d1,d2)/365)
    else:
        delta = N(-d1)
        theta = theta_put(spot,sigma,T,interes,strike,d1,d2)/365
    gamma = get_gamma(d1,spot,sigma,T)
    vega = get_vega(spot,T,d1)
    vi = 0
    return {"bsch":bsch,"delta":delta,"gamma":gamma,"theta":theta,"vega":vega,"vi":vi}

"""
spot = 123
strike = 150
T = 40/365
sigma = 0.40 
interes = 0.3

t0 = time.time()
print(get_greeks(spot,strike,interes,T,sigma,"C"))
t1 = time.time()
print(t1-t0)
"""
