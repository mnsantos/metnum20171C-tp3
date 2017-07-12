#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from sklearn.metrics import mean_squared_error
from queries import *
#import geocoder
from graphics import *
import math
from sklearn.model_selection import KFold
#from geopy.distance import vincenty

def cml(filas, b):
	A = np.vstack(filas)
	#print A, b
	coeficients = np.linalg.lstsq(A, b)[0]
	return coeficients.tolist()

def mse(actualValues, predictions):
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

def cross_validation_paises_promedio_global_v2(anios_train_inicio, anios_train_fin, anios_test_inicio, anios_test_fin, paises, c):
	anios = range(anios_train_inicio, anios_train_fin+1)

	A = temperaturas_promedio_anios(paises, anios, c)
	b = temperaturas_global(anios, c)
	coeficientes = cml(A, b)
	print coeficientes

	anios_test = range(anios_test_inicio, anios_test_fin+1)
	anios = anios + anios_test

	temperaturas_paises_test = temperaturas_promedio_anios(paises, anios_test, c)
	temperaturas_global_test = temperaturas_global(anios_test, c)

	temperaturas_paises_anios = np.vstack((A, temperaturas_paises_test))
	# #print temperaturas_paises_anios
	temperaturas_global_anios = np.vstack((b, temperaturas_global_test))
	# #print temperaturas_global_anios

	for temp in temperaturas_paises_anios:
		prediccion = np.dot(temp, coeficientes)
		try:
			predicciones
		except NameError:
			predicciones = prediccion
		else:
			predicciones = np.vstack((predicciones, prediccion))
	# #print predicciones
	# #print temperaturas_global_anios
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

def cross_validation_ciudades_meses_v2(anios_train_inicio, anios_train_fin, anios_test_inicio, anios_test_fin, ciudades, ciudad_objetivo, c):

	A = ciudades_anios_v2(ciudades, anios_train_inicio, anios_train_fin, c)
	#A = np.sin(A)
	b = ciudades_anios_v2([ciudad_objetivo], anios_train_inicio, anios_train_fin, c)

	##print cities
	#b = [c_anio[0] for c_anio in ciudad_obj]
	#A = [(ciudad[0] / distancia(ciudad[1],ciudad[2],ciudad_obj[0][1],ciudad_obj[0][2])) for ciudad in cities]
	##A = [ciudad[0] for ciudad in cities]

	#print A.shape
	#print b.shape
	coeficientes = cml(A, b)

	print coeficientes
	#print len(coeficientes)
	anios = range(anios_train_inicio, anios_train_fin+1)
	anios = anios + range(anios_test_inicio, anios_test_fin+1)
	ciudades_test = ciudades_anios_v2(ciudades, anios_test_inicio, anios_test_fin, c)
	#ciudades_test = np.sin(ciudades_test)
	#ciudades_test = [(ciudad[0] / distancia(ciudad[1],ciudad[2],ciudad_obj[0][1],ciudad_obj[0][2])) for ciudad in ciudades_test]
	##ciudades_test = [ciudad[0] for ciudad in ciudades_test]
	ciudad_objetivo_test = ciudades_anios_v2([ciudad_objetivo], anios_test_inicio, anios_test_fin, c)
	#temperaturas_ciudad_objetivo_test = [c_anio[0] for c_anio in ciudad_objetivo_test]
	
	#print A.shape, ciudades_test.shape
	ciudades_as = np.vstack((A, ciudades_test))
	##print temperaturas_paises_anios

	temperaturas_ciudad_objetivo_anios = np.vstack((b, ciudad_objetivo_test)) 
	##print temperaturas_global_anios
	for ci in ciudades_as:
		prediccion = np.dot(ci, coeficientes)
		try:
			predicciones
		except NameError:
			predicciones = prediccion
		else:
			predicciones = np.vstack((predicciones, prediccion))
	#print predicciones.shape
	#print temperaturas_ciudad_objetivo_anios.shape
	#print len(todos_los_meses_de(anios))
	fechas = todos_los_meses_de(anios)
	labels = []
	for fecha in fechas:
		label = fecha[0:-9]
		labels.append(label)
	print labels
	graficar_lineas(temperaturas_ciudad_objetivo_anios, predicciones, labels, 'Temperatura ciudad real')

def cross_validation_anios_global(anios_train, anios_test, grado):

	#print anios_train, anios_test, grado

	temperaturas_globales_train = temperaturas_global(anios_train, c)

	#print temperaturas_globales_train

	#fs = [pol_grado_n(grado,x) for x in anios_train]
	#fs = [pol_grado_n(grado,x) + [math.sin(x), math.cos(x)] for x in anios_train]
	fs = [pol_grado_n(grado,x) + [math.cos(x)] for x in anios_train]
	#fs = [[math.sin(x), math.cos(x), 1] for x in anios_train]
	#fs = [[math.sin(x), 1] for x in anios_train]
	#fs = [[math.cos(x), 1] for x in anios_train]
	coeficientes = cml(fs, temperaturas_globales_train)


	#print coeficientes
	predicciones_train = []
	predicciones_test = []
	predicciones = []
	anios = np.concatenate([anios_train, anios_test])
	for anio in anios:

		#print pol_grado_n(grado,anio)
		#prediccion = np.dot(pol_grado_n(grado,anio), coeficientes)
		#prediccion = np.dot(pol_grado_n(grado,anio) + [math.sin(anio), math.cos(anio)], coeficientes)
		prediccion = np.dot(pol_grado_n(grado,anio) + [math.cos(anio)], coeficientes)
		#prediccion = np.dot([math.sin(anio), math.cos(anio), 1], coeficientes)
		#prediccion = np.dot([math.sin(anio), 1], coeficientes)
		#prediccion = np.dot([math.cos(anio), 1], coeficientes)
		if (anio in anios_train):
			predicciones_train.append(prediccion)
		else:
			predicciones_test.append(prediccion)
		predicciones.append(prediccion)

	temperaturas_globales_test = temperaturas_global(anios_test, c)
	temperaturas_globales = temperaturas_globales_train + temperaturas_globales_test

	graficar_lineas(temperaturas_globales, predicciones_train, predicciones_test, anios, 'Temperatura global real', 'aproximacion.png')
	return mse(temperaturas_globales, predicciones)

def cross_validation(fechas, splits, functionToRun, args):
	fechas = np.array(fechas)
	kf = KFold(n_splits=splits)
	kf.get_n_splits(fechas)
	mse_list = []
	for train_index, test_index in kf.split(fechas): 
		#print("TRAIN:", train_index, "TEST:", test_index)
		fechas_train, fechas_test = fechas[train_index], fechas[test_index]
		mse = perform(functionToRun, fechas_train, fechas_test, args)
		mse_list.append(mse)
	#print mse_list
	return sum(mse_list)/len(mse_list)

def buscar_mejor_grado(anios_train, anios_test):
	min = cross_validation_anios_global(anios_train, anios_test, 1)
	grado_min = 1
	print grado_min, min
	for grado in range(2,80):
		mse = cross_validation_anios_global(anios_train, anios_test, grado)
		print grado, mse
		if (mse < min):
			min = mse
			grado_min = grado
	return grado_min

def perform(fun, *args):
    return fun(*args)

def pol_grado_n(n, x):
	return [x ** i for i in range(0,n+1)] 

def anios_vs_tempGlobal(c):
	anios = anios_global(c)
	temperaturas_globales = temperaturas_global(anios, c)
	graficar(anios, temperaturas_globales, "Años".decode('utf-8'), "Temperatura global", "anios_vs_tempGlobal")

def aproximacion_altura_dist_latitud(ciudad, fecha, c):
#def aproximacion_altura_dist_latitud(anios_train_inicio, anios_train_fin, anios_test_inicio, anios_test_fin, c):
# Ciudad, altura, distancia_al_mar, latitud, longitud
# (u'Cochabamba', [2558, 459, -16.87, -66.98])
# (u'Cordoba', [177, 708, -31.35, -64.08])
# (u'Corrientes', [52, 0, -28.13, -59.09])
# (u'Helsinki', [0, 0, 60.27, 25.95])
# (u'Jujuy', [1495, 533, -24.92, -65.62])
# (u'Lima', [202, 0, -12.05, -77.26])
# (u'Lusaka', [1123, 330, -15.27, 27.5])
# (u'Moscow', [151, 900, 55.45, 36.85])
# (u'New_York', [10, 0, 40.99, -74.56])
# (u'Riyadh', [571, 400, 24.92, 46.11])
# (u'Santiago_Del_Estero', [187, 658, -28.13, -64.55])
# (u'Sydney', [0, 0, -34.56, 151.78])

	ciudades = ['Cochabamba','Cordoba','Helsinki','Jujuy','Lima','Lusaka','Moscow', 'New_York','Riyadh','Santiago_Del_Estero','Sydney']
	#fecha = '2000-01-01 00:00:00'

	A = np.array([[2558, 459, -16.87],
		[177, 708, -31.35],
		[0, 0, 60.27],
		[1495, 533, -24.92],
		[202, 0, -12.05],
		[1123, 330, -15.27],
		[151, 900, 55.45],
		[10, 0, 40.99],
		[571, 400, 24.92],
		[187, 658, -28.13],
		[0, 0, -34.56]])
	
	b = ciudades_fecha(ciudades, fecha, c).transpose()

	coeficientes = cml(A, b)

	data_ciudad = np.array([52, 920, -28.13])
	temp_real = ciudades_fecha([ciudad], fecha, c)
	temp_aproximada = np.dot(data_ciudad,coeficientes)

#	temp_aproximada = np.dot(A,coeficientes)
#	for i in range(0,b.size):
#		print ciudades[i], b[i], temp_aproximada[i]
#	print np.sqrt(mse(b, temp_aproximada))

	print ciudad, temp_real, temp_aproximada


conn = lite.connect("temperaturas.db")
c = conn.cursor()

anios = anios_global(c)
#anios = anios[len(anios)/2:-1]
#print anios
#anios_train = anios[len(anios)/2:(len(anios)/2)+(len(anios)/4)]
#anios_train = anios[0: (len(anios)/2)]
#print anios_train
#anios_test = anios[(len(anios)/2)+(len(anios)/4):-1]
#anios_test = anios[(len(anios)/2):-1]
#print anios_test
#buscar_mejor_grado(anios_train, anios_test)
#print cross_validation_anios_global(anios_train, anios_test, 1)
# paises = ['Argentina', 'Guatemala', 'Canada', 'Congo', 'Poland', 'China', 'Australia']
# cross_validation_paises_estacion_global([1980,1981,1982,1983,1983,1984,1985,1986,1987,1988,1989,1990,1991,1992,1993,1994],paises,[1995,1996,1997,1998,1999,2000,2001,2002],c)



#Aca estan los tres puntos del TP funcionando bien.
#print cross_validation_anios_global(anios[len(anios)/2:(len(anios)/2)+(len(anios)/4)], anios[(len(anios)/2)+(len(anios)/4):-1], 2)
#paises = ['Argentina', 'Canada', 'South_Africa', 'Norway','Russia', 'China', 'Australia', 'Japan']
#cross_validation_paises_promedio_global_v2(1980,1995,1996,2012,paises,c)
# cross_validation_ciudades_meses_v2(1980,1981,1992,1993,['Canberra', 'Hobart', 'Sydney'],'Santiago_Del_Estero',c)
#aproximacion_altura_dist_latitud('Corrientes', '1990-04-01 00:00:00', c)

# print ciudades_de_pais('Argentina', [1990], c)
# newport_ri = (41.49008, -71.312796)
# cleveland_oh = (41.499498, -81.695391)
# print(vincenty(newport_ri, cleveland_oh).miles)

# c.execute("SELECT * FROM Paises")
# rows = c.fetchall()
# for row in rows:
# 	print row

#anios_vs_tempGlobal(c)


# g = geocoder.elevation('[-34.593213, -58.437835]')
# print (g.meters)

print cross_validation(anios, 2, cross_validation_anios_global, 1)
