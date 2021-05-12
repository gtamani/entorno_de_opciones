**Índice**
1. [Pasos previos](#id1)
    * [Instalar los requerimientos](#id1-1)
    * [Obtener acceso a la API](#id1-2)
    * [Configurar el entorno](#id1-3)
3. [Como útilizarlo](#id2)
    * [Panel de opciones](#id2-1)
    * [Panel de gráfico](#id2-2)
    * [Configuraciones](#id2-3)
5. [Consideraciones](#id3)



# Entorno de opciones

En este entorno podes...
- Visualizar tenencia de opciones, así como el resultado teórico y al vencimiento para cada precio al OPEX
- Armado de estrategias
- Variables como Volatilidad implícita y griegas más relevantes (delta,gamma,theta,vega)
- Comprar y vender desde la app (Próximamente)


<div id='id1' />

# Antes de empezar
Hay una serie de pasos a seguir antes de podes usar la app y las enumero a continuación:


<div id='id1-1' />

* ##  Instalar los requerimientos

La app tiene una serie de dependencias que son necesarias que tengas instaladas a la hora de ejecutar el entorno de opciones.
Pero nada que una linea de código en la consola no pueda solucionar. En el cmd, ubicate en la carpeta del proyecto y tipea:

```
pip install -r requirements.txt
```

<div id='id1-2' />

* ## Obtener el acceso a la API

Definitivamente el punto más importante.  

Para disponer de información en tiempo real es necesario hacer periodicamente consultas del tipo API REST, ya sea para la informacion de la cotización de las opciones de determinado subyascente como de la información historica para el gráfico de volatilidad.

Al día de hoy en Argentina, no existe conexión websocket gratuita y de libre acceso, por lo cual decidí usar la única API con acceso en tiempo real a mercado BYMA: Invertir Online. 

Por ende, para poder realizar requests de BYMA primero es necesario tener una cuenta en Invertir Online y una vez abierta, pedirles que te habiliten para poder usar su API.

Esto es estrictamente necesario, por lo cual si no tenes las credenciales, no tienen ningún sentido que uses la app.

<div id='id1-3' />

* ## Configurar el entorno
Nada muy complicado.  

En el archivo de entorno ".env" introducimos nuestros datos. en forma de string. Pero tranquilos, es solo información necesaria para iniciar sesión y solicitar el token para poder realizar los requests (Pueden ver las funciones [aquí mismo.](../API_data.py)).

```
USER="my_IOL_user"
PASSWORD="my_IOL_password"
POSTGRESS_PASSWORD="my_posgres_password"
```
 El último campo es su clave para poder acceder a su base de datos PosgreSQL interna, necesaria para vincular tenencias, usuarios, opciones e historial.

 Luego, al ejecutar la app, automáticamente se añaden al archivo.

<div id='id2' />


# Cómo utilizarla

Este es un pantallazo general de la aplicación, en donde podemos ver dos secciones bien definidas: a la izquierda el panel de opciones en tiempo real y a la derecha los gráficos del maquetado de estrategias y de la volatilidad histórica del subyascente

![screen1](https://user-images.githubusercontent.com/72049315/118001242-ec4f2c80-b31c-11eb-9375-faa45db600a0.png)


<div id='id2-1' />

## Panel de opciones


De un lado, los calls del próximo opex, del otro lado los puts.
En rojo los Out of the money, en amarillos los At the money y en verde los In the money. 

En el panel no se muestran tenencia (para eso la pestaña "Tenencia"), sino que se muestran variables de analísis que pueden servirle al inversor y que no se muestran en los paneles tradicionales.

En primer lugar, la prima de la opción junto al valor teoríco del modelo de Black Scholes, y inmediatamente al lado, las cuatro griegas más importantes (delta, gamma, theta y vega) junto a la volatilidad implícita.

Todas estas variables son calculadas respecto a parametros, tales como "sigma" o "free-risk rate" que pueden ser configurados en el panel de opciones para mayor presición.

Abajo a la izquierda, un mini panel de compra/venta para el modelado de opciones. Seleccionas la opción a operar, la cantidady listo. Click en "Operar" y ya se muestra en el panel de gráfico

También se encuentra el botón "Actualizar" disponible sólo con actualización manual, para refrescar los datos.

![screen3](https://user-images.githubusercontent.com/72049315/118016156-73a39c80-b32b-11eb-91ee-22e57c2913a8.png)

<div id='id2-2' />

## Panel de Gráfico


Podemos ver dos gráficos a continuación, totalmente customizables.

Arriba vemos el armado de la estrategia o nuestra tenencia. Cada vez que se opera una opción vemos el resultado en este gráfico. Por lo cual es ideal para maquetar estrategias como bulls spread, condors, butterflys, para hacer tasa, etc, viendo así tanto el costo del armado como el resultado final (y teorico, si se configura) a distintos precios del subyascente al final del ejercicio. Se pueden establecer bandas de rango, hacer zoom, y otras configuraciones en "Settings".

El segundo gráfico muestra la volatilidad histórica del subyascente calculado sobre las últimas 40 ruedas sobre una data de 365 días (estos dos últimos parametros también customizables). Permite orientarnos y comparar las volatilidades implicitas de las opciones con el comportamiento histórico de la acción.

<div style="text-align:center;">
<img src="https://user-images.githubusercontent.com/72049315/118016185-7acaaa80-b32b-11eb-9bb8-efcff717766d.png" ></div>

<div id='id2-3' />

## Settings

Aquí algunas configuraciones bastante intuitivas pero por las cuales vale la pena algunas pequeñas aclaraciones.

Vemos el panel dividido en 5 secciones.

* Actualización manual/ automática

..Si bien no debería haber problemas con frecuencia de actualización cortas, si se quiere tener control sobre la cantidad de requests puede modificarse o incluso actualizar manualmente mediante el botón "Actualizar" del panel de opciones

* Accion subyascente

..Claro está que GGAL (Grupo Financiero Galicia) es la acción subyascente con mayor volumen en opciones, pero si así se quisiese, también es posible acceder a data de otras opciones.

* Gráfico de armado de posición

..Configuracion sobre la curva de resultado teorico (en la que influye el valor extrínseco de las opciones), rango a mostrar (%), presición de las curvas y bandas de rangos (cantidad y porcentaje respecto a la cotización del subyascente)

* Gráfico de Volatilidad Histórica

..Por default y como tope se obtiene data de los últimos 365 días, calculando la volatilidad implícita sobre las 50 ruedas anteriores.

* Parametros para el cálculo de variables teóricas y resultado teórico

..Sigma y volatilidad, influyentes en el cálculo de las letras griegas, valuación según el modelo de Black scholes y la curva de valor explicito


<div style="text-align:center;">
<img src="https://user-images.githubusercontent.com/72049315/118001252-efe2b380-b31c-11eb-9780-471fbf036eed.png" ></div>

<div id='id3' />


# Algunas aclaraciones


Cada servidor pone sus propias limitaciones tanto a la frecuencia de las consultas a realizar como en la gratuidad de las mismas.

En el caso exclusivo de <b>IOL</b> y a la fecha de <b>hoy</b> las condiciones son las que voy a explicar a continuación. Eso no quiere decir que en un futuro cambie, por lo que aconsejo que le manden un mensaje (si es que no les explicaron todavía, como suelen hacer) a la empresa.

Tenes acceso a 20.000 consultas por mes totalmente gratis. A partir de la consulta 20.001, te descuentan sólo $500 que se usan a cuenta de comisiones. Empieza otro mes y se renueva el contador.

De esta forma se aseguran que no utilices las consultas sin operar desde el broker, pero es un número abismal de consultas para el funcionamiento de la aplicación. Incluso usandolo todos los días en que el mercado abre y a una frecuencia de actualización de 5 minutos, te sobran consultas.



