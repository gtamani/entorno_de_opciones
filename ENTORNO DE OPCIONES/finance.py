import numpy as np
from scipy.stats import norm

def calculo_blackScholes(spot,strike,tiempo_al_vencimiento,type = "C"):
    """
    Cálculo teórico de valuación de opciones financieras.
    Parte del DataFrame.
    """
    #Variables
    interes = 0.3
    sigma = 0.3



    #Cálculo de
    d1 = (np.log(spot/strike) + (interes + sigma**2/2)*tiempo_al_vencimiento)/(sigma*np.sqrt(tiempo_al_vencimiento))
    d2 = d1 - sigma*np.sqrt(tiempo_al_vencimiento)

    try:
        if type == "C":
            price = spot*norm.cdf(d1,0,1) - strike*np.exp(-interes*tiempo_al_vencimiento) \
                    * norm.cdf(d2,0,1)
        elif type == "V":
            price = strike*np.exp(-interes*tiempo_al_vencimiento)*norm.cdf(-d2,0,1)\
            - spot*norm.cdf(-d1,0,1)

        return round(price,2)
    except:
        return "Error"


def y_graph(side,base,prima,cant,x,lote=100):
    """
    Determina la curva de una opción, sea call/put comprado/lanzado
    """

    if side == "C":
        """
        compra True = comprar call (view alcista)
        compra False = lanzar call (view bajista)
        """
        if cant > 0:
            return [-prima * lote *cant if x <= base else round((x - (base+prima)) * lote * cant,2) for x in x ]
        return [prima * lote * -cant if x <= base else round(((base+prima) - x) * lote * -cant ,2)  for x in x ]

    else:
        """
        compra True = comprar put (view bajista)
        compra False = lanzar put (view alcista)
        """
        if cant > 0:
            return [-prima * lote * cant if x >= base else round(((base-prima) - x) * lote * cant,2) for x in x]
        return [prima * lote * -cant if x >= base else round((x - (base - prima)) * lote * -cant,2) for x in x]

def graph(details,x):
    """
    Calcula los valores de Y para la suma de todos los activos en cartera.
    Valores que muestra el gráfico en pantalla
    """
    #print("SUMA: ",suma)
    #print("NEW: ",new)

    suma = [0 for x in x]

    for i in details:
        print(i)
        for j in range(len(suma)):
            if len(i) == 3:
                suma[j] += [(x-i[1]) * i[2] for x in x][j]
            else:
                suma[j] += y_graph(i[0],float(i[1]),i[2],i[3],x)[j]
    print(suma)
    return suma

def tna_a_tea(tna,capitalize):
    """
    Transforma la tasa Nominal anual a su correspondiente Efectiva anual
    :param tna: Tasa TNA a transformar
    :param capitalize: Periodo de capitalización
    """
    times =(360/capitalize)
    tna /= times
    return (1 + tna) ** times

#print("Tasa Futuro enero DO: ",tna_a_tea(0.5111,105))
#print("Tasa Futuro octubre DO: ",tna_a_tea(0.3586,15))
#print("Tasa Futuro noviembre DO: ",tna_a_tea(0.4381,45))


