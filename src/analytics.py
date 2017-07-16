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
	#print actualValues, predictions
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

def cross_validation_paises_promedio_global(anios_train, anios_test, paises, graficar=False):
	print anios_train, anios_test, paises

	A = temperaturas_promedio_anios(paises, anios_train, c)
	#A = temperaturas_anios_train
	#print A
	b = temperaturas_global(anios_train, c)
	#print len(b)
	coeficientes = cml(A, b)

	#print coeficientes
	anios = np.concatenate([anios_train, anios_test])

	temperaturas_paises_test = temperaturas_promedio_anios(paises, anios_test, c)
	#temperaturas_paises_test = temperaturas_anios_test
	temperaturas_global_test = temperaturas_global(anios_test, c)

	temperaturas_paises_anios = A + temperaturas_paises_test 
	#print temperaturas_paises_anios
	temperaturas_global_anios = b + temperaturas_global_test
	#print temperaturas_global_anios

	predicciones = []
	predicciones_train = []
	predicciones_test = []
	for (temp, anio) in zip(temperaturas_paises_anios, anios):
		prediccion = np.dot(temp, coeficientes)
		if (anio in anios_train):
			predicciones_train.append(prediccion)
		else:
			predicciones_test.append(prediccion)
		predicciones.append(prediccion)
	#print predicciones
	#print temperaturas_global_anios

	if graficar and anios_test[-1] == 2012 :
		graficar_lineas(temperaturas_global_anios, predicciones_train, predicciones_test, anios, 'Temperatura global real', 'aproximacion.png')
	return mse(temperaturas_global_test, predicciones_test) 

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

def cross_validation_anios_global(anios_train, anios_test, metodo, grado_pol, grado_pol_tri, graficar=False):

	#print anios_train, anios_test, grado_pol, grado_pol_tri

	temperaturas_globales_train = temperaturas_global(anios_train, c)

	#print temperaturas_globales_train

	fs = [metodo_anios_global(metodo, grado_pol, grado_pol_tri, anio) for anio in anios_train]
	coeficientes = cml(fs, temperaturas_globales_train)


	#print fs
	#print coeficientes
	predicciones_train = []
	predicciones_test = []
	predicciones = []
	anios = np.concatenate([anios_train, anios_test])
	for anio in anios:
		prediccion = np.dot(metodo_anios_global(metodo, grado_pol, grado_pol_tri, anio), coeficientes)

		if (anio in anios_train):
			predicciones_train.append(prediccion)
		else:
			predicciones_test.append(prediccion)
		predicciones.append(prediccion)

	temperaturas_globales_test = temperaturas_global(anios_test, c)
	temperaturas_globales = temperaturas_globales_train + temperaturas_globales_test

	if graficar and anios_test[-1] == 2012 :
		graficar_lineas(temperaturas_globales, predicciones_train, predicciones_test, anios, 'Temperatura global real', 'aproximacion.png')
	return mse(temperaturas_globales_test, predicciones_test)

def cross_validation(fechas, splits, functionToRun, args):
	fechas = np.array(fechas)
	kf = KFold(n_splits=splits)
	kf.get_n_splits(fechas)
	mse_list = []
	for train_index, test_index in kf.split(fechas): 
		#print("TRAIN:", train_index, "TEST:", test_index)
		fechas_train, fechas_test = fechas[train_index], fechas[test_index]
		print fechas_train, fechas_test
		mse = perform(functionToRun, fechas_train, fechas_test, *args)
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

def pol_grado_n_v2(n, x):
	return [(x/20.0) ** i for i in range(0,n+1)] 

def pol_trigo_grado_n(n, x):
	return [ math.sin(i*x) for i in range(1,n+1)] + [ math.cos(i*x) for i in range(1,n+1)] + [1]

def pol_trigo_grado_n_v2(n, x):
	return [ math.sin(i*x) * math.cos(i*x) for i in range(1,n+1)] + [1]

def anios_vs_tempGlobal(c):
	anios = anios_global(c)
	temperaturas_globales = temperaturas_global(anios, c)
	graficar(anios, temperaturas_globales, "Años".decode('utf-8'), "Temperatura global", "anios_vs_tempGlobal")

def mses_anios_global(anios):
	metodos = range(1,4)

	mses = []
	for metodo in metodos:
		print "probando metodo " + str(metodo)
		if metodo == 1:
			for i in range(1,6):
				mse = cross_validation(anios, 10, cross_validation_anios_global, [metodo, i, 0])
				print "metodo {}. Iteracion: {}. Resultado: {}".format(str(metodo), i, mse) 
				mses.append(mse)
		elif metodo == 2:
			for i in range(1,6):
				mse = cross_validation(anios, 10, cross_validation_anios_global, [metodo, 0, i])
				mses.append(mse)
				print "metodo {}. Iteracion: {}. Resultado: {}".format(str(metodo), i, mse) 
		elif metodo == 3:
			for i in range(1,10):
				mse = cross_validation(anios, 10, cross_validation_anios_global, [metodo, 2, i])
				mses.append(mse)
				print "metodo {}. Iteracion: {}. Resultado: {}".format(str(metodo), i, mse)  
	return mses


def metodo_anios_global(metodo, grado_pol, grado_pol_tri, anio):
	if metodo == 1:
		return pol_grado_n(grado_pol,anio)
	elif metodo == 2:
		return pol_trigo_grado_n(grado_pol_tri,anio)
	elif metodo == 3:
		return pol_trigo_grado_n(grado_pol_tri,anio) + pol_grado_n_v2(grado_pol,anio)


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

def aproximacion_paises_global(anios):

# \item Sudamérica: Argentina, Brasil, Venezuela, Peru, Bolivia
# \item Norteamérica + Centroamérica: Eestados Unidos, Canada, Mexico, Cuba, Nicaragua
# \item Europa: Noruega, Portugal, Grecia, Ucrania, Alemania	
# \item Asia: Rusia, China, Mongolia, Japon, India
# \item África: Sudafrica, Egipto, Congo, Somalia, Nigeria
# \item Oceanía: Australia, Nueva Zelanda, Papua Nueva Guinea, Samoa, Tonga

	paises1 = ['Argentina', 'Brazil', 'Venezuela', 'Chile', 'Bolivia']
	paises2 = ['United_States', 'Canada', 'Mexico', 'Cuba', 'Nicaragua']
	paises3 = ['Norway', 'Portugal', 'Greece', 'Ukraine', 'Germany']
	paises4 = ['Russia', 'China', 'Mongolia', 'Japan', 'India']
	paises5 = ['South_Africa', 'Egypt', 'Congo_(Democratic_Republic_Of_The)', 'Somalia', 'Nigeria']
	paises6 = ['Australia', 'New_Zealand', 'Papua_New_Guinea', 'Samoa', 'Tonga']
	paises = [paises1, paises2, paises3, paises4, paises5, paises6]
	#paises = [paises6]
	mses = []
	for ps in paises:
		mse = cross_validation(anios, 5, cross_validation_paises_promedio_global, [ps])
		print "Mse para {}: {}".format(ps, mse)
		mses.append(mse)
	return mses



conn = lite.connect("temperaturas.db")
c = conn.cursor()

#anios = anios_global(c)
anios = range(1890,2013)
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

#print cross_validation(anios, 1, cross_validation_anios_global, [1, 5])
#print cross_validation_anios_global(anios_train, anios_test, 1, 5)

# Aproximacion global anios
#mses_anios_global(anios)

# Aproximacion global paises
#aproximacion_paises_global(anios)

anios_train = range(1890,1988)
anios_test = range(1988,2013)
paises = ['Russia', 'China', 'Mongolia', 'Japan', 'India']
cross_validation_paises_promedio_global(anios_train, anios_test, paises, True)