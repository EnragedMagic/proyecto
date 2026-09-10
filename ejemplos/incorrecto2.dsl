datos := abrir "ventas.csv";

ventas := datos
-> tomar [ciudad, producto, precio
-> cuando precio > 100;
