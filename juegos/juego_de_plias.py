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
                if j != k and j > 0 and k > 0 and j > k: 
                    acciones_posibles.append((i,j,k))
        return acciones_posibles

    def resultado(self, estado, accion):
        i, j, k = accion
        nuevo_estado = estado[:i] + [j, k] + estado[i+1:] # Partimos la pila de indice i en j y k y las ubicamos en la posición i+1
        return nuevo_estado

    def es_terminal(self, estado):
        return all(pila in (1, 2) for pila in estado) # True si todas las pilas son de 1 o 2 ladrillos.
    
    def utilidad(self, estado):
        if not self.es_terminal(estado):
            return None
        return 1 if self.jugador(estado) == "MIN" else 0

def minimax(estado, juego, profundidad=0):
    if juego.es_terminal(estado):
        return juego.utilidad(estado)

    jugador = juego.jugador(estado)
    utilidades = []

#obtenemos un nuevo_estado por cada accion posible aplicada sobre el estado actual.
    for accion in juego.acciones(estado): 
        nuevo_estado = juego.resultado(estado, accion) 
        valor = minimax(nuevo_estado, juego, profundidad + 1)
        utilidades.append(valor)

    if jugador == "MAX":
        return max(utilidades)
    else:
        return min(utilidades)


juego = juego_pilas([7])
ganador = minimax([7], juego)

if ganador == 1:
    print("🏆 Gana MAX si ambos juegan óptimamente.")
else:
    print("🏆 Gana MIN si ambos juegan óptimamente.")

#que son las utilidades?
# que es un nuevo_estado? Sería algo como un nuevo nodo?
#que son el 7 en juego_pilas([7]) y que es el 7 en minimax([7], juego)