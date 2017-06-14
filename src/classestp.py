from datetime import date

class Medicion(object):
	"""docstring for Medicion"""
	def __init__(self, fecha, temp, tempE):
		super(Medicion, self).__init__()
		self.fecha = date(fecha)
		self.temp = float(temp)
		self.tempE = float(tempE)

	def __eq__(self, other):
		return ((self.fecha, self.temp, self.tempE) == (other.fecha, other.temp, other.tempE))

	def __lt__(self, other):
		return (self.fecha < other.fecha)

	def __hash__(self):
		return hash((self.fecha, self.temp, self.tempE))

class Pais(object):
	"""docstring for Pais"""
	def __init__(self, nombre):
		super(Pais, self).__init__()
		self.nombre = nombre
		self.ciudades = set()
		self.mediciones = set()

	def agregarCiudad(self, ciudad):
		self.ciudades.add(ciudad)

	def agregarMedicion(self, medicion):
		self.mediciones.add(medicion)

	def darMediciones(self):
		return self.mediciones
	
class Ciudad(object):
	"""docstring for Ciudad"""
	def __init__(self, nombre, pais, latitud, longitud):
		super(Ciudad, self).__init__()
		self.nombre = nombre
		self.pais = pais
		if (latitud[-1] == 'S'):
			self.latitud = -float(latitud[:-1])
		else:
			self.latitud = float(latitud[:-1])
		if (longitud[-1] == 'W'):
			self.longitud = -float(longitud[:-1])
		else:
			self.longitud = float(longitud[:-1])
		self.mediciones = set()
		
	def agregarMedicion(self, medicion):
		self.mediciones.add(medicion)

	def darMediciones(self):
		return self.mediciones

class Mundo(object):
	"""docstring for Mundo"""
	def __init__(self):
		super(Mundo, self).__init__()
		self.mediciones = set()

	def agregarMedicion(self, medicion):
		self.mediciones.add(medicion)

	def darMediciones(self):
		return self.mediciones