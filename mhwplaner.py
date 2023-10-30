import base.modelo as md
import base.stores as st
import base.analisis as a

store = st.MhwDbStore()

# s_escudo no existe en estos datos ??
s_guardia = store.habilidadByNombre("Guard")
s_artilleria = store.habilidadByNombre("Artillery")
s_bloqueo_agro = store.habilidadByNombre("Offensive Guard")
s_capacidad = store.habilidadByNombre("Capacity Boost")
s_ataque = store.habilidadByNombre("Attack Boost")
habilidades = [s_guardia, s_artilleria, s_bloqueo_agro, s_capacidad]

# a.dime_candidatas(habilidades, store)
pantalones = store.piezas[1324]
for p in store.findPiezas(habilidad=s_guardia, nivel_habilidad=2, rango=md.Rango.MAESTRO):
	print(p.describe())