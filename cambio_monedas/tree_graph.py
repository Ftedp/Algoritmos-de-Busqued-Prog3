#cambio de monedas

from collections import deque

"""
Formulación del problema:
Este problema consiste en dar una cierta cantidad de cambio en monedas de cierta
 denominación, de forma tal que el número de monedas dadas sea mínimo. 

Caso particular:
Dar 6 de cambio y disponiendo de una cantidad ilimitada de monedas
 con denominación 1, 3 y 4.

x=6
monedas = [1, 3, 4]

#Modelación del problema:

P = (S, A, T, s0, G)
donde:
S conjunto de estados
A conjunto de acciones
T función de transición
s0 estado inicial
G conjunto de estados objetivo

S = {0, 1, 2, 3, 4, 5, 6}  # cada estado representa el monto de cambio entregado (acumulado hasta el momento)
A = {1, 3, 4}  # acciones posibles, cada acción representa entregar una moneda de una denominación específica
T(s, a) = s + a  # función de transición, dado un estado s y una acción a, retorna el nuevo estado
#Desde un estado s, solo podemos aplicar una acción a si, s+a <= x.
Costo(s, a) = 1  # el costo de cada acción es 1, ya que cada acción representa entregar una moneda
"""

class CambioMonedas:
    def __init__(self, objetivo, denominaciones):
        self.objetivo = objetivo
        self.denominaciones = denominaciones

    def estado_inicial(self):
        return 0
    
    def test_objetivo(self, estado):
        return estado == self.objetivo
    
    def acciones(self, estado):
        return [ moneda for moneda in self.denominaciones if estado + moneda <= self.objetivo]
        # acciones_posibles = []
        # for moneda in self.denominaciones:
        #     if estado + moneda <= self.objetivo:
        #         acciones_posibles.append(moneda)
        # return acciones_posibles

    def transformacion(self, estado, accion):
        return estado + accion
    
    def costo(self, estado = None, accion = None):
        return 1
    
class Nodo:
    def __init__(self, estado, padre=None, accion=None, costo=0):
        self.estado = estado
        self.padre = padre
        self.hijos = []
        self.accion = accion
        self.costo = costo

    def obtener_camino(self):
        camino = []
        nodo = self
        while nodo.padre is not None:
            camino.append((nodo.estado, nodo.accion))
            nodo = nodo.padre
        camino.append(nodo.estado)
        return list(reversed(camino))
    
def tree_search(problema):
    n0 = Nodo(problema.estado_inicial())  
    frontera = deque([n0])
    while frontera:
        nodo = frontera.popleft()
        if problema.test_objetivo(nodo.estado):
            return nodo.obtener_camino()
        
        for accion in problema.acciones(nodo.estado):
            s = problema.transformacion(nodo.estado, accion)
            nuevo_nodo = Nodo(s, nodo, accion, nodo.costo + problema.costo(nodo.estado, accion)) 
            frontera.append(nuevo_nodo)
    return None

def graph_search(problema):
    n0 = Nodo(problema.estado_inicial())
    frontera = deque([n0])
    visitados = set()

    while frontera:
        nodo = frontera.popleft()
        if problema.test_objetivo(nodo.estado):
            return nodo.obtener_camino()
        
        if nodo.estado not in visitados:
            visitados.add(nodo.estado)
            for accion in problema.acciones(nodo.estado):
                s = problema.transformacion(nodo.estado, accion)
                nuevo_nodo = Nodo(s, nodo, accion, nodo.costo + problema.costo(nodo.estado, accion))
                frontera.append(nuevo_nodo)
    return None

 
#Definición del problema
problema = CambioMonedas(objetivo = 643,denominaciones = [1, 3, 4, 9, 13, 223, 578, 241])
#Búsqueda en árbol
print("Búsqueda en árbol:")
camino_tree = tree_search(problema)
for paso in camino_tree:
    print(paso)

#Búsqueda en grafo
print("\nBúsqueda en grafo:")
camino_graph = graph_search(problema)
for paso in camino_graph:
    print(paso)
