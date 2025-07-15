class Nodo:
    def __init__(self, estado, padre=None, accion=None, costo=0):
        self.estado = estado          # ('L','R','L','R')
        self.padre = padre            # Nodo padre (para reconstruir el camino)
        self.accion = accion          # Acción que llevó a este nodo
        self.costo = costo            # Costo desde el nodo inicial (puede ser útil para UCS o A*)

    def __eq__(self, other):
        return self.estado == other.estado

    def __hash__(self):
        return hash(self.estado)


class GrafoBusqueda:
    def __init__(self, estado_inicial, es_estado_objetivo, transiciones):
        self.estado_inicial = estado_inicial
        self.es_estado_objetivo = es_estado_objetivo
        self.transiciones = transiciones

    def bfs(self):
        from collections import deque
        nodo_inicial = Nodo(self.estado_inicial)
        frontera = deque([nodo_inicial])
        visitados = set([nodo_inicial.estado])

        while frontera:
            actual = frontera.popleft()

            if self.es_estado_objetivo(actual.estado):
                return self.reconstruir_camino(actual)

            for accion, estado_siguiente in self.transiciones(actual.estado):
                if estado_siguiente not in visitados:
                    visitados.add(estado_siguiente)
                    hijo = Nodo(estado=estado_siguiente, padre=actual, accion=accion, costo=actual.costo + 1)
                    frontera.append(hijo)
        return None

    def reconstruir_camino(self, nodo):
        camino = []
        while nodo:
            camino.append(nodo.estado)
            nodo = nodo.padre
        return list(reversed(camino))


pesos = { 'A': 100, 'B': 60, 'C': 40 }

def generar_transiciones(estado):
    trans = []
    lado_bote = estado[3]
    orilla = [p for p, pos in zip(['A', 'B', 'C'], estado[:3]) if pos == lado_bote]
    posibles_acciones = [['A'], ['B'], ['C'], ['B', 'C']]
    for personas in posibles_acciones:
        if all(p in orilla for p in personas):
            peso_total = sum(pesos[p] for p in personas)
            if peso_total <= 100:
                nuevo_estado = list(estado)
                lado_opuesto = 'R' if lado_bote == 'L' else 'L'
                for p in personas:
                    idx = {'A': 0, 'B': 1, 'C': 2}[p]
                    nuevo_estado[idx] = lado_opuesto
                nuevo_estado[3] = lado_opuesto
                trans.append((personas, tuple(nuevo_estado)))
    return trans


grafo = GrafoBusqueda(
    estado_inicial=('L', 'L', 'L', 'L'),
    es_estado_objetivo=lambda s: s == ('R', 'R', 'R', 'R'),
    transiciones=generar_transiciones
)

solucion = grafo.bfs()
for i, estado in enumerate(solucion):
    print(f"Paso {i}: {estado}")
