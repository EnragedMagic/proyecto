# PROGRAMA 2
# Objetivo:
# Crear una columna calculada y tratar valores faltantes.

datos := abrir "datos/ventas.csv";

ventas_preparadas := datos
-> rellenar precio con 0
-> eliminar_nulos [cantidad]
-> crear total := cantidad * precio
-> ordenar por total desc;

guardar ventas_preparadas como "salidas/ventas_preparadas.csv";
