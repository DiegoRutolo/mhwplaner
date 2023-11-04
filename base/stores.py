import requests
import pickle
import base.modelo as md

"""
Almacén con los datos de https://docs.mhw-db.com/
Guarda los datos descargados en un archivo data/mhw_store.pickle
"""
class MhwDbStore(md.Store):

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
