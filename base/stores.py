import requests
import pickle
import re
import base.modelo as md
from bs4 import BeautifulSoup

class MhwDbStore(md.Store):
	"""
	Almacén con los datos de https://docs.mhw-db.com/
	Guarda los datos descargados en un archivo data/mhw_store.pickle
	"""

	_ARCHIVO_COMPLETO = "data/mhw_store.pickle"
	_URL_SKILLS = "https://mhw-db.com/skills"
	_URL_ARMOR = "https://mhw-db.com/armor"

	def __init__(self, nombre="mhw-db", logs=False):
		super().__init__(nombre)
		self.logs = logs

		# intenta cargarse desde archivo
		try:
			with open(self._ARCHIVO_COMPLETO, 'rb') as f:
				datos = pickle.load(f)
			self.cargar(datos)
			if self.logs:
				print(f"Cargados datos desde el archivo")
		except Exception as e:
			if self.logs:
				print(f"No se cargaron datos")
		
		# si no tiene habilidades, las descarga
		if self.habilidades is None or len(self.habilidades) <= 0:
			self._download_habilidades()
	
		# si no tiene armaduras, las descarga
		if self.piezas is None or len(self.piezas) <= 0:
			self._download_piezas()
		
		# se guarda en el archivo para el futuro
		with open(self._ARCHIVO_COMPLETO, 'wb') as f:
			pickle.dump(self, f)
	
	def _download_habilidades(self):
		r = requests.get(self._URL_SKILLS)
		habilidades = r.json()

		for h in habilidades:
			id = h["id"]
			nombre = h["name"]
			descripcion = h["description"]
			nivel_max = len(h["ranks"])
			hab = md.Habilidad(id, nombre, descripcion, nivel_max)
			self.addHabilidad(id, hab)
		r.close()
		if self.logs:
			print(f"Descargadas {len(self.habilidades)} habilidades")

	def _download_piezas(self):
		r = requests.get(self._URL_ARMOR)
		errores = 0
		for p in r.json():
			try:
				id = p["id"]
				nombre = p["name"]
				rango = md.Rango.get(p["rank"])
				parte = md.Parte.get(p["type"])
				rareza = p["rarity"]
				habilidades = md.ListaHabilidades()
				for s in p["skills"]:
					idHabilidad = s["skill"]
					nivel = s["level"]
					habilidades.addHabilidad(self.habilidades[idHabilidad], nivel)
				defensa_base = int(p["defense"]["base"])
				n_huecos_joya = 0
				for s in p["slots"]:
					n_huecos_joya += int(s["rank"])
				self.addPieza(id, md.Pieza(id, nombre, rango, parte, 
						habilidades, defensa_base, n_huecos_joya, rareza))
			except Exception as e:
				if self.logs:
					print(f"Error cargando {p}")
					print(e)
				errores += 1
		r.close()
		if self.logs:
			print(f"Descargadas Piezas de armadura: {len(r.json())} totales / {len(self.piezas)} cargadas / {errores} con error")


class KiranicoStore(md.Store):
	"""Almacén de datos sacados de Kiranico.
	"""
	_ARCHIVO_COMPLETO = "data/kiranico_mhw.pickle"
	_URL_SKILLS = "https://mhworld.kiranico.com/es/skilltrees"
	_URL_ARMOR = "https://mhworld.kiranico.com/es/armorseries"

	def __init__(self, nombre="kiranico", logs=False):
		super().__init__(nombre)
		self.logs = logs

		# intenta cargarse desde archivo
		try:
			with open(self._ARCHIVO_COMPLETO, 'rb') as f:
				datos = pickle.load(f)
			self.cargar(datos)
			if self.logs:
				print(f"Cargados datos desde el archivo")
		except Exception as e:
			if self.logs:
				print(f"No se cargaron datos")
		
		# si no tiene habilidades, las descarga
		if self.habilidades is None or len(self.habilidades) <= 0:
			self._download_habilidades()
	
		# si no tiene armaduras, las descarga
		if self.piezas is None or len(self.piezas) <= 0:
			self._download_piezas()
		
		# se guarda en el archivo para el futuro
		with open(self._ARCHIVO_COMPLETO, 'wb') as f:
			pickle.dump(self, f)
	
	def _download_habilidades(self):
		selector_tabla_habilidades = "#app > div > div > div.content-w > div.content-i > div.content-box.p-4 > div.element-wrapper > div.element-box-tp > div > table > tbody"

		r = requests.get(self._URL_SKILLS)
		sopa = BeautifulSoup(r.content, "html.parser")
		tabla_habilidades = sopa.select_one(selector_tabla_habilidades)

		for td in tabla_habilidades.select("td[rowspan]"):
			url = td.contents[0].attrs['href']
			id = re.compile("https:\/\/mhworld\.kiranico\.com\/es\/skilltrees\/(.*)\/.*").findall(url)[0]
			nombre = td.text
			nivel_max = int(td.attrs["rowspan"]) - 1
			hab = md.Habilidad(id=id, nombre=nombre, nivel_max=nivel_max)
			self.addHabilidad(id, hab)

	def _download_piezas(self):
		pass