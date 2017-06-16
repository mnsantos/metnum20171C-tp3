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

def temperaturas_anio(paises, anio, c):
	temps = []
	for p in paises:
		query = "SELECT tempProm, fecha FROM Paises WHERE pais = '{}' AND fecha IN ('{}-01-01 00:00:00', '{}-04-01 00:00:00', '{}-07-01 00:00:00','{}-10-01 00:00:00')".format(p, anio, anio, anio, anio)
		c.execute(query)
		rows = c.fetchall()
		for row in rows:
			temps.append(row[0])
	return temps

conn = lite.connect("temperaturas.db")
c = conn.cursor()
#c.execute("SELECT fecha FROM Paises WHERE pais = 'Argentina' ORDER BY date(fecha) DESC")
#rows = c.fetchall()
#for row in rows:
#	print row
#print anios_paises(c)
#print paises(c)
#print temperaturas_anio(['Iceland'], 2000, c)