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

piezas = []	# lista con todas las piezas que me interesan
for h in habilidades:
	piezas.extend(store.findPiezas(habilidad=h, rango=md.Rango.MAESTRO))

estrategia = a.Estrategia(habilidades, piezas)
intentos = 1000

mejor_set = [0, a.build_random_set(estrategia.piezas_candidatas)]
for i in range(intentos):
	set = a.build_random_set(estrategia.piezas_candidatas)
	puntos = estrategia.puntua_set(set)
	if puntos > mejor_set[0]:
		mejor_set[0] = puntos
		mejor_set[1] = set


print(mejor_set[0])
print(mejor_set[1].get_info())
