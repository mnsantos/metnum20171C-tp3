import numpy as np
from sklearn.metrics import mean_squared_error
from queries import *
from graphics import *
from geopy.distance import vincenty

def cml(filas, b):
	A = np.vstack(filas)
	coeficients = np.linalg.lstsq(A, b)[0]
	return coeficients.tolist()

def mse(featuresList, coeficients, actualValues):
	predictions = [ np.dot(features, coeficients) for features in featuresList ]
	return mean_squared_error(actualValues, predictions)

def distancia(lat1,long1,lat2,long2):
	par1 = (lat1, long1)
	par2 = (lat2, long2)
	return vincenty(par1, par2).miles * 1.60934

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

def cross_validation_ciudades(anios_train, anios_test, ciudades, ciudad_objetivo, c):

	cities = ciudades_anios(ciudades, anios_train, c)
	ciudad_obj = ciudades_anios([ciudad_objetivo], anios_train, c)

	#print cities
	b = [c_anio[0] for c_anio in ciudad_obj]
	A = [(ciudad[0] / distancia(ciudad[1],ciudad[2],ciudad_obj[0][1],ciudad_obj[0][2])) for ciudad in cities]
	#A = [ciudad[0] for ciudad in cities]

	print A
	print b
	coeficientes = cml(A, b)

	print coeficientes
	anios = anios_train + anios_test

	ciudades_test = ciudades_anios(ciudades, anios_test, c)
	ciudades_test = [(ciudad[0] / distancia(ciudad[1],ciudad[2],ciudad_obj[0][1],ciudad_obj[0][2])) for ciudad in ciudades_test]
	#ciudades_test = [ciudad[0] for ciudad in ciudades_test]
	ciudad_objetivo_test = ciudades_anios([ciudad_objetivo], anios_test, c)
	temperaturas_ciudad_objetivo_test = [c_anio[0] for c_anio in ciudad_objetivo_test]

	ciudades_as = A + ciudades_test 
	#print temperaturas_paises_anios
	temperaturas_ciudad_objetivo_anios = b + temperaturas_ciudad_objetivo_test
	#print temperaturas_global_anios

	predicciones = []
	for ci in ciudades_as:
		prediccion = np.dot(ci, coeficientes)
		predicciones.append(prediccion)
	#print predicciones
	#print temperaturas_global_anios
	graficar_lineas(temperaturas_ciudad_objetivo_anios, predicciones, anios, 'Temperatura ciudad real')

conn = lite.connect("temperaturas.db")
c = conn.cursor()
# paises = ['Argentina', 'Guatemala', 'Canada', 'Congo', 'Poland', 'China', 'Australia']
# cross_validation_paises_estacion_global([1980,1981,1982,1983,1983,1984,1985,1986,1987,1988,1989,1990,1991,1992,1993,1994],paises,[1995,1996,1997,1998,1999,2000,2001,2002],c)
# cross_validation_paises_promedio_global([1980,1981,1982,1983,1983,1984,1985,1986,1987,1988,1989,1990,1991,1992,1993,1994],paises,[1995,1996,1997,1998,1999,2000,2001,2002],c)

cross_validation_ciudades([1980,1981,1982,1982,1983,1984,1985,1986,1987,1988,1989,1990,1991],[1992,1993,1994,1995,1996],['Tucuman'],'Santiago_Del_Estero',c)
# print ciudades_de_pais('Argentina', [1990], c)
# newport_ri = (41.49008, -71.312796)
# cleveland_oh = (41.499498, -81.695391)
# print(vincenty(newport_ri, cleveland_oh).miles)

# c.execute("SELECT * FROM Paises")
# rows = c.fetchall()
# for row in rows:
# 	print row