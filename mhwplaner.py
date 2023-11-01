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

# pantalones = store.piezas[1324]
# 	print(p.describe())

set = a.Set(habilidades)
for h in habilidades:
	for p in store.findPiezas(habilidad=h, rango=md.Rango.MAESTRO):
		if not p in set.piezas_disponibles:
			set.puntuaPiezaAnhade(p)

# for pieza, puntos in sorted(set.piezas_disponibles.items(), key = lambda i: i[1]):
# 	print(f"{pieza}: {puntos}")
set.clasisicaCandidatas()