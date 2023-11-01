from enum import Enum

class Rango(Enum):
	BAJO = 0
	ALTO = 1
	MAESTRO = 2

	def get( txt: str):
		if txt == "low":
			return Rango.BAJO
		if txt == "high":
			return Rango.ALTO
		if txt == "master":
			return Rango.MAESTRO

class Parte(Enum):
	CABEZA = 1
	BRAZOS = 2
	CUERPO = 3
	CINTURA = 4
	PIERNAS = 5
	CIGUA = 6

	def get(txt: str):
		if txt == "head":
			return Parte.CABEZA
		if txt == "gloves":
			return Parte.BRAZOS
		if txt == "chest":
			return Parte.CUERPO
		if txt == "waist":
			return Parte.CINTURA
		if txt == "legs":
			return Parte.PIERNAS
		return Parte.CIGUA

class Habilidad:
	def __init__(self, id, nombre="", descripcion="", nivel_max=1):
		self.id = id
		self.nombre = nombre
		self.descripcion = descripcion
		self.nivel_max = nivel_max
	
	def __hash__(self) -> int:
		return int(self.id)
	
	def __str__(self) -> str:
		return str(self.nombre)
	
	def __repr__(self) -> str:
		return str(self.nombre)
	
	def __eq__(self, other) -> bool:
		if other == None:
			return False
		return self.id == other.id

class ListaHabilidades:

	def __init__(self) -> None:
		self.lista = {}

	def addHabilidad(self, habilidad: Habilidad, nivel) -> None:
		self.lista[habilidad] = nivel

	def isCompleto(self, habilidad) -> bool:
		return self.lista[habilidad] >= habilidad.nivel_max

class Pieza:
	def __init__(self, id, nombre: str = "", rango: Rango = Rango.MAESTRO, 
			parte: Parte = Parte.CIGUA, habilidades: ListaHabilidades = ListaHabilidades(),
			defensa_base: int = 0, n_huecos_joya: int = 0):
		self.id = id
		self.nombre = nombre
		self.rango = rango
		self.parte = parte
		self.defensa_base = defensa_base
		self.n_huecos_joya = n_huecos_joya	# suma de rangos de huecos
		self.habilidades = habilidades

	def __hash__(self) -> int:
		return int(self.id)
	
	def __str__(self) -> str:
		return f"{self.id}-{self.nombre}"
	
	def __repr__(self) -> str:
		return f"{self.id}-{self.nombre}"
	
	def describe(self) ->  str:
		txt = f"{self.id}-{self.nombre}"
		for h, n in self.habilidades.lista.items():
			txt += f"\n  {h} {n}"
		return txt
	
class Joya:
	def __init__(self, id, nombre="", nivel=1, habilidades={}):
		self.id = id

	def __hash__(self) -> int:
		return int(self.id)

class Store:
	def __init__(self, nombre):
		self.nombre = nombre
		self.habilidades = {}
		self.piezas = {}
	
	def cargar(self, store):
		self.nombre = store.nombre
		self.habilidades = store.habilidades
		self.piezas = store.piezas
	
	def addHabilidad(self, id, habilidad):
		self.habilidades[id] = habilidad

	def addPieza(self, id, pieza):
		self.piezas[id] = pieza
	
	def habilidadByNombre(self, nombre) -> Habilidad:
		for id, h in self.habilidades.items():
			if nombre == h.nombre:
				return h

	def findHabilidad(self, nombre=""):
		for id, h in self.habilidades.items():
			if nombre in h.nombre:
				yield h
	
	def findPiezas(self, habilidad: Habilidad = None, rango: Rango = None, 
				parte: Parte = None, nivel_habilidad: int = None):
		for id, p in self.piezas.items():
			if rango != None and not rango == p.rango:
				continue
			
			if parte != None and not parte == p.parte:
				continue
			
			if habilidad != None and not habilidad in p.habilidades.lista:
				continue

			if nivel_habilidad != None and p.habilidades.lista[habilidad] != nivel_habilidad:
				continue
			
			yield p