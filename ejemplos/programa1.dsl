# PROGRAMA 1
# Objetivo:
# Cargar datos, seleccionar columnas,
# filtrar registros y ordenar el resultado.

datos := abrir "datos/ventas.csv";

ventas_filtradas := datos
-> tomar [ciudad, producto, cantidad, precio]
-> cuando cantidad > 0
-> ordenar por precio desc;

guardar ventas_filtradas como "salidas/ventas_filtradas.csv";
