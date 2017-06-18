import numpy as np
from sklearn.metrics import mean_squared_error
from queries import *
from graphics import *

def cml(filas, b):
	A = np.vstack(filas)
	coeficients = np.linalg.lstsq(A, b)[0]
	return coeficients.tolist()

def mse(featuresList, coeficients, actualValues):
	predictions = [ np.dot(features, coeficients) for features in featuresList ]
	return mean_squared_error(actualValues, predictions)


def cross_validation_paises_estacion_global(anios_train, paises, anios_test, c):
	A = temperaturas_estacion_anios(paises, anios_train, c)
	#print A
	b = temperaturas_global(anios_train, c)
	#print len(b)
	coeficientes = cml(A, b)

	print coeficientes
	anios = anios_train + anios_test

	temperaturas_paises_test = temperaturas_estacion_anios(paises, anios_test, c)
	temperaturas_global_test = temperaturas_global(anios_test, c)

	temperaturas_paises_anios = A + temperaturas_paises_test 
	#print temperaturas_paises_anios
	temperaturas_global_anios = b + temperaturas_global_test
	#print temperaturas_global_anios

	predicciones = []
	for temp in temperaturas_paises_anios:
		prediccion = np.dot(temp, coeficientes)
		predicciones.append(prediccion)
	#print predicciones
	#print temperaturas_global_anios
	graficar_lineas(temperaturas_global_anios, predicciones, anios, 'Temperatura global real')

def cross_validation_paises_promedio_global(anios_train, paises, anios_test, c):
	A = temperaturas_promedio_anios(paises, anios_train, c)
	#print A
	b = temperaturas_global(anios_train, c)
	#print len(b)
	coeficientes = cml(A, b)

	print coeficientes
	anios = anios_train + anios_test

	temperaturas_paises_test = temperaturas_promedio_anios(paises, anios_test, c)
	temperaturas_global_test = temperaturas_global(anios_test, c)

	temperaturas_paises_anios = A + temperaturas_paises_test 
	#print temperaturas_paises_anios
	temperaturas_global_anios = b + temperaturas_global_test
	#print temperaturas_global_anios

	predicciones = []
	for temp in temperaturas_paises_anios:
		prediccion = np.dot(temp, coeficientes)
		predicciones.append(prediccion)
	#print predicciones
	#print temperaturas_global_anios
	graficar_lineas(temperaturas_global_anios, predicciones, anios, 'Temperatura global real')

conn = lite.connect("temperaturas.db")
c = conn.cursor()
paises = ['Argentina', 'Guatemala', 'Canada', 'Congo', 'Poland', 'China', 'Australia']
#cross_validation_paises_estacion_global([1980,1981,1982,1983,1983,1984,1985,1986,1987,1988,1989,1990,1991,1992,1993,1994],paises,[1995,1996,1997,1998,1999,2000,2001,2002],c)
cross_validation_paises_promedio_global([1980,1981,1982,1983,1983,1984,1985,1986,1987,1988,1989,1990,1991,1992,1993,1994],paises,[1995,1996,1997,1998,1999,2000,2001,2002],c)

# c.execute("SELECT * FROM Paises")
# rows = c.fetchall()
# for row in rows:
# 	print row