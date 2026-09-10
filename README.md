# DataDSL

Proyecto de Lenguajes de Programacion y Transduccion.

DataDSL es un lenguaje de dominio especifico orientado a operaciones basicas de ciencia de datos.

Esta primera fase se enfoca en la definicion de la sintaxis del lenguaje, la construccion del lexer y parser con ANTLR4 y la validacion de programas correctos e incorrectos.

## Sintaxis general

Un ejemplo de programa escrito en DataDSL es:

```text
datos := abrir "ventas.csv";

ventas := datos
-> tomar [ciudad, producto, precio]
-> cuando precio > 100;

mostrar barras de ventas;
```

## Funcionalidades de esta fase

Actualmente el lenguaje reconoce:

- Asignaciones.
- Apertura de archivos CSV.
- Seleccion de columnas.
- Filtros con condiciones.
- Expresiones aritmeticas.
- Comparaciones.
- Operadores logicos.
- Encadenamiento de operaciones con `->`.
- Instrucciones de visualizacion.

La instruccion de visualizacion solo se reconoce de forma sintactica. En esta fase no se genera una grafica real.

## Estructura del proyecto

```text
DataDSL/
|
|-- grammar/
|   `-- DataDSL.g4
|
|-- ejemplos/
|   |-- correcto1.dsl
|   |-- correcto2.dsl
|   |-- correcto3.dsl
|   |-- incorrecto1.dsl
|   `-- incorrecto2.dsl
|
|-- docs/
|   |-- alcance.md
|   |-- instrucciones.md
|   `-- gramatica_ebnf.md
|
|-- generated/
|
|-- ErrorListener.py
|-- main.py
`-- README.md
```

## Requisitos

Para ejecutar el proyecto se necesita:

- Python 3.11 o superior.
- Java.
- ANTLR4.
- Runtime de ANTLR para Python.

Instalar el runtime de ANTLR con:

```bash
pip install antlr4-python3-runtime==4.13.2
```

## Generar Lexer y Parser

Desde la carpeta principal del proyecto, entrar a `grammar`:

```bash
cd grammar
```

Generar los archivos de ANTLR para Python:

```bash
antlr4 -Dlanguage=Python3 -visitor -o ../generated DataDSL.g4
```

Volver a la carpeta principal:

```bash
cd ..
```

ANTLR genera automaticamente archivos como:

```text
DataDSLLexer.py
DataDSLParser.py
DataDSLListener.py
DataDSLVisitor.py
```

Estos archivos se guardan en la carpeta `generated`.

## Ejecutar el programa

Para probar un archivo correcto:

```bash
python main.py ejemplos/correcto1.dsl
```

Tambien se pueden ejecutar:

```bash
python main.py ejemplos/correcto2.dsl
```

```bash
python main.py ejemplos/correcto3.dsl
```

Si el programa cumple la gramatica, la salida muestra:

```text
Programa valido

Arbol de analisis:

(programa ...)
```

## Probar errores

Para probar un archivo incorrecto:

```bash
python main.py ejemplos/incorrecto1.dsl
```

o:

```bash
python main.py ejemplos/incorrecto2.dsl
```

El programa muestra la linea y la columna donde ANTLR encuentra el error.

Ejemplo:

```text
Error en linea 1, columna 6: ...
```

## Documentacion

La carpeta `docs` contiene la documentacion principal del lenguaje:

- `alcance.md`: describe el objetivo, usuarios, entradas, salidas y limitaciones de la primera fase.
- `catalogo_instrucciones.md`: explica las instrucciones y operadores disponibles.
- `gramatica_ebnf.md`: contiene la definicion formal de la sintaxis antes de su implementacion en ANTLR4.

## Estado actual

Esta version corresponde a la primera fase del proyecto.

El sistema permite reconocer programas escritos en DataDSL, generar su arbol de analisis sintactico y detectar errores lexicos o sintacticos.

El procesamiento real de datos, la tabla de simbolos, el Visitor y la generacion de visualizaciones corresponden a las siguientes fases del proyecto.
