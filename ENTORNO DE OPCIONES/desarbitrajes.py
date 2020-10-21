import logging

logging.basicConfig(level=logging.INFO,format=" [%(levelname)s] (%(threadName)-s) %(message)s ")


def main(side, opciones):
    muestra = [opciones[i] for i in range(len(opciones)) if opciones[i].side == side and opciones[i].prima != 0]
    spread(muestra)
    condor(muestra,side)
    butterfly(muestra,side)


def spread(muestra):
    for i in range(len(muestra)):  # Oportunidad de Spread
        try:
            dif_base = abs(muestra[i].base - muestra[i - 1].base)
            dif_prima = abs(muestra[i].prima - muestra[i - 1].prima)
            costo = (muestra[i-1].prima - muestra[i].prima) * 100 - (muestra[i].prima + muestra[i - 1].prima)
        except:
            pass
        if dif_base < dif_prima:
            logging.info("DESARBITRAJE SPREAD. Bases: {} y {}. Neto de comisiones: {} ".format(muestra[i].base,
                                                                                          muestra[i - 1].base,
                                                                                        costo))

def condor(muestra,side):
    punta_izq = 0
    ancho = 1
    while ancho < len(muestra) / 3:  # Oportunidad de Condor
        acc = [muestra[punta_izq + ancho * x] for x in range(4)]
        if acc[1].base - acc[0].base == acc[2].base - acc[1].base == acc[3].base - acc[2].base:
            costo = (-acc[0].prima + acc[1].prima + acc[2].prima - acc[3].prima) * 100
            prima = sum([x.prima for x in acc])
            if costo > prima:
                logging.info("DESARBITRAJE {}_CONDOR. Bases: {} {} {} {} . Neto de comisiones: {}".format(side, acc[0].base,
                                                                                                   acc[1].base,
                                                                                                   acc[2].base,
                                                                                                   acc[3].base,
                                                                                                   round(costo - prima,2)))
        punta_izq += 1
        if punta_izq + ancho * 3 >= len(muestra):
            ancho += 1
            punta_izq = 0


def butterfly(muestra,side):
    punta_izq = 0
    ancho = 1
    while ancho < len(muestra) / 2:  # Oportunidad de Condor
        acc = [muestra[punta_izq + ancho * x] for x in range(3)]
        if acc[1].base - acc[0].base == acc[2].base - acc[1].base:
            costo = (-acc[0].prima + 2 * acc[1].prima - acc[2].prima) * 100
            prima = sum([x.prima for x in acc])
            if costo > prima:
                logging.info("DESARBITRAJE {}_BUTTERFLY. Bases: {} {} {} . Neto de comisiones: {}".format(side, acc[0].base,
                                                                                                   acc[1].base,
                                                                                                   acc[2].base,
                                                                                                   round(costo - prima,
                                                                                                         2)))
        punta_izq += 1
        if punta_izq + ancho * 2 >= len(muestra):
            ancho += 1
            punta_izq = 0