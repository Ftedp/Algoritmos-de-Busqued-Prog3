'''
Formulacion problema de correctar ortografico, como problema de busqueda.
Acciones permitidas 
Insertar una letra (a-z)
Eliminar una letra
Intercambiar dos letras consecutivas.

P=(S,A,T,s0,G,c)

S = cadenas de caracteres alcanzables desdela palabra mal escrita.
A = Insertar letra, eliminar letra, intercambiar letra
T(s,a) = resultado de aplicar la accion sobre una palabra
s0 = palabra mal escrita
G = cualquier palabra del diccionario U
c(s,a) = costo de insertar, eliminnar o intercambiar = 1

Podemos usar BFS para encontrar la palabra con menor cantidad de transformaciones
GRAPH SEARCH para evitar repetir estados

2) Caminos cíclicos y reduntantes:
Puede haber caminos ciclicos
Puede haber caminos reduntantes

3) Cuantos nodos hay en el arbol de busqueda?
Estado inicial: "acst"
🔸 Nivel 1: aplicar una sola acción
Inserción:

Podés insertar 1 letra entre cada posición de la palabra.

"acst" tiene 4 letras → hay 5 posiciones para insertar letras

Alfabeto tiene 26 letras

➤ 5 × 26 = 130 palabras nuevas por inserción

Eliminación:

Podés eliminar 1 letra en cada una de las 4 posiciones
➤ 4 palabras nuevas

Intercambio:

Hay 3 pares consecutivos que podés intercambiar:
(a,c), (c,s), (s,t)

➤ 3 palabras nuevas

✅ Total en nivel 1:
130 (inserciones)+4 (eliminaciones)+3 (intercambios)= 137

🔸 Nivel 2: aplicar una segunda acción sobre cada uno de los 137 estados del nivel 1
Es un poco más difícil de calcular porque:

Algunas acciones no se pueden aplicar dos veces (ej: no podés eliminar más de lo que hay)

Algunas palabras se repiten

Pero si tomamos un estimado máximo bruto:

Para cada una de las 137 palabras:

Tiene aprox 5 letras → 6 inserciones × 26 letras ≈ 156

~5 eliminaciones

~4 intercambios

➤ Hasta 165 nuevas por cada palabra

✅ Total estimado nivel 2 (máximo bruto):

​137×165≈ 22.605 nodos en nivel 2
 
(Esto es un máximo bruto sin eliminar repetidos)
'''

import string

class ProblemaCorrector:
    def __init__(self, palabra_inicial, diccionario):
        self.inicial = palabra_inicial
        self.diccionario = set(diccionario)

    def estado_inicial(self):
        return self.inicial
    
    def test_objetivo(self, estado):
        return estado in self.diccionario

    def acciones(self, estado):
        acciones_posibles = []  
        letras = string.ascii_lowercase

        # Inserción
        for i in range(len(estado) + 1):
            for l in letras:
                nueva = estado[:i] + l + estado[i:]
                acciones_posibles.append(nueva)

        # Eliminación 
        for i in range(len(estado)):
            nueva = estado[:i] + estado[i+1:]  
            acciones_posibles.append(nueva)

        # Intercambio
        for i in range(len(estado) - 1):
            nueva = list(estado)
            nueva[i], nueva[i+1] = nueva[i+1], nueva[i]
            acciones_posibles.append("".join(nueva))
        
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

    
from collections import deque

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

    return None

        
palabra = "acst"
diccionario = ["casa", "gato", "perro"]

problema = ProblemaCorrector(palabra, diccionario)
camino = graph_search(problema)

if camino is None:
    print("❌ No se encontró solución.")
else:
    print("✅ Sugerencia encontrada:")
    for i, (estado, accion) in enumerate(camino):
        if accion is None:
            print(f"Paso {i}: Inicio en {estado}")
        else:
            print(f"Paso {i}: {estado} ← generado por {accion}")