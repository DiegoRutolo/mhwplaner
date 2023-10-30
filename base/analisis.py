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
