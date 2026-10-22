# Reglas semanticas de DataDSL

## Objetivo

Este documento explica las reglas semanticas utilizadas por DataDSL.

La sintaxis indica si una instruccion esta bien escrita.

La semantica verifica si esa instruccion tiene sentido durante la ejecucion.

Ejemplo:

```text
ventas := datos
-> tomar [precio];
```

La instruccion puede estar correctamente escrita.

Sin embargo, si la variable `datos` no existe, se produce un error semantico.

---

## Diferencia entre errores

### Error lexico

Ocurre cuando aparece un simbolo o elemento que el lexer no reconoce.

Ejemplo:

```text
datos := abrir @ventas.csv;
```

El simbolo `@` no pertenece a la sintaxis esperada.

### Error sintactico

Ocurre cuando los tokens existen, pero estan organizados de una forma que no cumple la gramatica.

Ejemplo:

```text
datos abrir "ventas.csv";
```

Falta el operador de asignacion `:=`.

### Error semantico

Ocurre cuando la instruccion esta bien escrita, pero no puede ejecutarse correctamente.

Ejemplo:

```text
resultado := variable_inexistente
-> tomar [precio];
```

La variable `variable_inexistente` no fue declarada.

---

# Reglas semanticas

## 1. Variables declaradas

Una variable debe existir antes de ser utilizada.

Ejemplo valido:

```text
datos := abrir "datos/ventas.csv";

resultado := datos
-> tomar [producto, precio];
```

Ejemplo invalido:

```text
resultado := ventas
-> tomar [producto, precio];
```

Si `ventas` nunca fue creada, se genera:

```text
VariableNoDefinidaError
```

---

## 2. Columnas existentes

Toda columna utilizada en una operacion debe existir dentro del conjunto de datos.

Ejemplo:

```text
resultado := datos
-> tomar [producto, precio];
```

Esto solo es valido si las columnas `producto` y `precio` existen.

Si se escribe:

```text
resultado := datos
-> tomar [producto, dinosaurio];
```

y `dinosaurio` no existe, se genera:

```text
ColumnaNoExisteError
```

---

## 3. Apertura de archivos

El archivo indicado en la instruccion `abrir` debe existir.

Ejemplo:

```text
datos := abrir "datos/ventas.csv";
```

Si el archivo no existe, se genera:

```text
ArchivoNoExisteError
```

---

## 4. Seleccion de columnas

La instruccion `tomar` recibe una o varias columnas.

Ejemplo:

```text
resultado := datos
-> tomar [ciudad, producto, precio];
```

Todas las columnas indicadas deben existir.

La operacion devuelve un nuevo conjunto de datos y no modifica directamente el conjunto original.

---

## 5. Filtros

La instruccion `cuando` debe producir una condicion booleana.

Ejemplo:

```text
resultado := datos
-> cuando precio > 100;
```

Cada fila se evalua usando la condicion.

Las filas donde la condicion sea verdadera se conservan.

Tambien se permiten operadores logicos:

```text
resultado := datos
-> cuando precio > 100 y cantidad > 0;
```

---

## 6. Operadores relacionales

DataDSL permite:

```text
>
<
>=
<=
==
!=
```

Estos operadores se utilizan principalmente para construir condiciones.

Ejemplo:

```text
precio >= 100
```

---

## 7. Operadores logicos

DataDSL permite:

```text
y
o
```

Ejemplo:

```text
precio > 100 y cantidad > 0
```

El operador `y` requiere que ambas condiciones sean verdaderas.

El operador `o` requiere que al menos una condicion sea verdadera.

---

## 8. Operadores aritmeticos

DataDSL permite:

```text
+
-
*
/
%
^
```

Estos operadores pueden utilizarse para crear expresiones y columnas calculadas.

Ejemplo:

```text
cantidad * precio
```

---

## 9. Creacion de columnas

La instruccion `crear` permite generar una nueva columna.

Ejemplo:

```text
resultado := datos
-> crear total := cantidad * precio;
```

Las columnas utilizadas en la expresion deben existir.

La nueva columna se agrega al conjunto de datos resultante.

---

## 10. Ordenamiento

La instruccion `ordenar` permite ordenar los registros usando una columna.

Ejemplo:

```text
resultado := datos
-> ordenar por precio asc;
```

Tambien:

```text
resultado := datos
-> ordenar por precio desc;
```

La columna indicada debe existir.

Si no se indica `asc` o `desc`, se utiliza orden ascendente.

---

## 11. Valores faltantes

### Rellenar valores

La instruccion:

```text
-> rellenar precio con 0
```

reemplaza los valores faltantes de la columna `precio` por `0`.

La columna debe existir.

### Eliminar valores faltantes

La instruccion:

```text
-> eliminar_nulos [precio, cantidad]
```

elimina las filas que tengan valores faltantes en alguna de las columnas indicadas.

---

## 12. Agrupamiento

La instruccion `agrupar` organiza los datos en grupos.

Ejemplo:

```text
-> agrupar por [ciudad]
```

La columna o columnas utilizadas para agrupar deben existir.

El resultado se utiliza posteriormente para realizar agregaciones.

---

## 13. Agregaciones

Despues de agrupar se pueden calcular estadisticas.

Ejemplo:

```text
-> resumir ingreso := suma(total),
           promedio := media(total),
           registros := contar()
```

Las funciones disponibles son:

```text
suma(columna)
media(columna)
mediana(columna)
minimo(columna)
maximo(columna)
desviacion(columna)
contar()
```

Las funciones que reciben una columna requieren que esa columna exista.

---

## 14. Exportacion

La instruccion `guardar` permite exportar un conjunto de datos a CSV.

Ejemplo:

```text
guardar resumen como "salidas/resumen.csv";
```

La variable indicada debe existir.

El resultado se guarda utilizando formato CSV.

---

## 15. Tipos incompatibles

Algunas operaciones requieren datos compatibles.

Por ejemplo:

```text
cantidad * precio
```

espera normalmente valores numericos.

Si una operacion no puede realizarse debido al tipo de los datos, DataDSL debe producir un error semantico.

El error utilizado es:

```text
TipoIncompatibleError
```

---

## 16. Operaciones no permitidas

Si una instruccion es sintacticamente valida pero no puede ejecutarse correctamente, se utiliza:

```text
OperacionNoPermitidaError
```

Esto permite diferenciar los problemas de ejecucion de los errores de sintaxis.

---

# Flujo de validacion

El proceso general es:

```text
Programa DataDSL
        |
        v
Lexer
        |
        v
Parser
        |
        v
Arbol sintactico
        |
        v
Visitor
        |
        v
Validaciones semanticas
        |
        v
MotorDatos
        |
        v
Resultado
```

ANTLR comprueba principalmente la estructura del lenguaje.

El Visitor y las clases de soporte comprueban que las operaciones tengan sentido y luego ejecutan el procesamiento de datos.

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

guardar resumen como "salidas/resumen.csv";
```

En este ejemplo DataDSL debe validar:

1. Que el archivo exista.
2. Que `datos` haya sido creado.
3. Que las columnas utilizadas existan.
4. Que el filtro pueda evaluarse.
5. Que la columna `total` pueda calcularse.
6. Que `ciudad` pueda utilizarse para agrupar.
7. Que `total` exista antes de calcular sus estadisticas.
8. Que `resumen` exista antes de exportarlo.
