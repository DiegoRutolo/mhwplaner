import base.modelo as md

def print_piezas_por_habilidades(habilidades, store):
	todas = []
	candidatos_por_habilidades = {}

	for s in habilidades:
		for p in store.findPiezas(habilidad=s):
			todas.append(p)

	for p in todas:
		n = todas.count(p)
		if not n in candidatos_por_habilidades:
			candidatos_por_habilidades[n] = []
		if not p in candidatos_por_habilidades[n]:
			candidatos_por_habilidades[n].append(p)

	for x in range(len(candidatos_por_habilidades)):
		print(x+1)
		for y in candidatos_por_habilidades[x+1]:
			print(y)
			for h, n in y.habilidades.lista.items():
				print("  ", h, n)

"""
Puntuacion: suma de las puntuaciones de todas las piezas
"""
class Set:
	_multiplicadores = {
		"defensa": 1,
		"huecos_joya": 1,
		"habilidad_deseada": 10,			# habilidad que interesa
		"habilidad_deseada_completa": 25,	# todos los puntos posibles para una habilidad que interesa
		"habilidad_no_deseada": 0,			# habilidad que no interesa
		"habilidad_no_deseada_completa": 0,	# todos los puntos posibles para una habilidad que interesa
	}

	def __init__(self, habilidades_deseadas = []) -> None:
		self.piezas_equipadas = {
			md.Parte.CABEZA: None,
			md.Parte.CUERPO: None,
			md.Parte.BRAZOS: None,
			md.Parte.CINTURA: None,
			md.Parte.PIERNAS: None
		}
		self.piezas_candidatas = {
			md.Parte.CABEZA: [],
			md.Parte.CUERPO: [],
			md.Parte.BRAZOS: [],
			md.Parte.CINTURA: [],
			md.Parte.PIERNAS: []
		}
		self.piezas_disponibles = {}
		self.habilidades_deseadas = habilidades_deseadas
		self.puntuacion = 0
	
	def clasisicaCandidatas(self) -> None:
		def isParte(pieza: md.Pieza, parte: md.Parte):
			pieza.parte == parte
		
		for parte, piezas in self.piezas_candidatas.items():
			piezas_de_parte = filter(lambda pieza: pieza[0].parte == parte, 
					self.piezas_disponibles.items())
			ordenadas = sorted(piezas_de_parte, key=lambda p: p[1], reverse=True)
			for x in ordenadas:
				print(x)
			

	def puntuaPiezaAnhade(self, pieza: md.Pieza) -> int:
		puntos = self.puntuaPieza(pieza)
		self.addPieza(pieza, puntos)
	
	def puntuaPieza(self, pieza: md.Pieza) -> int:
		puntos = 0
		puntos += pieza.defensa_base * self._multiplicadores["defensa"]
		puntos += pieza.n_huecos_joya * self._multiplicadores["huecos_joya"]
		for h, n in pieza.habilidades.lista.items():
			if h in self.habilidades_deseadas:
				puntos += n * self._multiplicadores["habilidad_deseada"]
				if n >= h.nivel_max:
					puntos += self._multiplicadores["habilidad_deseada_completa"]
			else:
				puntos += n * self._multiplicadores["habilidad_no_deseada"]
				if n >= h.nivel_max:
					puntos += self._multiplicadores["habilidad_no_deseada_completa"]
		# self.piezas_disponibles[pieza] = puntos
		return puntos
	
	def addPieza(self, pieza: md.Pieza, puntos: int) -> None:
		self.piezas_disponibles[pieza] = puntos