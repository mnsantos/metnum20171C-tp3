import sqlite3 as lite
import sys
import csv
from classestp import *
import dateutil.parser
from datetime import datetime

def insertartMedicionesPaises(databaseName):
	con = None

	try:
		con = lite.connect(databaseName)
		con.text_factory = str

		cur = con.cursor()

		cur.execute("DROP TABLE IF EXISTS Paises")
		cur.execute("CREATE TABLE Paises(fecha text, tempProm real, tempPromE real, pais text)")


		with open('../data/temperaturas/GlobalLandTemperaturesByCountry.csv') as csvfile:
				reader = csv.DictReader(csvfile)
				for row in reader:
					if (not(row['AverageTemperature'] == '' or row['AverageTemperatureUncertainty'] == '')):
						fecha = datetime.strptime(row['dt'], '%Y-%m-%d')
						tempProm = float(row['AverageTemperature'])
						tempPromE = float(row['AverageTemperatureUncertainty'])
						pais = row['Country'].decode("utf-8")

						cur.execute("INSERT INTO Paises VALUES(?,?,?,?)", (fecha,tempProm,tempPromE,pais))
						#print (fecha,tempProm,tempPromE,pais)
		con.commit()

	except lite.Error, e:

		print "Error %s:" % e.args[0]
		sys.exit(1)

	finally:

		if con:
			con.close()

def insertartMedicionesCiudades(databaseName):
	con = None

	try:
		con = lite.connect(databaseName)
		con.text_factory = str

		cur = con.cursor()

		cur.execute("DROP TABLE IF EXISTS Ciudades")
		cur.execute("CREATE TABLE Ciudades(fecha text, tempProm real, tempPromE real, ciudad text, pais text, latitud real, longitud real)")

		with open('../data/temperaturas/GlobalLandTemperaturesByCity.csv') as csvfile:
				reader = csv.DictReader(csvfile)
				for row in reader:
					if (not(row['AverageTemperature'] == '' or row['AverageTemperatureUncertainty'] == '')):
						fecha = datetime.strptime(row['dt'], '%Y-%m-%d')
						tempProm = float(row['AverageTemperature'])
						tempPromE = float(row['AverageTemperatureUncertainty'])
						ciudad = row['City'].decode('utf-8')
						pais = row['Country'].decode('utf-8')
						if (row['Latitude'][-1] == 'S'):
							lat = -float(row['Latitude'][:-1])
						else:
							lat = float(row['Latitude'][:-1])
						if (row['Longitude'][-1] == 'W'):
							lon = -float(row['Longitude'][:-1])
						else:
							lon = float(row['Longitude'][:-1])

						cur.execute("INSERT INTO Ciudades VALUES(?,?,?,?,?,?,?)", (fecha,tempProm,tempPromE,ciudad,pais,lat,lon))
		con.commit()

	except lite.Error, e:

		print "Error %s:" % e.args[0]
		sys.exit(1)

	finally:

		if con:
			con.close()

def insertartMedicionesMundo(databaseName):
	con = None

	try:
		con = lite.connect(databaseName)

		cur = con.cursor()

		cur.execute("DROP TABLE IF EXISTS Mundo")
		cur.execute("CREATE TABLE Mundo(fecha text, tempProm real)")
		with open('../data/temperaturas/worldTemperature.csv') as csvfile:
			fieldnames = ['dt', 'AverageTemperature']
			reader = csv.DictReader(csvfile, fieldnames, delimiter=' ')
			for row in reader:
				fecha = datetime.strptime(row['dt'], '%Y')
				tempProm = float(row['AverageTemperature'])

				cur.execute("INSERT INTO Mundo VALUES(?,?)", (fecha, tempProm))
		con.commit()

	except lite.Error, e:

		print "Error %s:" % e.args[0]
		sys.exit(1)

	finally:

		if con:
			con.close()

insertartMedicionesPaises("temperaturas.db")
insertartMedicionesCiudades("temperaturas.db")
insertartMedicionesMundo("temperaturas.db")

# conn = lite.connect("temperaturas.db")
# c = conn.cursor()
# c.execute("SELECT * FROM Mundo")
# rows = c.fetchall()

# for row in rows:
# 	print row