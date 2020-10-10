import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

x = np.linspace(0,50,200)
x_data,y_data = list(),list()

fig,ax = plt.subplots()
ax.set_xlim(0,50) # Dominio de x
ax.set_ylim(-2,2) # Hasta donde va en y
line, = ax.plot(10,10)

update = 0


def animation_frame(i):
    #Actualizamos los nuevos puntos
    global update
    if update < 200:
        x_data.append(i)#
    y_data.append(np.sin(i))

    line.set_xdata(x_data)
    line.set_ydata(y_data)
    update += 1
    if update > 200:
        #x_data.pop(0)
        y_data.pop(0)
    #print(update)
    #print(x_data)
    #print(y_data)
    #print()

    return line,

"""
class matplotlib.animation.FuncAnimation(fig, func, frames=None, init_func=None, fargs=None,
save_count=None, *, cache_frame_data=True, **kwargs)[source]
"""

animation = FuncAnimation(fig, func=animation_frame,frames = x,interval=10)
plt.plot(x,(x/(50/4))-2)
plt.title("Combinando gráfico estático y dinámico")
plt.show()
