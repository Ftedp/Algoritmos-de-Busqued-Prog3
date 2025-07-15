from collections import deque

class Nodo:
    def __init__(self, estado, padre=None, accion=None, costo=0):
        self.estado = estado
        self.padre = padre
        self.accion = accion
        self.costo = costo

    def reconstruir_camino(self):
        camino = []
        nodo = self
        while nodo:
            camino.append((nodo.estado, nodo.accion))
            nodo = nodo.padre
        return list(reversed(camino))


class ProblemaCruceRio:
    def __init__(self):
        self.inicial = ('L', 'L', 'L', 'L')
        self.objetivo = ('R', 'R', 'R', 'R')
        self.pesos = {'A': 100, 'B': 60, 'C': 40}
        self.indices = {'A': 0, 'B': 1, 'C': 2}

    def test_objetivo(self, estado):
        return estado == self.objetivo

    def acciones(self, estado):
        lado_bote = estado[3]
        personas_en_lado = [p for p in ['A', 'B', 'C'] if estado[self.indices[p]] == lado_bote]

        posibles = [['A'], ['B'], ['C'], ['B', 'C']]
        acciones_validas = []

        for grupo in posibles:
            if all(p in personas_en_lado for p in grupo):
                peso_total = sum(self.pesos[p] for p in grupo)
                if peso_total <= 100:
                    acciones_validas.append(grupo)
        return acciones_validas

    def resultado(self, estado, accion):
        lado_bote = estado[3]
        lado_opuesto = 'R' if lado_bote == 'L' else 'L'
        nuevo_estado = list(estado)
        for p in accion:
            idx = self.indices[p]
            if estado[idx] != lado_bote:
                return None  # no se puede mover
            nuevo_estado[idx] = lado_opuesto
        nuevo_estado[3] = lado_opuesto  # mover bote
        return tuple(nuevo_estado)

    def costo(self, estado, accion):
        return 1  # cada cruce cuesta 1


#TREE_SEARCH


def tree_search(problema):
    n0 = Nodo(problema.inicial)
    frontera = deque([n0])

    while frontera:
        n = frontera.popleft()
        if problema.test_objetivo(n.estado):
            return n.reconstruir_camino()

        for a in problema.acciones(n.estado):
            s = problema.resultado(n.estado, a)
            if s:  # si es un estado válido
                n_ = Nodo(s, padre=n, accion=a, costo=n.costo + problema.costo(n.estado, a))
                frontera.append(n_)
    return None


#GRAPH-SEARCH
def graph_search(problema):
    n0 = Nodo(problema.inicial)
    alcanzados = set([n0.estado])
    frontera = deque([n0])

    while frontera:
        n = frontera.popleft()
        if problema.test_objetivo(n.estado):
            return n.reconstruir_camino()

        for a in problema.acciones(n.estado):
            s = problema.resultado(n.estado, a)
            if s and s not in alcanzados:
                alcanzados.add(s)
                n_ = Nodo(s, padre=n, accion=a, costo=n.costo + problema.costo(n.estado, a))
                frontera.append(n_)
    return None

def tree_search_stack(problema):
    n0 = Nodo(problema.inicial)
    frontera = [n0]  # Pila
    while frontera:
        nodo = frontera.pop()  # LIFO
        if problema.test_objetivo(nodo.estado):
            return nodo.reconstruir_camino()
        for accion in problema.acciones(nodo.estado):
            s = problema.resultado(nodo.estado, accion)
            costo = nodo.costo + problema.costo(nodo.estado, accion)
            nuevo_nodo = Nodo(s, nodo, accion, costo)
            if not contiene_en_camino(nodo, s): 
                frontera.append(nuevo_nodo)
    return None  # fallo

def contiene_en_camino(nodo, estado_nuevo):
    """Devuelve True si el estado_nuevo ya aparece en el camino desde nodo hasta la raíz"""
    while nodo is not None:
        if nodo.estado == estado_nuevo:
            return True
        nodo = nodo.padre
    return False


problema = ProblemaCruceRio()

print("🔍 TREE SEARCH:")
camino_tree = tree_search(problema)
for i, (estado, accion) in enumerate(camino_tree):
    print(f"Paso {i}: Estado = {estado}, Acción = {accion}")

print("\n🔍 GRAPH SEARCH:")
camino_graph = graph_search(problema)
for i, (estado, accion) in enumerate(camino_graph):
    print(f"Paso {i}: Estado = {estado}, Acción = {accion}")

    print("\n🔍 TREE SEARCH con Pila:")
camino_stack = tree_search_stack(problema)
for i, (estado, accion) in enumerate(camino_stack):
    print(f"Paso {i}: Estado = {estado}, Acción = {accion}")
