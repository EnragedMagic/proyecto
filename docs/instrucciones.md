# Catalogo de instrucciones de DataDSL

## Objetivo

Este documento explica las instrucciones disponibles en DataDSL.

Cada instruccion representa una operacion que el usuario puede escribir dentro de un archivo `.dsl`.

En resumen:

- La gramatica define como se escriben.
- El Visitor interpreta lo que significan.
- El MotorDatos ejecuta las operaciones reales con pandas.

---

# 1. Abrir

La instruccion `abrir` carga un archivo CSV.

Sintaxis:

```text
variable := abrir "ruta/archivo.csv";
```

Ejemplo:

```text
datos := abrir "datos/ventas.csv";
```

Significado:

- `datos` es el nombre de la variable.
- `:=` realiza la asignacion.
- `abrir` indica que debe cargarse un archivo.
- `"datos/ventas.csv"` es la ruta del archivo.

Internamente, el archivo se convierte en un DataFrame de pandas.

---

# 2. Tomar

La instruccion `tomar` selecciona columnas especificas.

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

Solo se conservan las columnas indicadas.

Todas las columnas deben existir.

---

# 3. Cuando

La instruccion `cuando` filtra filas utilizando una condicion.

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

Tambien se pueden combinar condiciones:

```text
ventas := datos
-> cuando precio > 100 y cantidad > 0;
```

Las filas donde la condicion sea verdadera se conservan.

---

# 4. Ordenar

La instruccion `ordenar` organiza los registros segun una columna.

Sintaxis:

```text
-> ordenar por columna
```

Puede indicarse el sentido:

```text
-> ordenar por precio asc
```

o:

```text
-> ordenar por precio desc
```

Significado:

- `asc` = ascendente.
- `desc` = descendente.

Si no se indica direccion, se utiliza orden ascendente.

---

# 5. Crear

La instruccion `crear` genera una nueva columna calculada.

Sintaxis:

```text
-> crear nueva_columna := expresion
```

Ejemplo:

```text
-> crear total := cantidad * precio
```

En este caso se crea una nueva columna llamada `total`.

Su valor se obtiene multiplicando `cantidad` por `precio` en cada fila.

---

# 6. Rellenar

La instruccion `rellenar` reemplaza valores faltantes.

Sintaxis:

```text
-> rellenar columna con valor
```

Ejemplo:

```text
-> rellenar precio con 0
```

Si una fila no tiene precio, el valor faltante se reemplaza por `0`.

---

# 7. Eliminar nulos

La instruccion `eliminar_nulos` elimina filas con valores faltantes.

Sintaxis:

```text
-> eliminar_nulos [columna1, columna2]
```

Ejemplo:

```text
-> eliminar_nulos [precio, cantidad]
```

Se eliminan las filas donde alguna de esas columnas tenga un valor faltante.

---

# 8. Agrupar

La instruccion `agrupar` organiza los datos en grupos.

Sintaxis:

```text
-> agrupar por [columna]
```

Ejemplo:

```text
-> agrupar por [ciudad]
```

Esto permite reunir todas las filas que pertenezcan a la misma ciudad.

Tambien se pueden usar varias columnas:

```text
-> agrupar por [ciudad, producto]
```

Normalmente, despues de `agrupar` se utiliza `resumir`.

---

# 9. Resumir

La instruccion `resumir` calcula estadisticas sobre datos agrupados.

Ejemplo:

```text
-> resumir ingreso := suma(total),
           promedio := media(total),
           registros := contar()
```

Cada resultado recibe un nombre.

En este ejemplo:

- `ingreso` guarda la suma de `total`.
- `promedio` guarda la media de `total`.
- `registros` cuenta las filas de cada grupo.

---

# 10. Funciones de agregacion

DataDSL permite las siguientes funciones:

## suma

```text
suma(columna)
```

Suma los valores de una columna.

## media

```text
media(columna)
```

Calcula el promedio.

## mediana

```text
mediana(columna)
```

Calcula la mediana.

## minimo

```text
minimo(columna)
```

Obtiene el valor minimo.

## maximo

```text
maximo(columna)
```

Obtiene el valor maximo.

## desviacion

```text
desviacion(columna)
```

Calcula la desviacion estandar.

## contar

```text
contar()
```

Cuenta los registros de cada grupo.

---

# 11. Guardar

La instruccion `guardar` exporta un conjunto de datos a CSV.

Sintaxis:

```text
guardar variable como "ruta/archivo.csv";
```

Ejemplo:

```text
guardar resumen como "salidas/resumen.csv";
```

La variable debe existir antes de poder guardarse.

---

# 12. Mostrar

La instruccion `mostrar` representa una visualizacion.

Sintaxis:

```text
mostrar barras de variable;
```

Ejemplo:

```text
mostrar barras de resumen;
```

En el segundo corte esta instruccion sigue siendo reconocida, pero la implementacion completa de visualizaciones corresponde al tercer corte.

---

# 13. Asignacion

DataDSL utiliza:

```text
:=
```

para asignar un resultado a una variable.

Ejemplo:

```text
datos := abrir "datos/ventas.csv";
```

La variable `datos` queda registrada dentro de la tabla de simbolos.

---

# 14. Encadenamiento

DataDSL utiliza:

```text
->
```

para aplicar varias operaciones de forma consecutiva.

Ejemplo:

```text
ventas := datos
-> tomar [ciudad, precio]
-> cuando precio > 100
-> ordenar por precio desc;
```

Cada paso utiliza como entrada el resultado del paso anterior.

---

# 15. Operadores aritmeticos

DataDSL permite:

```text
+
-
*
/
%
^
```

Ejemplo:

```text
cantidad * precio
```

Pueden utilizarse principalmente en columnas calculadas.

---

# 16. Operadores relacionales

DataDSL permite:

```text
>
<
>=
<=
==
!=
```

Ejemplo:

```text
precio >= 100
```

Se utilizan principalmente para construir filtros.

---

# 17. Operadores logicos

DataDSL permite:

```text
y
o
```

Ejemplo:

```text
precio > 100 y cantidad > 0
```

`y` requiere que ambas condiciones sean verdaderas.

`o` requiere que al menos una condicion sea verdadera.

---

# 18. Valores booleanos

DataDSL reconoce:

```text
verdadero
falso
```

---

# 19. Numeros

Se permiten enteros y decimales.

Ejemplos:

```text
10
250
3.14
1500.50
```

---

# 20. Cadenas de texto

Las cadenas se escriben entre comillas dobles.

Ejemplos:

```text
"Bogota"
"ventas.csv"
"datos/ventas.csv"
```

---

# 21. Identificadores

Los identificadores representan nombres de variables o columnas.

Ejemplos validos:

```text
datos
ventas
ventas_limpias
precio
total
datos2026
```

Deben comenzar con una letra o guion bajo.

---

# Ejemplo completo

```text
datos := abrir "datos/ventas.csv";

ventas_limpias := datos
-> tomar [ciudad, producto, cantidad, precio]
-> cuando cantidad > 0
-> crear total := cantidad * precio
-> ordenar por total desc;

resumen := ventas_limpias
-> agrupar por [ciudad]
-> resumir ingreso := suma(total),
           promedio := media(total),
           registros := contar();

guardar resumen como "salidas/resumen_ciudades.csv";
```

Este programa:

1. Carga un CSV.
2. Selecciona columnas.
3. Filtra registros.
4. Crea una columna.
5. Ordena los resultados.
6. Agrupa por ciudad.
7. Calcula estadisticas.
8. Exporta una tabla resumen.
