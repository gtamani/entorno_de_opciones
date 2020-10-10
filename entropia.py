import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random

x_data,y_data,y_data2,y_data3 = list(),list(),list(),list()
last = 40000
suma_50,suma_200 = 40000,40000
media_50,media_200 = 40000,40000
alcista = True

fig,ax = plt.subplots()
ax.set_xlim(0,500)
ax.set_ylim(20000,60000)
line, = ax.plot(0,0)
line2, = ax.plot(0,0)
line3, = ax.plot(0,0)

def precios(i):
    global last,media_50,suma_50,media_200,suma_200,alcista
    i += 1
    if i <= 500:
        x_data.append(i)
    if i > 500:
        y_data.pop(0)
        y_data2.pop(0)
        y_data3.pop(0)

    if i % 200 == 0:
        if alcista:
            alcista = False
        else:
            alcista = True

    if alcista:
        last += random.choice([-500,-400,-300,-200,-100,50,100,100,150,200,300,400,500])
    else:
        last += random.choice([-500, -400, -300,-150,-100,-100 -200,-50, -100, 100, 200, 300, 400, 500])


    y_data.append(last)



    if len(y_data) < 50:
        suma_50 += last
        media_50 = None
    else:
        suma_50 -= y_data[-50]
        suma_50 += last
        media_50 = suma_50/50

    if len(y_data) < 200:
        suma_200 += last
        media_200 = None
    else:
        suma_200 -= y_data[-200]
        suma_200 += last
        media_200 = suma_200/200


    y_data2.append(media_50)
    y_data3.append(media_200)

    print(len(x_data),i,alcista)




    line.set_xdata(x_data)
    line.set_ydata(y_data)
    line2.set_xdata(x_data)
    line2.set_ydata(y_data2)
    line3.set_xdata(x_data)
    line3.set_ydata(y_data3)
    return line, line2, line3


animation = FuncAnimation(fig,func=precios,interval=10)

plt.title("MERVAL EN PESOS CROCANTES")
plt.show()
