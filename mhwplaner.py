import base.modelo as md
import base.stores as st

store = st.MhwDbStore()

# s_escudo no existe en estos datos ??
s_guardia = store.habilidadByNombre("Guard")
s_artilleria = store.habilidadByNombre("Artillery")
s_bloqueo_agro = store.habilidadByNombre("Offensive Guard")
s_capacidad = store.habilidadByNombre("Capacity Boost")
s_ataque = store.habilidadByNombre("Attack Boost")

for x in store.findPiezas(habilidad=s_guardia, 
		rango=md.Rango.MAESTRO, parte=md.Parte.CABEZA):
	print(x)

