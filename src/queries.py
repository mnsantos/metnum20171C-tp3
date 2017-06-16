import sqlite3 as lite
from datetime import datetime
import collections
from collections import OrderedDict

def paises(database):
	c.execute("SELECT pais FROM Paises ORDER BY pais ASC")
	rows = c.fetchall()
	paises = []
	for row in rows:
		paises.append(row[0])
	paises = list(OrderedDict.fromkeys(paises))
	return paises

def years_paises(c):
	c.execute("SELECT fecha FROM Paises ORDER BY fecha ASC")
	rows = c.fetchall()
	years = []
	for row in rows:
		datetime_object = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S')
		year = datetime_object.year
		years.append(year)
	years = list(OrderedDict.fromkeys(years))
	return years



conn = lite.connect("temperaturas.db")
c = conn.cursor()
#print years_paises(c)
print paises(c)
