import sqlite3 as lite
from datetime import datetime
import collections
from collections import OrderedDict
import numpy as np

def paises(c):
	c.execute("SELECT pais FROM Paises ORDER BY pais ASC")
	rows = c.fetchall()
	paises = []
	for row in rows:
		paises.append(row[0])
	paises = list(OrderedDict.fromkeys(paises))
	return paises

def anios_paises(c):
	c.execute("SELECT fecha FROM Paises ORDER BY fecha ASC")
	rows = c.fetchall()
	years = []
	for row in rows:
		datetime_object = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S')
		year = datetime_object.year
		years.append(year)
	years = list(OrderedDict.fromkeys(years))
	return years

def temperaturas_estacion_anios(paises, anios, c):
	temps = []
	for anio in anios:
		ts = []
		for p in paises:
			query = "SELECT tempProm FROM Paises WHERE pais = '{}' AND fecha IN ('{}-01-01 00:00:00', '{}-04-01 00:00:00', '{}-07-01 00:00:00','{}-10-01 00:00:00')".format(p, anio, anio, anio, anio)
			c.execute(query)
			rows = c.fetchall()
			for row in rows:
				ts.append(row[0])
		temps.append(ts)
	return temps

def temperaturas_promedio_anios(paises, anios, c):
	temps = []
	for anio in anios:
		ts = []
		for p in paises:
			query = "SELECT tempProm FROM Paises WHERE pais = '{}' AND date(fecha) BETWEEN '{}-01-00 00:00:00' AND '{}-12-31 00:00:00'".format(p, anio, anio)
			c.execute(query)
			rows = c.fetchall()
			temps_anio = []
			for row in rows:
				temps_anio.append(row[0])
			ts.append(sum(temps_anio) / len(temps_anio))
		temps.append(ts)
	temps = np.array(temps)
	return temps

def temperaturas_global(anios, c):
	temps = []
	for anio in anios:
		query = "SELECT tempProm FROM Mundo WHERE fecha = '{}-01-01 00:00:00'".format(anio)
		c.execute(query)
		rows = c.fetchall()
		for row in rows:
			temps.append(row[0])
	temps = np.array(temps).reshape(len(temps), 1)
	return temps

def ciudades_de_pais(pais, anios, c):
	temps = []
	for anio in anios:
		ts = []
		query = "SELECT ciudad, tempProm, latitud, longitud FROM Ciudades WHERE pais = '{}' AND date(fecha) BETWEEN '{}-01-00 00:00:00' AND '{}-12-31 00:00:00'".format(pais, anio, anio)
		c.execute(query)
		rows = c.fetchall()
		for row in rows:
			ts.append(row[0:4])
		temps.append(ts)
	return temps

def ciudades_anios(ciudades, anios, c):
	temps = []
	for anio in anios:
		ts = []
		for ciudad in ciudades:
			query = "SELECT tempProm, latitud, longitud FROM Ciudades WHERE ciudad = '{}' AND date(fecha) BETWEEN '{}-01-00 00:00:00' AND '{}-12-31 00:00:00'".format(ciudad.encode('utf-8'), anio, anio)
			c.execute(query)
			rows = c.fetchall()
			temps_anio = []
			for row in rows:
				temps_anio.append(row[0])
			temp_prom = sum(temps_anio)/len(temps_anio)
			ts = ts + [temp_prom,rows[0][1], rows[0][2]]
		temps.append(ts)
	return temps

def ciudades_anios_v2(ciudades, inicio, fin, c):
	for ciudad in ciudades:
		columna = np.array([])
		print "procesando ciudad " + ciudad.encode('utf-8')
		query = "SELECT tempProm, latitud, longitud FROM Ciudades WHERE ciudad = '{}' AND date(fecha) BETWEEN '{}-01-00 00:00:00' AND '{}-12-31 00:00:00' ORDER BY fecha".format(ciudad.encode('utf-8'), inicio, fin)
		c.execute(query)
		rows = c.fetchall()
		print ciudad.encode('utf-8'), len(rows)
		for row in rows:
			columna = np.append(columna, row[0])
		columna = columna.reshape(columna.size, 1)
		try:
			matriz
		except NameError:
			matriz = columna
		else:
			matriz = np.hstack((matriz, columna))
	return matriz

def ciudades_similares(ciudad, limite):
	temps = []
	queryLat_Long = "SELECT latitud, longitud FROM Ciudades WHERE ciudad = '{}' LIMIT 1".format(ciudad)
	c.execute(queryLat_Long)
	rows = c.fetchall()
	row = rows[0]
	lat1 = row[0]
	long1 = row[1]
	ciudades = []
	query = "SELECT DISTINCT ciudad, latitud, longitud FROM Ciudades WHERE (latitud BETWEEN ({}-{}) AND ({}+{}) OR longitud BETWEEN ({}-{}) AND ({}+{})) AND ciudad != '{}' ORDER BY pais".format(lat1, limite, lat1, limite, long1, limite, long1, limite, ciudad)
	c.execute(query)
	rows = c.fetchall()
	for row in rows:
		ciudades.append(row[0])
	return ciudades

def temperaturas_por_fechas_paises(paises, fechas):
	query = "SELECT fecha, tempProm, "
	for pais in paises:
		query += "(SELECT tempProm from Paises WHERE pais = '"+pais+"' AND fecha = fecha), "
	query = query[:-2]
	query += " FROM Mundo WHERE fecha IN ("
	for fecha in fechas:
		query += "'"+fecha+"', "
	query = query[:-2]
	query += ") "
	c.execute(query)
	rows = c.fetchall()
	return rows

def temperaturas_por_fechas_ciudades(ciudades, fechas):
	query = "SELECT fecha, "
	for ciudad in ciudades:
		query += "(SELECT tempProm from Ciudades WHERE ciudad = '{}' AND fecha = fecha), ".format(ciudad.encode('utf-8'))
	query = query[:-2]
	query += " FROM Ciudades WHERE fecha IN ("
	for fecha in fechas:
		query += "'{}', ".format(fecha)
	query = query[:-2]
	query += ") ORDER BY fecha"
	print query
	c.execute(query)
	rows = c.fetchall()
	return rows

def todos_los_meses_de(anios):
	fechas = []
	for anio in anios:
		for mes in range(1,13):
			fechas.append('{}-{}-01 00:00:00'.format(anio, str(mes).zfill(2)))
	return fechas

# def temperaturas_ciudad_anios(ciudad, anios, c):
# 	temps = []
# 	for anio in anios:
# 		ts = []
# 		for p in paises:
# 			query = "SELECT tempProm FROM Paises WHERE pais = '{}' AND date(fecha) BETWEEN '{}-01-00 00:00:00' AND '{}-12-31 00:00:00'".format(p, anio, anio)
# 			c.execute(query)
# 			rows = c.fetchall()
# 			temps_anio = []
# 			for row in rows:
# 				temps_anio.append(row[0])
# 			ts.append(sum(temps_anio) / len(temps_anio))
# 		temps.append(ts)
# 	return temps

conn = lite.connect("temperaturas.db")
c = conn.cursor()


#similares = ciudades_similares('Tucuman', 0)
#print ciudades_anios_v2(similares[0:2], 1980, 1981, c)


#print similares
#fechas = todos_los_meses_de(range(1980, 1991))
#print fechas
#print temperaturas_por_fechas_ciudades(similares, fechas)

# c.execute("SELECT * FROM Ciudades")
# rows = c.fetchall()
# for row in rows:
# 	print row
#print anios_paises(c)
#print paises(c)
#print temperaturas_anios(['Iceland'], [2000,2001,2002], c)
#print temperaturas_global([2000,2001,2002], c)