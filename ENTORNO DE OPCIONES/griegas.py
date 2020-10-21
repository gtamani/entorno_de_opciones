def delta():
    pass

def gamma():
    pass

def vega(spot,strike,tiempo_al_vencimiento,interes,sigma):
    spot = float(spot)
    d1 = (np.log(spot/strike) + (interes + 0.5 * sigma**2)*tiempo_al_vencimiento)/(sigma*np.sqrt(tiempo_al_vencimiento))
    vega = spot* N(d1)*sqrt(tiempo_al_vencimiento)



    return vega