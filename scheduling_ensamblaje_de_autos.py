import constraint as csp

# Paso 1️⃣: Crear un objeto de la clase Problem
scheduling = csp.Problem()

# Paso 2️⃣: Definir variables y dominios.
trenes = ["TREN-D", "TREN-T"]
ruedas = ["RUEDA-DI","RUEDA-DD","RUEDA-TI","RUEDA-TD"]
tuercas = ["TUERCA-DI","TUERCA-DD","TUERCA-TI","TUERCA-TD"]
tazas = ["TAZA-DI","TAZA-DD","TAZA-TI","TAZA-TD"]
inspec = "INSPEC"
variables = trenes + ruedas + tuercas + tazas + [inspec]
dominio = range(0,31)

# Paso 3️⃣: Agregar las variables con su respectivo dominio al problema
for v in variables:
    scheduling.addVariable(v, dominio)

# Paso 4️⃣: Agregar las restricciones al problema

  # - Los trenes se deben ensamblar antes que las ruedas y
  # que el ensamblaje de cada tren toma 10 minutos
for i in range(2):
    for j in range(i * 2, i * 2 + 2):
        scheduling.addConstraint(csp.FunctionConstraint(lambda x, y: x + 10 <= y), [trenes[i], ruedas[j]])

  # - Precedencia entre las ruedas y las tuercas:
for i in range(4):
    scheduling.addConstraint(csp.FunctionConstraint(lambda x, y: x + 1 <= y), [ruedas[i], tuercas[i]])

  # - Precedencia entre las tuercas y las tazas:
for i in range(4):
    scheduling.addConstraint(csp.FunctionConstraint(lambda x, y: x + 2 <= y), [tuercas[i], tazas[i]])

  # - Precedencia para la inspección:
for v in tazas:
    scheduling.addConstraint(csp.FunctionConstraint(lambda x, y: x + 1 <= y), [v, inspec])

  # - La inspección debe finalizar en el tiempo límite:
scheduling.addConstraint(csp.FunctionConstraint(lambda x: x <= 27), [inspec])

  # - Impedir que los trenes delantero y trasero se coloquen al mismo tiempo:
scheduling.addConstraint(csp.FunctionConstraint(lambda x, y: (x + 10 <= y) or (y + 10 <= x)),
                         [trenes[0], trenes[1]])

# Paso 5️⃣: Resolver el problema
solver = csp.BacktrackingSolver()
scheduling.setSolver(solver)

print(scheduling.getSolution())