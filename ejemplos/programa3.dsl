# PROGRAMA 3
# Objetivo:
# Procesar los datos y generar una tabla resumen
# agrupada por ciudad.

datos := abrir "datos/ventas.csv";

ventas_limpias := datos
-> tomar [ciudad, producto, cantidad, precio]
-> cuando cantidad > 0
-> crear total := cantidad * precio;

resumen := ventas_limpias
-> agrupar por [ciudad]
-> resumir ingreso := suma(total),
           promedio := media(total),
           registros := contar();

guardar resumen como "salidas/resumen_ciudades.csv";
