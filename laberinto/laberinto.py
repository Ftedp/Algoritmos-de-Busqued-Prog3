'''
1) Formulación del problema del laberinto como problema de búsqueda (version discreta) (4x4).
P=(S,A,T,s0,G,c)
S=estados: casillas libres del laberinto.
A=acciones
T(s,a): nueva casilla si el movimiento es válido.
s0: posición inicial pos(0,4)
G: objetivo pos(4,4)
c(s,a): costo 1 por paso.
Solución óptima ruta con menos casillas.

2) Formulación versión continua (plano real)
no podemos mover en cualquier dirección y con cualquier módula, mientras no se crucen paredes.

Consideraciones:
- Los estados ya no son casillas -> son puntos reales: (x,y) E R2.
- Las acciones ya no son solo arriba/abajo/derecha/izquierda. Pueden ser vectores de movimiento de cualquier dirección.
- El movimiento es línea recta.
- Solo se acepta si el segmento no corta paredes.

Estados : coordenadas reales (x,y)
Acciones; cualquier segmento sin cruzar paredes.
Costo: distancia euclidiana.
Solución optima ruta más corta

Redefinición del espacio de estados:
Usamos como nodos del grafo:
-Las esquinas visibles (vértice de las paredes)
Punto inicial (0,4)
Punto objetivo (4,4)
Conectamos aristas entre nodos. Aristas= distancia euclidiana entre puntos
'''
from collections import deque
import heapq
import itertools

class ProblemaLaberintoDiscreto:
    def __init__(self, laberinto, inicial, objetivo):
        self.matriz = laberinto
        self.inicial = inicial
        self.objetivo = objetivo
        self.filas = len(laberinto)
        self.columnas = len(laberinto[0])

    def estado_inicial(self):
        return self.inicial

    def test_objetivo(self, estado):
        return estado == self.objetivo

    def acciones(self, estado):
        x, y = estado
        acciones_posibles = []
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]: #arriba, abajo, izq, der
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.filas and 0 <= ny < self.columnas:
                if self.matriz[nx][ny] == 0:
                    acciones_posibles.append((nx,ny))
        return acciones_posibles
    
    def resultado(self, estado, accion):
        return accion 

    def costo(self, estado, accion):
        return 1

    
class Nodo:
    def __init__(self, estado, padre=None, accion=None, costo=0):
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

def heuristica_manhattan(estado, objetivo):
    x1, y1 = estado
    x2, y2 = objetivo
    return abs(x1 - x2) + abs(y1 - y2)

def a_estrella(problema):
    nodo_inicial = Nodo(problema.estado_inicial())
    frontera = []
    contador = itertools.count()
    heapq.heappush(frontera, (0, next(contador), nodo_inicial)) 
    alcanzados = {nodo_inicial.estado: 0}

    while frontera:
        _,_, nodo = heapq.heappop(frontera)

        if problema.test_objetivo(nodo.estado):
            return nodo.obtener_camino()

        for accion in problema.acciones(nodo.estado):
            nuevo_estado = problema.resultado(nodo.estado, accion)
            g = nodo.costo + problema.costo(nodo.estado, accion)
            h = heuristica_manhattan(nuevo_estado, problema.objetivo)
            f = g + h
            
            if nuevo_estado not in alcanzados or g < alcanzados[nuevo_estado]:
                alcanzados[nuevo_estado] = g 
                hijo = Nodo(nuevo_estado, nodo, accion, g)
                heapq.heappush(frontera, (f, next(contador), hijo))
        
    return None
    

def graph_search(problema):
    n0 = Nodo(problema.estado_inicial())
    frontera = deque([n0])
    alcanzados = set([n0.estado])

    while frontera:
        nodo = frontera.popleft()
    
        if problema.test_objetivo(nodo.estado):
            return nodo.obtener_camino()

        for accion in problema.acciones(nodo.estado):
            nuevo_estado = problema.resultado(nodo.estado, accion)

            if nuevo_estado not in alcanzados:
                alcanzados.add(nuevo_estado)
                hijo = Nodo(nuevo_estado, nodo, accion, nodo.costo + problema.costo(nodo.estado, accion))
                frontera.append(hijo)
    
    return None #si no encuentra sol.

laberinto = [
    [0,0,1,0,0,0,0,0],
    [1,0,0,1,0,1,1,1],
    [1,0,0,0,0,1,0,0],
    [0,0,1,0,0,1,0,1],
    [1,1,1,0,0,0,0,0],
    [0,0,0,0,1,0,0,0]
]

inicial = (0,0)
objetivo = (5,7)

problema = ProblemaLaberintoDiscreto(laberinto, inicial, objetivo)
camino_grafo = graph_search(problema)

print("✅ Solución encontrada con búsqueda de Grafo:")
for i, paso in enumerate(camino_grafo):
    estado, accion = paso
    if accion is None:
        print(f"Paso {i}: Inicio en {estado}")
    else:
        print(f"Paso {i}: Mover a {estado} desde {camino_grafo[i-1][0]}")



camino_estrella = a_estrella(problema)

print("✅ Solución encontrada con A* y heurística:")
for i, paso in enumerate(camino_estrella):
    estado, accion = paso
    if accion is None:
        print(f"Paso {i}: Inicio en {estado}")
    else:
        print(f"Paso {i}: Mover a {estado} desde {camino_estrella[i-1][0]}")

