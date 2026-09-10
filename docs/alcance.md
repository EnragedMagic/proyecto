# Alcance del proyecto

## MagicDSL

DataDSL

## Descripcion general

DataDSL es un lenguaje de dominio especifico orientado a tareas basicas de ciencia de datos.

El lenguaje busca permitir que un usuario pueda escribir instrucciones sencillas para trabajar con conjuntos de datos sin tener que programar directamente en Python.

En esta primera fase el proyecto se concentra en definir la sintaxis del lenguaje y construir el analizador lexico y sintactico usando ANTLR4.

## Usuarios

DataDSL esta pensado principalmente para estudiantes o usuarios que necesiten realizar operaciones sencillas sobre datos usando instrucciones faciles de leer.

No se busca reemplazar Python ni librerias como pandas, sino ofrecer una sintaxis mas simple para expresar operaciones comunes.

## Entradas

El sistema recibe archivos con extension `.dsl`.

Dentro de estos archivos el usuario puede escribir instrucciones como:

- Abrir un archivo CSV.
- Asignar datos a una variable.
- Seleccionar columnas.
- Aplicar filtros.
- Usar expresiones basicas.
- Definir una instruccion de visualizacion.

Ejemplo:

```text
datos := abrir "ventas.csv";

ventas := datos
-> tomar [ciudad, producto, precio]
-> cuando precio > 100;

mostrar barras de ventas;
```

## Salidas

En esta primera fase el sistema no procesa realmente los datos.

La salida consiste en:

- Indicar si el programa escrito en DataDSL es valido.
- Generar el arbol de analisis sintactico.
- Detectar errores lexicos o sintacticos.
- Mostrar la linea y la columna donde ocurre un error.

## Funcionalidades incluidas

La primera version de DataDSL permite reconocer:

- Asignaciones.
- Numeros enteros y decimales.
- Cadenas de texto.
- Valores booleanos.
- Operadores aritmeticos.
- Operadores relacionales.
- Operadores logicos.
- Apertura de archivos CSV.
- Seleccion de columnas.
- Filtros con condiciones.
- Encadenamiento de operaciones.
- Instrucciones de visualizacion.

## Limitaciones de esta fase

En esta primera entrega:

- No se procesan realmente los archivos CSV.
- No se generan graficas.
- No se calculan estadisticas.
- No se implementan agrupaciones.
- No se usa todavia una tabla de simbolos completa.
- No se ejecutan transformaciones reales sobre los datos.

Estas funcionalidades corresponden a las siguientes fases del proyecto.
