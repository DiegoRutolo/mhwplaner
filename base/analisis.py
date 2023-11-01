import base.modelo as md
import random as rd
from typing import Iterable

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

class Set:
	_multiplicadores = {
		"defensa": 1,
		"huecos_joya": 2,
		"habilidad_deseada": 10,			# habilidad que interesa
		"habilidad_deseada_completa": 25,	# todos los puntos posibles para una habilidad que interesa
		"habilidad_no_deseada": 0,			# habilidad que no interesa
		"habilidad_no_deseada_completa": 5,	# todos los puntos posibles para una habilidad que interesa
	}

	def __init__(self, 
			habilidades_deseadas = Iterable[md.Habilidad], 
			piezas = Iterable[md.Pieza]) -> None:
		self.habilidades_deseadas = habilidades_deseadas
		self.piezas_equipadas = {
			md.Parte.CABEZA: None,
			md.Parte.CUERPO: None,
			md.Parte.BRAZOS: None,
			md.Parte.CINTURA: None,
			md.Parte.PIERNAS: None
		}

		self.piezas_candidatas = {	# Parte: [piezas, ordenadas, por puntuacion]
			md.Parte.CABEZA: [],
			md.Parte.CUERPO: [],
			md.Parte.BRAZOS: [],
			md.Parte.CINTURA: [],
			md.Parte.PIERNAS: []
		}

		self.habilidades_equipadas = {}	# Habilidad: niveles_actuales

		self._clasifica_piezas(piezas)
		self._build_primeros()

		# Calcula habilidades equipadas
		for parte, pieza in self.piezas_equipadas.items():
			for hab, nivel in pieza.habilidades.lista.items():
				if not hab in self.habilidades_equipadas:
					self.habilidades_equipadas[hab] = 0
				self.habilidades_equipadas[hab] += nivel

		self.puntuacion = self._puntuaSet()

	def get_info(self):
		t = ""
		t += "Piezas:"
		t += "\n  " + str(self.piezas_equipadas[md.Parte.CABEZA])
		t += "\n  " + str(self.piezas_equipadas[md.Parte.CUERPO])
		t += "\n  " + str(self.piezas_equipadas[md.Parte.BRAZOS])
		t += "\n  " + str(self.piezas_equipadas[md.Parte.CINTURA])
		t += "\n  " + str(self.piezas_equipadas[md.Parte.PIERNAS])
		t += "\nHabilidades:"
		for h, n in self.habilidades_equipadas.items():
			t += f"\n  {h} {n} / {h.nivel_max}"
		# t += "\nPuntuacion total: " + str(self.puntuacion)
		return t

	def _puntuaSet(self) -> int:
		puntos = 0
		
		return puntos
	
	def _build_primeros(self):
		"""Elige la mejor candidata"""
		for x in self.piezas_candidatas:
			self.piezas_equipadas[x] = self.piezas_candidatas[x][0][0]
	
	def _clasifica_piezas(self, piezas: Iterable[md.Pieza] = []) -> None:
		""" Guarda todas las piezas indicadas en self.piezas_disponibles,
		usando la parte como id, y ordenandolas por puntuacion
		"""
		
		piezas = map(lambda p: (p, self.puntua_pieza(p)), piezas)
		# p[0] es la pieza, p[1] es la puntuacion
		for pieza in piezas:
			self.piezas_candidatas[pieza[0].parte].append(pieza)
		
		for parte, candidatas in self.piezas_candidatas.items():
			candidatas = sorted(candidatas, key=lambda p: p[1], reverse=True)
	
	def puntua_pieza(self, pieza: md.Pieza) -> int:
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
		return puntos
