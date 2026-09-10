# Catalogo de instrucciones

DataDSL utiliza instrucciones sencillas para representar operaciones basicas relacionadas con ciencia de datos.

## Abrir

La instruccion `abrir` permite indicar que una variable representa un archivo CSV.

Sintaxis:

```text
variable := abrir "archivo.csv";
```

Ejemplo:

```text
datos := abrir "ventas.csv";
```

## Tomar

La instruccion `tomar` permite seleccionar las columnas que se quieren conservar de un conjunto de datos.

Sintaxis:

```text
resultado := datos
-> tomar [columna1, columna2];
```

Ejemplo:

```text
ventas := datos
-> tomar [ciudad, producto, precio];
```

## Cuando

La instruccion `cuando` permite aplicar una condicion sobre los datos.

Sintaxis:

```text
resultado := datos
-> cuando condicion;
```

Ejemplo:

```text
ventas := datos
-> cuando precio > 100;
```

Tambien puede usarse despues de otra operacion:

```text
ventas := datos
-> tomar [ciudad, precio]
-> cuando precio > 100;
```

## Mostrar

La instruccion `mostrar` permite reconocer una instruccion de visualizacion.

En esta primera fase solamente se valida la sintaxis de la instruccion. La grafica no se genera todavia.

Sintaxis:

```text
mostrar barras de variable;
```

Ejemplo:

```text
mostrar barras de ventas;
```

## Palabras reservadas

Las palabras reservadas definidas para esta version del lenguaje son:

```text
abrir
tomar
cuando
mostrar
barras
de
verdadero
falso
y
o
```

## Identificadores

Los identificadores representan variables o nombres de columnas.

Pueden comenzar con una letra o con guion bajo. Despues pueden contener letras, numeros o guiones bajos.

Ejemplos validos:

```text
datos
ventas
ventas_limpias
precio
ciudad
datos2026
```

Ejemplos invalidos:

```text
2datos
ventas-limpias
```

## Numeros

El lenguaje reconoce numeros enteros y decimales.

Ejemplos:

```text
10
200
3.14
1500.50
```

## Cadenas de texto

Las cadenas se escriben entre comillas dobles.

Ejemplos:

```text
"ventas.csv"
"Bogota"
"producto"
```

## Valores booleanos

El lenguaje reconoce los valores:

```text
verdadero
falso
```

## Operadores aritmeticos

Los operadores aritmeticos disponibles son:

```text
+
-
*
/
```

Ejemplos:

```text
precio + 100
cantidad * precio
total / 2
```

## Operadores relacionales

Los operadores relacionales disponibles son:

```text
>
<
>=
<=
==
!=
```

Ejemplos:

```text
precio > 100
edad >= 18
ciudad == "Bogota"
precio != 0
```

## Operadores logicos

Los operadores logicos disponibles son:

```text
y
o
```

Ejemplo:

```text
precio > 100 y cantidad > 0
```

## Asignacion

DataDSL utiliza el operador `:=` para asignar un valor o resultado a una variable.

Ejemplo:

```text
datos := abrir "ventas.csv";
```

## Encadenamiento de operaciones

El operador `->` permite aplicar varias operaciones sobre un conjunto de datos.

Ejemplo:

```text
ventas := datos
-> tomar [ciudad, producto, precio]
-> cuando precio > 100;
```

La idea es que cada paso represente una operacion sencilla dentro del flujo de trabajo.
