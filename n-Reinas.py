import constraint as csp

def n_queens(n):
    # Paso 1️⃣: Crear un objeto de la clase Problem
    reinas = csp.Problem()
    # Paso 2️⃣: Definir variables y dominios
    variables = range(1, n + 1)
    dominio = range(1, n + 1)
    # Paso 3️⃣: Agregar las variables con su respectivo dominio al problema
    for v in variables:
        reinas.addVariable(v, dominio)
    # Paso 4️⃣: Agregar las restricciones al problema
      # - 2 reinas en una misma fila
    reinas.addConstraint(csp.AllDifferentConstraint())
      # - 2 reinas en una misma diagonal
    for i in range(n-1):
        for j in range(i+1,n):
            reinas.addConstraint(csp.FunctionConstraint(lambda x, y, w=i, z=j: abs(x-y) != z-w),
                                 [variables[i], variables[j]])
    return reinas


# Encontrar todas las soluciones para el problema de las 8-reinas usando backtracking. Medir tiempo consumido
# import time
# start = time.time()
# reinas_8 = n_queens(8)
# solver = csp.BacktrackingSolver()
# reinas_8.setSolver(solver)
# reinas_8.getSolutions()
# end = time.time()
# print("Tiempo total: ", end-start)


# Definimos el problema de las 8 reinas
reinas = n_queens(8)

# Paso 5️⃣: Resolver el problema
solver = csp.BacktrackingSolver()
reinas.setSolver(solver)
sol = reinas.getSolution()
print(sol)