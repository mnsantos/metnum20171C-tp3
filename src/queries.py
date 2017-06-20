import sqlite3 as lite
from datetime import datetime
import collections
from collections import OrderedDict

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
	return temps

def temperaturas_global(anios, c):
	temps = []
	for anio in anios:
		query = "SELECT tempProm FROM Mundo WHERE fecha = '{}-01-01 00:00:00'".format(anio)
		c.execute(query)
		rows = c.fetchall()
		for row in rows:
			temps.append(row[0])
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
			query = "SELECT tempProm, latitud, longitud FROM Ciudades WHERE ciudad = '{}' AND date(fecha) BETWEEN '{}-01-00 00:00:00' AND '{}-12-31 00:00:00'".format(ciudad, anio, anio)
			c.execute(query)
			rows = c.fetchall()
			temps_anio = []
			for row in rows:
				temps_anio.append(row[0])
			temp_prom = sum(temps_anio)/len(temps_anio)
			ts = ts + [temp_prom,rows[0][1], rows[0][2]]
		temps.append(ts)
	return temps

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

# conn = lite.connect("temperaturas.db")
# c = conn.cursor()
# print ciudades_de_pais('Argentina', [1999,2000])

# c.execute("SELECT * FROM Ciudades")
# rows = c.fetchall()
# for row in rows:
# 	print row
#print anios_paises(c)
#print paises(c)
#print temperaturas_anios(['Iceland'], [2000,2001,2002], c)
#print temperaturas_global([2000,2001,2002], c)