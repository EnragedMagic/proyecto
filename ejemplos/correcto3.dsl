datos := abrir "ventas.csv";

ventas_filtradas := datos
-> tomar [ciudad, producto, cantidad, precio]
-> cuando precio > 100 y cantidad > 0;

mostrar barras de ventas_filtradas;
