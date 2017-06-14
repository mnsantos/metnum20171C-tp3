import csv
from classestp import *

def cargarPaisesCSV():
	with open('../data/temperaturas/GlobalLandTemperaturesByCountry.csv') as csvfile:
		reader = csv.DictReader(csvfile)
		paises = {}
		for row in reader:
			if not(row['Country'] in paises):
				country = Pais(row['Country'])
				paises[row['Country']] = country

			if (not(row['AverageTemperature'] == '' or row['AverageTemperatureUncertainty'] == '')):
				reading = Medicion(row['dt'], row['AverageTemperature'], row['AverageTemperatureUncertainty'])
				paises[row['Country']].agregarMedicion(reading)

#			print(row['dt'],row['AverageTemperature'],row['AverageTemperatureUncertainty'],row['Country'])
	return paises

def cargarCiudadesCSV(paises):
	with open('../data/temperaturas/GlobalLandTemperaturesByCity.csv') as csvfile:
		reader = csv.DictReader(csvfile)
		ciudades = {}
		for row in reader:
			if not(row['City'] in ciudades):
				city = Ciudad(row['City'],row['Country'],row['Latitude'],row['Longitude'])
				ciudades[row['City']] = city
			
			if (not(row['AverageTemperature'] == '' or row['AverageTemperatureUncertainty'] == '')):
				reading = Medicion(row['dt'], row['AverageTemperature'], row['AverageTemperatureUncertainty'])
				ciudades[row['City']].agregarMedicion(reading)

			paises[row['Country']].agregarCiudad(row['City'])

#			print(row['dt'],row['AverageTemperature'],row['AverageTemperatureUncertainty'],row['City'],row['Country'],row['Latitude'],row['Longitude'])
	return ciudades

def cargarMundoCSV():
	fieldnames = ['dt', 'AverageTemperature']
	with open('../data/temperaturas/worldTemperature.csv') as csvfile:
		reader = csv.DictReader(csvfile, fieldnames, delimiter=' ')
		world = Mundo()
		for row in reader:
			if not(row['AverageTemperature'] == ''):
				reading = Medicion(row['dt'], row['AverageTemperature'], 0)
				world.agregarMedicion(reading)

#			print(row['dt'], row['AverageTemperature'])
	return world

paises = cargarPaisesCSV()
print len(paises.keys())
ciudades = cargarCiudadesCSV(paises)
print len(ciudades.keys())
mundo = cargarMundoCSV()
print len(mundo.darMediciones())