import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

desde = 0
largo = 2

actualizacion = 0
inte = 0
x = np.linspace(0,largo,501)

#Configuraciones
x_data,y_data = list(),list()
fig,ax = plt.subplots()
ax.set_xlim(desde,largo)
ax.set_ylim(0,largo)
line, = ax.plot(0,0)

def seno(x):
    return x**2

def integral(puntos,actualizacion):
    global desde, largo
    ancho_rect = 0
    extremos = 0
    suma = 0
    if actualizacion > 0:
        extremos = puntos[0]+puntos[-1]
        ancho_rect = (largo - desde) / actualizacion
    if actualizacion > 1:
        for i in range(1,len(puntos)-1):
            suma += (puntos[i]*2)
            #print("Medio pos {}: {}".format(i,puntos[i]))

    integral = (extremos+suma)*(ancho_rect/2)

    return integral



def trapecio_multiple(data):
    global largo,x_data,y_data,actualizacion

    #print(data)
    if data != 0:
        x_data = np.linspace(0,largo,int(data))
        y_data = seno(x_data)


    print(actualizacion," trapecio(s)")
    #print(x_data)
    #print(y_data)
    inte = ((largo**3)/3)
    inte2 = integral(y_data,actualizacion)
    print("Integral simbolica: ",round(inte2,5),"Integral exacta: ",round(inte,5),"Error:",(inte2-inte))

    #(ancho rect/2)*[1 vez y[1],1 vez y[n], 2 veces el medio]

    line.set_xdata(x_data)
    line.set_ydata(y_data)
    plt.title("Método de {} trapecios".format(actualizacion))
    if data > 0:
        actualizacion += 1
    print()
    return line,


animation = FuncAnimation(fig,func=trapecio_multiple,frames=np.linspace(0,100,101),interval=500)
plt.plot(x,seno(x))
plt.title("Método de {} trapecios".format(actualizacion))


plt.show()