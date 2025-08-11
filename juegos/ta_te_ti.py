from typing import List, Tuple, Optional
import math

Jugador = str
Estado = List[List[str]]  # 3x3: "X", "O", "."

class Tateti:
    def __init__(self):
        self.jugador_inicial = "X"  # MAX

    def jugador(self, estado: Estado) -> Jugador:
        """ Determina a quién le toca jugar en el estado actual del tablero.
        Args:
            estado (Estado): tablero actual

        Returns:
            Jugador: Devuelve el jugador con el siguiente turno.
        """        

        x_count = sum(row.count("X") for row in estado)
        o_count = sum(row.count("O") for row in estado) 
        return "X" if x_count == o_count else "O"

        """estado = [
                    ["X", ".", "O"], row 0
                    ["O", "X", "."], row 1
                    [".", ".", "O"]] row 2
        Resultado: [1,    1,    1]"""

    def acciones(self, estado: Estado) -> List[Tuple[int, int]]:
        """Genera todas las coordenadas posibles (i, j) del tablero 
        donde haya un punto ".", es decir, casillas vacías. (Acciones legales)
        Args:
            estado (Estado): Tablero actual
        Returns:
            List[Tuple[int, int]]: devuelve una lista de tuplas que contiene cada una coordenadas i, j
        """
        return [(i, j) for i in range(3) for j in range(3) if estado[i][j] == "."] 

    def resultado(self, estado: Estado, accion: Tuple[int, int]) -> Estado:
        """Devuelve la transformación (nuevo_estado) que aplica jugador(X,O) 
        con la accion (i, j) sobre el estado (tablero).
        Args:
            estado (Estado): tablero
            accion (Tuple[int, int]): posición i,j de la ficha colocada (X,O)
        Returns:
            Estado: nuevo tablero 
        """        

        i, j = accion
        jugador = self.jugador(estado) # Determinamos turno
        nuevo_estado = [row.copy() for row in estado] # copia independiente del tablero
        nuevo_estado[i][j] = jugador # Se genera un nuevo estado con la accion del jugador indicado.
        return nuevo_estado

    def es_terminal(self, estado: Estado) -> bool:
        return self.hay_ganador(estado) is not None or all(cell != "." for row in estado for cell in row) 
 
    def utilidad(self, estado: Estado, jugador: Jugador) -> int:
        ganador = self.hay_ganador(estado)
        if ganador is None:
            return self.evaluacion(estado)
        return 1 if ganador == jugador else 0

    def hay_ganador(self, estado: Estado) -> Optional[str]:    
        lineas = self.obtener_lineas(estado)
        #chequeamos si el primer items de cada lista es diferente de nulo y si todas las celdas son iguales, entonces hay ganador.
        for linea in lineas:
            if linea[0] != "." and all(cell == linea[0] for cell in linea):
                return linea[0]
        return None

    def obtener_lineas(self, estado: Estado) -> List[List[str]]:
        return [
            *estado,  # filas
            *[[estado[i][j] for i in range(3)] for j in range(3)],  # columnas
            [estado[i][i] for i in range(3)],  # diagonal principal
            [estado[i][2 - i] for i in range(3)]  # diagonal secundaria
        ]


    def evaluacion(self, estado: Estado) -> int:
        """Calculamos una heurística para un tablero cuando todavía no hay ganador.
        Evaluamos que tan favorable es un estado para el jugador "X"
        Args:
            estado (Estado): _description_
        Returns:
            int: _description_
        """        
        def cuenta_lineas(simbolo):
            
            lineas = self.obtener_lineas(estado)
            x1 = x2 = x3 = 0

            for linea in lineas:
                if "X" in linea and "O" in linea:
                    continue  # línea bloqueada
                count = linea.count(simbolo) # contamos cantidad de veces que aparece X u O. dependiendo el simbolo.
                if count == 1:
                    x1 += 1
                elif count == 2:
                    x2 += 1
                elif count == 3:
                    x3 += 1
            return x1, x2, x3

        x1, x2, _ = cuenta_lineas("X")
        o1, o2, _ = cuenta_lineas("O")
                
        return x1 + x2 - (2 * o2 + o1)


# Minimax con poda alfa-beta y profundidad limitada (versión explícita)
def minimax_ab(problema: Tateti, estado: Estado, profundidad_max: int = 2) -> Tuple[int, int]:
    """
    Recorre todas las acciones posibles y evalúa cada una con minimax y poda alfa–beta.
    Devuelve la acción óptima según si el jugador es MAX (X) o MIN (O).
    """
    
    # Determinar de quién es el turno
    jugador = problema.jugador(estado)

    # Inicializar alfa y beta
    alfa = -math.inf  # Mejor valor que MAX (X) conoce hasta ahora
    beta = math.inf   # Mejor valor que MIN (O) conoce hasta ahora

    # Diccionario para guardar acción -> valor calculado
    sucs = {}

    # Si es el turno de X (MAX)
    if jugador == "X":
        # Recorrer todas las acciones legales
        for accion in problema.acciones(estado):
            # Simular el tablero después de hacer la acción
            nuevo_estado = problema.resultado(estado, accion)

            # Evaluar este nuevo estado usando minimax_max_ab
            valor = minimax_max_ab(
                problema,         # El objeto Tateti
                nuevo_estado,     # Estado resultante de la acción
                alfa,             # Mejor valor que MAX conoce
                beta,             # Mejor valor que MIN conoce
                1,                # Profundidad actual (ya hicimos una jugada)
                profundidad_max   # Profundidad máxima de búsqueda
            )

            # Guardar en el diccionario
            sucs[accion] = valor

        # Devolver la acción con el valor más alto
        mejor_accion = max(sucs, key=sucs.get)
        return mejor_accion

    # Si es el turno de O (MIN)
    else:
        for accion in problema.acciones(estado):
            nuevo_estado = problema.resultado(estado, accion)

            valor = minimax_min_ab(
                problema,
                nuevo_estado,
                alfa,
                beta,
                1,
                profundidad_max
            )

            sucs[accion] = valor

        # Devolver la acción con el valor más bajo
        mejor_accion = min(sucs, key=sucs.get)
        return mejor_accion



def minimax_max_ab(problema, estado, alfa, beta, profundidad, profundidad_max):

    if problema.es_terminal(estado) or profundidad == profundidad_max:
        return problema.utilidad(estado, "X")
    
    valor = -math.inf

    for accion in problema.acciones(estado):
        estado_sucesor = problema.resultado(estado, accion)
        valor = max(valor, minimax_min_ab(problema, estado_sucesor, alfa, beta, profundidad + 1, profundidad_max))
        if valor >= beta:
            return valor
        alfa = max(alfa, valor)

    return valor


def minimax_min_ab(problema, estado, alfa, beta, profundidad, profundidad_max):
    if problema.es_terminal(estado) or profundidad == profundidad_max:
        return problema.utilidad(estado, "X")

    valor = math.inf

    for accion in problema.acciones(estado):
        estado_sucesor = problema.resultado(estado, accion)
        valor = min(valor, minimax_max_ab(problema, estado_sucesor, alfa, beta, profundidad + 1, profundidad_max))
        if valor <= alfa:
            return valor
        beta = min(beta, valor)
    return valor



        

juego = Tateti()
estado_inicial = [[".", ".", "."],
                  [".", ".", "."],
                  [".", ".", "."]]

mejor_jugada = minimax_ab(juego, estado_inicial, profundidad_max=2)
print("Mejor jugada:", mejor_jugada)
