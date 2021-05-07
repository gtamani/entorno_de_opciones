import numpy as np

lista = [("user","date"),("user","date"),("user","date")]

lista = np.array(lista).T.tolist()
print(lista)