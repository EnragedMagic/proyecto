# Gramatica EBNF de DataDSL

## Objetivo

Este documento describe la estructura formal de DataDSL utilizando notacion EBNF.

La EBNF sirve para representar de forma clara como se construyen las instrucciones del lenguaje antes de llevarlas a ANTLR4.

En resumen:

- La EBNF describe la forma del lenguaje.
- `DataDSL.g4` implementa esa estructura en ANTLR4.
- El Parser verifica que los programas cumplan estas reglas.

---

# Gramatica

```ebnf
programa = { instruccion } ;

instruccion = asignacion, ";"
            | guardado, ";"
            | visualizacion, ";" ;

asignacion = identificador, ":=", contenido ;

contenido = lectura
          | flujo
          | expresion ;

lectura = "abrir", cadena ;

flujo = identificador, paso, { paso } ;

paso = "->", seleccion
     | "->", filtro
     | "->", ordenamiento
     | "->", columna_calculada
     | "->", rellenar_nulos
     | "->", eliminar_nulos
     | "->", agrupacion
     | "->", resumen ;

seleccion = "tomar", "[", columnas, "]" ;

columnas = identificador, { ",", identificador } ;

filtro = "cuando", expresion ;

ordenamiento = "ordenar", "por", identificador, [ "asc" | "desc" ] ;

columna_calculada = "crear", identificador, ":=", expresion ;

rellenar_nulos = "rellenar", identificador, "con", expresion ;

eliminar_nulos = "eliminar_nulos", "[", columnas, "]" ;

agrupacion = "agrupar", "por", "[", columnas, "]" ;

resumen = "resumir", agregacion, { ",", agregacion } ;

agregacion = identificador, ":=", funcion_agregacion ;

funcion_agregacion = "suma", "(", identificador, ")"
                   | "media", "(", identificador, ")"
                   | "mediana", "(", identificador, ")"
                   | "minimo", "(", identificador, ")"
                   | "maximo", "(", identificador, ")"
                   | "desviacion", "(", identificador, ")"
                   | "contar", "(", ")" ;

guardado = "guardar", identificador, "como", cadena ;

visualizacion = "mostrar", "barras", "de", identificador ;

expresion = expresion_logica ;

expresion_logica = comparacion, { ("y" | "o"), comparacion } ;

comparacion = suma,
              [ (">" | "<" | ">=" | "<=" | "==" | "!="), suma ] ;

suma = producto, { ("+" | "-"), producto } ;

producto = potencia, { ("*" | "/" | "%"), potencia } ;

potencia = valor, { "^", valor } ;

valor = numero
      | cadena
      | booleano
      | identificador
      | "(", expresion, ")" ;

booleano = "verdadero"
         | "falso" ;

identificador = (letra | "_"),
                { letra | digito | "_" } ;

numero = digito,
         { digito },
         [ ".", digito, { digito } ] ;

cadena = '"', { caracter }, '"' ;
```

---

# Explicacion de las reglas principales

## programa

Representa un archivo completo escrito en DataDSL.

Puede contener varias instrucciones.

Ejemplo:

```text
datos := abrir "datos/ventas.csv";

guardar datos como "salidas/copia.csv";
```

---

## instruccion

Una instruccion puede ser:

- Una asignacion.
- Una exportacion.
- Una instruccion de visualizacion.

Todas terminan con `;`.

---

## asignacion

Permite guardar un resultado dentro de una variable.

Ejemplo:

```text
datos := abrir "datos/ventas.csv";
```

La variable queda registrada en la tabla de simbolos.

---

## lectura

Representa la apertura de un archivo CSV.

Ejemplo:

```text
abrir "datos/ventas.csv"
```

---

## flujo

Permite aplicar varias operaciones de forma encadenada.

Ejemplo:

```text
ventas := datos
-> tomar [ciudad, precio]
-> cuando precio > 100;
```

Cada paso recibe como entrada el resultado del paso anterior.

---

## seleccion

Permite elegir una o varias columnas.

Ejemplo:

```text
-> tomar [ciudad, producto, precio]
```

---

## filtro

Permite conservar solo las filas que cumplan una condicion.

Ejemplo:

```text
-> cuando precio > 100
```

---

## ordenamiento

Permite ordenar los registros.

Ejemplo:

```text
-> ordenar por precio desc
```

La direccion puede ser `asc` o `desc`.

---

## columna_calculada

Permite crear una nueva columna a partir de una expresion.

Ejemplo:

```text
-> crear total := cantidad * precio
```

---

## rellenar_nulos

Permite reemplazar valores faltantes.

Ejemplo:

```text
-> rellenar precio con 0
```

---

## eliminar_nulos

Permite eliminar filas que tengan valores faltantes.

Ejemplo:

```text
-> eliminar_nulos [precio, cantidad]
```

---

## agrupacion

Permite agrupar registros usando una o varias columnas.

Ejemplo:

```text
-> agrupar por [ciudad]
```

---

## resumen

Permite definir una o varias agregaciones.

Ejemplo:

```text
-> resumir ingreso := suma(total),
           promedio := media(total),
           registros := contar()
```

---

## funcion_agregacion

Representa las operaciones estadisticas disponibles.

Funciones:

```text
suma(columna)
media(columna)
mediana(columna)
minimo(columna)
maximo(columna)
desviacion(columna)
contar()
```

---

## guardado

Permite exportar una variable a CSV.

Ejemplo:

```text
guardar resumen como "salidas/resumen.csv";
```

---

## visualizacion

Representa una instruccion de grafica.

Ejemplo:

```text
mostrar barras de resumen;
```

En el segundo corte se mantiene el reconocimiento sintactico de esta instruccion.

---

# Expresiones

## expresion_logica

Permite combinar comparaciones usando:

```text
y
o
```

Ejemplo:

```text
precio > 100 y cantidad > 0
```

---

## comparacion

Permite utilizar:

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

---

## suma

Permite:

```text
+
-
```

---

## producto

Permite:

```text
*
/
%
```

---

## potencia

Permite:

```text
^
```

Ejemplo:

```text
numero ^ 2
```

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

Este programa cumple la estructura definida por la gramatica EBNF y posteriormente puede ser reconocido por la gramatica ANTLR4.
