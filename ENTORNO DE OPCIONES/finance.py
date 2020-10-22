import numpy as np
from scipy.stats import norm

def N(d):
    return norm.cdf(d,0,1)

def calculo_blackScholes(spot,strike,tiempo_al_vencimiento,type = "C",sigma = 0.3,interes=0.3):
    """
    Cálculo teórico de valuación de opciones financieras.
    Parte del DataFrame.
    """
    #Maturity = tiempo al venc/365

    d1 = (np.log(spot/strike) + (interes + sigma**2/2)*tiempo_al_vencimiento)/(sigma*np.sqrt(tiempo_al_vencimiento))
    d2 = d1 - sigma*np.sqrt(tiempo_al_vencimiento)
    vega = spot * N(d1) * np.sqrt(tiempo_al_vencimiento)


    try:
        if type == "C":
            price = spot * N(d1) - strike*np.exp(-interes*tiempo_al_vencimiento) * N(d2)
        elif type == "V":
            price = strike * np.exp(-interes*tiempo_al_vencimiento) * N(-d2) - spot*N(-d1)

        return round(price,2)#,d1,d2,vega
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

def graph(details,var_x,opex=0):
    """
    [RESULTADO AL VENCIMIENTO]
    Calcula los valores de Y para la suma de todos los activos en cartera.
    Valores que muestra el gráfico en pantalla
    """
    #print("SUMA: ",suma)
    #print("NEW: ",new)


    al_vto, teorico = [0 for x in var_x],[0 for x in var_x]

    print("DETAILSSSSSSSSSS\n",details,"VAR_X",var_x)

    for i in details:
        #print(i[0], i[1], i[2], i[3], i[4])

        print(i)
        if len(i) == 3:
            print("ACCION")
            curva_vto = [(x-i[1]) * i[2] for x in var_x]
            curva_teorico = [(x - i[1]) * i[2] for x in var_x]
        else:
            print("OPCION")
            print(var_x[1],var_x[2],var_x[3],i[1],opex,i[0])
            curva_vto = y_graph(i[0],float(i[1]),i[2],i[3],var_x)
            curva_teorico = [(calculo_blackScholes(var_x[z],int(i[1]),opex,i[0]) - i[4]) * i[3] * 100 if i[3] >= 0 else
                             (i[4] + calculo_blackScholes(var_x[z],int(i[1]),opex,i[0])) * i[3] * 100 for z in range(len(al_vto))]
            print("teorico,curva",curva_teorico)
            print()


        for j in range(len(curva_vto)):
            al_vto[j] += curva_vto[j]
            teorico[j] += curva_teorico[j]


    print(al_vto)
    print(teorico)



    return al_vto, teorico

def graph2():
    pass

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


#prima,d1,d2,vega = calculo_blackScholes(100,90,0.3287671233,"C",0.3,0.05)

#print(prima)
#print(d1,d2)
#print(N(d1),N(d2))
#print(N(-d1),N(-d2))
#print(vega)

#print(volatilidad_implicita(34,30,1,0.0001,2.724,0.5))