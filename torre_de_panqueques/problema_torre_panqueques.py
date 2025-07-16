#formulación del problema.
#n = cantidad de panqueques
#di (perteneciente a N) diametro de cada panqueque
'''
P = (S, A, T, s0, G, c)
S = estados: permutaciones de los n panqueques
A = voltear los primeros k panqueques donde 2 <= k <= n
T(s,a) = aplicar un flip sobre los primeros k panqueques.
s0 = estado inicial: torre desordenada
G = estado objetivo: torre ordenada de mayor a menor 
c(s,a) = costo de la accion: 1
'''
from collections import deque

class Nodo:
    def __init__(self, estado, padre=None, accion=None, costo=1):
        self.estado = estado
        self.padre = padre
        self.accion = accion
        self.costo = costo

    def obtener_camino(self):
        camino = []
        nodo = self
        while nodo is not None:
            camino.append((nodo.estado, nodo.accion))
            nodo = nodo.padre
        return list(reversed(camino))


class Problema_panqueques:
    def __init__(self, torre_inicial):
        self.inicial = tuple(torre_inicial)
        self.objetivo = tuple(sorted(torre_inicial, reverse = True))

    def estado_inicial(self):
        return self.inicial 

    def test_objetivo(self, estado):
        return estado == self.objetivo

    def acciones(self, estado):
        return list(range(2, len(estado) + 1))

    def transformacion(self, estado, accion):
        k = accion
        return tuple(reversed(estado[:k])) + estado[k:]
    
    def costo(self, estado, accion):
        return 1


#Graph search
def graph_search(problema, usar_dfs=False):
    n0 = Nodo(problema.estado_inicial())
    frontera = deque([n0])
    alcanzados = set([n0.estado])

    while frontera:
        nodo = frontera.pop() if usar_dfs else frontera.popleft()

        if problema.test_objetivo(nodo.estado):
            return nodo.obtener_camino()

        for accion in problema.acciones(nodo.estado):
            estado_siguiente = problema.transformacion(nodo.estado, accion)
            if estado_siguiente not in alcanzados:
                alcanzados.add(estado_siguiente)
                hijo = Nodo(estado_siguiente, nodo, accion, nodo.costo + problema.costo(nodo.estado, accion))
                frontera.append(hijo)
    
    return None


# -------------------- Mostrar camino --------------------
def mostrar_camino(camino, metodo):
    print(f"\n🔍 Método: {metodo}")
    for i, (estado, accion) in enumerate(camino):
        if accion is None:
            print(f"Paso {i}: Estado inicial = {estado}")
        else:
            print(f"Paso {i}: Estado = {estado}, flip({accion})")
    print(f"✔️ Pasos totales: {len(camino) - 1}")

# -------------------- Comparar BFS y DFS --------------------
if __name__ == "__main__":
    torre = [8, 12, 10, 5, 3]
    problema = Problema_panqueques(torre)

    camino_bfs = graph_search(problema, usar_dfs=False)
    camino_dfs = graph_search(problema, usar_dfs=True)

    mostrar_camino(camino_bfs, "BFS (cola FIFO)")
    mostrar_camino(camino_dfs, "DFS (pila LIFO)")


