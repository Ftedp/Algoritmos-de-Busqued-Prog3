from typing import Any, Dict

class juego_pilas:
    def __init__(self, estado_inicial):
       self.inicial = estado_inicial

    def jugador(self, estado):
        return "MAX" if len(estado) % 2 == 1 else "MIN" # Cantidad impar de pilas juega MAX, sino MIN

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


def minimax_alfa_beta(problema, estado):
    jugador = problema.jugador(estado)

    if jugador == "MAX":
        sucs = {
            accion: minimax_min_ab(problema, problema.resultado(estado, accion), float("-inf"), float("inf"))
            for accion in problema.acciones(estado)
        }
        return max(sucs, key=sucs.get)
    else:
        sucs = {
            accion: minimax_max_ab(problema, problema.resultado(estado, accion), float("-inf"), float("inf"))
            for accion in problema.acciones(estado)
        }
        return min(sucs, key=sucs.get)



def minimax_max_ab(problema, estado, alfa, beta):
    if problema.es_terminal(estado):
        return problema.utilidad(estado, "MAX")

    valor = float("-inf")
    for accion in problema.acciones(estado):
        sucesor = problema.resultado(estado, accion)
        valor = max(valor, minimax_alfa_beta(problema, sucesor, alfa, beta))
        if valor >= beta:
            return valor
        alfa = max(alfa, valor)
    return valor


def minimax_min_ab(problema, estado, alfa, beta):
    if problema.es_terminal(estado):
        return problema.utilidad(estado, "MAX")

    valor = float("inf")
    for accion in problema.acciones(estado):
        sucesor = problema.resultado(estado, accion)
        valor = min(valor, minimax_alfa_beta(problema, sucesor, alfa, beta))
        if valor <= alfa:
            return valor
        beta = min(beta, valor)
    return valor



juego = juego_pilas([5,5])
accion_optima = minimax_alfa_beta(juego, [5,5])

if accion_optima == 1:
    print("🏆 Gana MAX si ambos juegan óptimamente.")
else:
    print("🏆 Gana MIN si ambos juegan óptimamente.")
