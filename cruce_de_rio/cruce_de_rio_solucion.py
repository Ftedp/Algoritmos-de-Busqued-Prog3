from collections import deque

# Pesos de las personas
pesos = {
    'A': 100,
    'B': 60,
    'C': 40
}

# Estado inicial y objetivo
estado_inicial = ('L', 'L', 'L', 'L')
estado_objetivo = ('R', 'R', 'R', 'R')

# Todas las combinaciones de personas válidas por peso
def acciones_validas(orilla):
    posibles = [['A'], ['B'], ['C'], ['B', 'C']]
    return [comb for comb in posibles if sum(pesos[p] for p in comb) <= 100 and all(p in orilla for p in comb)] # list comprehension

# Aplica una acción y devuelve el nuevo estado
def transicion(estado, personas):
    nuevo = list(estado)
    lado_actual = estado[3]
    lado_opuesto = 'R' if lado_actual == 'L' else 'L'

    indices = {'A': 0, 'B': 1, 'C': 2}
    for p in personas:
        idx = indices[p]
        if estado[idx] != lado_actual:
            return None  # no se puede mover desde el lado contrario
        nuevo[idx] = lado_opuesto
    if estado[3] != lado_actual:
        return None  # el bote no está en ese lado
    nuevo[3] = lado_opuesto
    return tuple(nuevo)

# Búsqueda BFS para encontrar la solución óptima
def bfs():
    frontera = deque()
    frontera.append((estado_inicial, []))  # estado, camino
    visitados = set()
    visitados.add(estado_inicial)

    while frontera:
        actual, camino = frontera.popleft()

        if actual == estado_objetivo:
            return camino + [actual]

        lado_bote = actual[3]
        orilla_actual = [p for p, pos in zip(['A', 'B', 'C'], actual[:3]) if pos == lado_bote]
        for personas in acciones_validas(orilla_actual):
            siguiente = transicion(actual, personas)
            if siguiente and siguiente not in visitados:
                visitados.add(siguiente)
                frontera.append((siguiente, camino + [actual]))

    return None  # no se encontró solución

# Ejecutar
solucion = bfs()
for i, estado in enumerate(solucion):
    print(f"Paso {i}: {estado}")
