import base.modelo as md
import random as rd
from typing import Any, Iterable
from random import choice

def build_random_set(piezas_candidatas) -> md.Set:
	a_equipar = []
	a_equipar.append(choice(piezas_candidatas[md.Parte.CABEZA])[0])
	a_equipar.append(choice(piezas_candidatas[md.Parte.CUERPO])[0])
	a_equipar.append(choice(piezas_candidatas[md.Parte.BRAZOS])[0])
	a_equipar.append(choice(piezas_candidatas[md.Parte.CINTURA])[0])
	a_equipar.append(choice(piezas_candidatas[md.Parte.PIERNAS])[0])
	return md.Set(a_equipar)
	

class Analizador:
	_multiplicadores = {	# Como se valora cada aspecto de una pieza o set
		"defensa": 1,
		"huecos_joya": 7,
		"habilidad_deseada": 20,			# habilidad que interesa
		"habilidad_deseada_completa": 100,	# todos los puntos posibles para una habilidad que interesa
		"habilidad_no_deseada": 0,			# habilidad que no interesa
		"habilidad_no_deseada_completa": 10,	# todos los puntos posibles para una habilidad que interesa
	}

	def __init__(self,
			  habilidades_deseadas = Iterable[md.Habilidad],
			  piezas_disponibles = Iterable[md.Pieza]) -> None:
		
		self.piezas_candidatas = {	# Parte: [(10, piezas), (8, ordenadas), (6, por puntuacion)]
			md.Parte.CABEZA: [],
			md.Parte.CUERPO: [],
			md.Parte.BRAZOS: [],
			md.Parte.CINTURA: [],
			md.Parte.PIERNAS: []
		}

		self.habilidades_deseadas = habilidades_deseadas
		self._clasifica_piezas(piezas_disponibles)

	def _clasifica_piezas(self, piezas: Iterable[md.Pieza] = []) -> None:
		""" Guarda todas las piezas indicadas en self.piezas_disponibles,
		usando la parte como id, y ordenandolas por puntuacion descendente
		"""
		
		piezas = list(map(lambda p: (p, self.puntua_pieza(p)), piezas))
		# p[0] es la pieza, p[1] es la puntuacion
		for pieza in piezas:
			self.piezas_candidatas[pieza[0].parte].append(pieza)
		
		for parte, candidatas in self.piezas_candidatas.items():
			self.piezas_candidatas[parte] = sorted(candidatas, key=lambda p: p[1], reverse=True)
	
	def puntua_pieza(self, pieza: md.Pieza) -> int:
		puntos = 0
		puntos += pieza.defensa_base * self._multiplicadores["defensa"]
		puntos += pieza.n_huecos_joya * self._multiplicadores["huecos_joya"]
		for h, n in pieza.habilidades.lista.items():
			if h in self.habilidades_deseadas:
				puntos += n * self._multiplicadores["habilidad_deseada"]
				if h.is_completa(n):
					puntos += self._multiplicadores["habilidad_deseada_completa"]
			else:
				puntos += n * self._multiplicadores["habilidad_no_deseada"]
				if h.is_completa(n):
					puntos += self._multiplicadores["habilidad_no_deseada_completa"]
		return puntos
	
	def puntua_set(self, set: md.Set) -> int:
		"""Como se puntua:
		 - Habilidad deseada
		 -- Por fracción de completa
		 - Habilidad no deseada
		 -- Bonus si está completa
		 - Huecos de joya
		 -- Cada hueco vale su nivel
		 - Puntos de defensa
		"""
		puntos = 0
		
		# puntuar habilidades
		for h, n in set.habilidades_equipadas.items():
			if h in self.habilidades_deseadas:
				valor_por_punto = self._multiplicadores["habilidad_deseada_completa"] / h.nivel_max
				puntos += int(min(valor_por_punto * n, valor_por_punto * h.nivel_max))
			else:
				puntos += self._multiplicadores["habilidad_no_deseada"]
				if h.is_completa(n):
					puntos += self._multiplicadores["habilidad_no_deseada_completa"]

		# puntuar valores de piezas piezas
		for parte, pieza in set.piezas_equipadas.items():
			puntos += pieza.n_huecos_joya * self._multiplicadores["huecos_joya"]
			puntos += pieza.defensa_base * self._multiplicadores["defensa"]

		return puntos

