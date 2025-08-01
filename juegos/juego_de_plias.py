"""
Juego de las pilas
 Este juego comienza con una pila de 7 ladrillos y los jugadores MAX y MIN juegan por
 turnos. En su turno, un jugador debe partir una pila de ladrillos en dos pilas nuevas con
 distinta cantidad de ladrillos. Por ejemplo, MAX podría partir la pila de 7 en dos pilas de
 4 y 3. Luego MIN podría partir la pila de 4 en dos pilas de 3 y 1 (está prohibido partirla
 en dos pilas iguales de 2 ladrillos). Como resultado, ahora hay 3 pilas con 3, 3 y 1
 ladrillos. Otra opción para MIN podría haber sido partir la pila de 3 en dos pilas de 2 y 1,
 quedando 3 pilas con 4, 2 y 1 ladrillos. Si en su turno un jugador tiene todas las pilas
 con 1 o 2 ladrillos, entonces ese jugador pierde y su utilidad es 0, mientras que el otro
 jugador gana y su utilidad es 1.
 1. Formular este juego. Representar cada estado como una lista con la cantidad de
 ladrillos de cada pila.
 2. Aplicar el algoritmo minimax para decidir quién gana si ambos juegan
 óptimamente.
 """
from typing import Any, Dict

class juego_pilas:
    def __init__(self, estado_inicial):
       self.inicial = estado_inicial

    def jugador(self, estado):
        return "Turno: MAX" if len(estado) % 2 == 1 else "Turno: MIN" # Cantidad impar de pilas juega MAX, sino MIN

    def acciones(self, estado):
        acciones_posibles = []
        for i, pila in enumerate(estado): # i es el indice de la pila
            for j in range(1, pila): # intentamos partir en j y pila-j
                k = pila - j
                if j != k:
                    a, b = max(j, k), min(j, k)
                    acciones_posibles.append((i, a, b))
        return acciones_posibles

    def resultado(self, estado, accion):
        i, j, k = accion
        nuevo_estado = estado[:i] + [j, k] + estado[i+1:] # Partimos la pila de indice i en j y k y las ubicamos en la posición i+1
        return nuevo_estado

    def es_terminal(self, estado):
        return all(pila <= 2 for pila in estado) # True si todas las pilas son de 1 o 2 ladrillos.
    
    def utilidad(self, estado, jugador):
        if not self.es_terminal(estado):
            return None
        return 1 if self.jugador(estado) != jugador else 0


def minimax(problema: juego_pilas, estado: list[int]) -> Any:
    jugador = problema.jugador(estado)

    if jugador == "MAX":
        sucs: Dict[Any, int] = {
            accion: minimax_min(problema, problema.resultado(estado, accion))
            for accion in problema.acciones(estado)
        }
        return max(sucs, keys=sucs.get)
    else: # jugador == "MIN"
        sucs: Dict[Any, int] = {
            accion: minimax_max(problema, problema.resultado(estado, accion))
            for accion in problema.acciones(estado)
    }

    return min(sucs, key=sucs.get)


def minimax_max(problema: juego_pilas, estado: list[int]) -> int:
    if problema.es_terminal(estado):
        return problema.utilidad(estado, "MAX")

    valor = float("-inf")
    for accion in problema.acciones(estado):
        sucesor = problema.resultado(estado, accion)
        valor = max(valor, minimax_min(problema, sucesor))

    return valor
    

def minimax_min(problema: juego_pilas, estado: list[int]) -> int:
    if problema.es_terminal(estado):
        return problema.utilidad(estado, "MAX")

    valor = float("inf")
    for accion in problema.acciones(estado):
        sucesor = problema.resultado(estado, accion)
        valor = min(valor, minimax_max(problema, sucesor))

    return valor


juego = juego_pilas([5,5])
accion_optima = minimax(juego, [5,5])

if accion_optima == 1:
    print("🏆 Gana MAX si ambos juegan óptimamente.")
else:
    print("🏆 Gana MIN si ambos juegan óptimamente.")
