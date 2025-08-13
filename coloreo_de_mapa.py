import constraint as csp

# 1 creamos un objeto de la clase problem
coloreo = csp.Problem()

# 2 definimos variables y dominimos
variables = ["WA", "NT", "Q", "NSW", "V", "SA", "T"]
dominio = ["rojo", "azul", "verde"]

# 3 agregamos variables con su respectivo dominio al problema
for variable in variables:
    coloreo.addVariable(variable, dominio)

# 4 agregamos restricciones 
aristas = [("WA","NT"), ("WA","SA"),
           ("NT","Q"), ("NT","SA"),
           ("Q","NSW"), ("Q","SA"),
           ("NSW","V"), ("NSW","SA"),
           ("V","SA")]

for arista in aristas:
    coloreo.addConstraint(csp.AllDifferentConstraint(), arista)

# 5 Resolución
solver = csp.BacktrackingSolver()
# solver = csp.MinConflictSolver() #opcion diferente

#obtengo solución
coloreo.setSolver(solver)
print(coloreo.getSolution()) # tambien podemos obtener todas las soluciones posibles con .getSolutions()

"""Observación: dependiendo si queremos resolver el CSP con una búsqueda vuelta atrás o
   con una búsqueda local de mínimos-conflictos utilizaremos los contructores BacktrackingSolver() o
    MinConflictsSolver() respectivamente
""" 
