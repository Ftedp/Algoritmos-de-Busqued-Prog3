import constraint as csp

# Paso 1️⃣: Crear un objeto de la clase Problem
sudoku = csp.Problem()

# Paso 2️⃣: Definir variables y dominios
variables = [i * 10 + j for i in range(1,10) for j in range(1,10)]
variables_fijadas = {13:4, 14:7, 15:5, 19:3,\
                     26:8, 27:4,\
                     35:6, 38:7, 39:5,\
                     41:6, 42:3, 47:5,\
                     52:8, 58:6,\
                     63:5, 68:9, 69:1,\
                     71:8, 72:4, 75:3,\
                     83:9, 84:8,\
                     91:3, 95:9, 96:7, 97:1} # Variables con valores fijos
variables_no_fijadas = [v for v in variables if v not in variables_fijadas]

# Paso 3️⃣: Agregar las variables con su respectivo dominio al problema
for v, k in variables_fijadas.items(): # Para variables fijas
    sudoku.addVariable(v, [k]) # Restringimos dominio con el valor fijo asignado

for v in variables_no_fijadas: # Para variables no fijadas
    sudoku.addVariable(v, range(1,10)) # Dominio del 1 al 9

# Paso 4️⃣: Agregar las restricciones al problema

 # - Filas con todos valores distintos
for i in range(1, 10):
    fila = [i * 10 + j for j in range(1,10)]
    sudoku.addConstraint(csp.AllDifferentConstraint(), fila)

 # - Columnas con todos valores distintos
for j in range(1, 10):
    columna = [i * 10 + j for i in range(1,10)] # Definimos todas las columnas
    sudoku.addConstraint(csp.AllDifferentConstraint(), columna)

 # - Cajas con todos valores distintos
for i in range(1,10,3): # Definimos todas las cajas
    for j in range(1,10,3):
        caja = [(i + a) * 10 + j + b for a in range(0,3) for b in range(0,3)]
        sudoku.addConstraint(csp.AllDifferentConstraint(), caja)

# Paso 5️⃣: Resolver el problema
solver = csp.BacktrackingSolver()
sudoku.setSolver(solver)
sol =sudoku.getSolution()
print(sol)