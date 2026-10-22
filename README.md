# DataDSL

Hecho por Johan Steven Galeano Gonzalez

Proyecto de Lenguajes de Programacion y Transduccion.

DataDSL es un lenguaje de dominio especifico orientado a operaciones de ciencia de datos.

En el segundo corte, el proyecto incorpora semantica y procesamiento real de datos mediante el patron Visitor, una tabla de simbolos y un motor de procesamiento implementado con pandas.

---

# Objetivo del segundo corte

El objetivo es que DataDSL deje de limitarse al reconocimiento sintactico y pueda ejecutar operaciones reales sobre datos.

La version actual permite:

- Cargar archivos CSV.
- Guardar variables en una tabla de simbolos.
- Seleccionar columnas.
- Filtrar registros.
- Ordenar datos.
- Crear columnas calculadas.
- Tratar valores faltantes.
- Agrupar datos.
- Calcular estadisticas descriptivas.
- Exportar resultados a CSV.
- Detectar errores semanticos.

---

# Ejemplo de programa

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

---

# Arquitectura general

```text
Programa .dsl
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
Tabla de simbolos
    |
    v
MotorDatos
    |
    v
pandas
    |
    v
Resultado / CSV
```

La responsabilidad de cada componente es:

- Lexer: convierte el texto en tokens.
- Parser: verifica la estructura del lenguaje.
- Visitor: interpreta el arbol sintactico.
- ContextoEjecucion: administra la tabla de simbolos.
- MotorDatos: ejecuta operaciones reales con pandas.
- ErroresSemanticos: controla errores durante la ejecucion.

---

# Estructura del proyecto

```text
proyecto/
|
|-- grammar/
|   `-- DataDSL.g4
|
|-- src/
|   |-- ContextoEjecucion.py
|   |-- DataDSLVisitorImpl.py
|   |-- ErroresSemanticos.py
|   `-- MotorDatos.py
|
|-- datos/
|   `-- ventas.csv
|
|-- ejemplos/
|   |-- correcto1.dsl
|   |-- correcto2.dsl
|   |-- correcto3.dsl
|   |-- incorrecto1.dsl
|   |-- incorrecto2.dsl
|   |-- programa1.dsl
|   |-- programa2.dsl
|   `-- programa3.dsl
|
|-- tests/
|   |-- test_carga.py
|   |-- test_filtros.py
|   |-- test_semantica.py
|   `-- test_integracion.py
|
|-- docs/
|   |-- alcance.md
|   |-- gramatica_ebnf.md
|   |-- instrucciones.md
|   `-- reglas_semanticas.md
|
|-- generated/
|
|-- ErrorListener.py
|-- main.py
`-- README.md
```

---

# Requisitos

Para ejecutar el proyecto se necesita:

- Python 3.11 o superior.
- Java.
- ANTLR4.
- pandas.
- pytest.
- Runtime de ANTLR para Python.

Instalar las dependencias de Python con:

```bash
pip install antlr4-python3-runtime==4.13.2 pandas pytest
```

---

# Generar Lexer, Parser y Visitor

ANTLR genera automaticamente los archivos necesarios a partir de:

```text
grammar/DataDSL.g4
```

Desde la carpeta principal del proyecto:

```bash
cd grammar
```

Ejecutar:

```bash
antlr4 -Dlanguage=Python3 -visitor -o ../generated DataDSL.g4
```

Volver a la raiz:

```bash
cd ..
```

ANTLR genera archivos como:

```text
DataDSLLexer.py
DataDSLParser.py
DataDSLListener.py
DataDSLVisitor.py
```

Estos archivos se guardan dentro de:

```text
generated/
```

---

# Ejecutar DataDSL

Para ejecutar un programa:

```bash
python main.py ejemplos/programa1.dsl
```

Tambien pueden ejecutarse:

```bash
python main.py ejemplos/programa2.dsl
```

```bash
python main.py ejemplos/programa3.dsl
```

El archivo `main.py` realiza el flujo completo:

```text
archivo .dsl
-> Lexer
-> Parser
-> Arbol
-> Visitor
-> MotorDatos
-> Resultado
```

---

# Programas completos

## programa1.dsl

Demuestra:

- Carga.
- Seleccion.
- Filtrado.
- Ordenamiento.
- Exportacion.

## programa2.dsl

Demuestra:

- Tratamiento de valores faltantes.
- Creacion de columnas.
- Ordenamiento.
- Exportacion.

## programa3.dsl

Demuestra:

- Carga.
- Seleccion.
- Filtrado.
- Columna calculada.
- Agrupamiento.
- Estadisticas.
- Exportacion.

Este programa es el ejemplo principal del segundo corte.

---

# Datos de prueba

El archivo:

```text
datos/ventas.csv
```

contiene datos reales de ejemplo con:

- Ciudad.
- Producto.
- Cantidad.
- Precio.

Tambien incluye un valor faltante para probar las operaciones de limpieza.

---

# Tabla de simbolos

La tabla de simbolos se encuentra en:

```text
src/ContextoEjecucion.py
```

Su funcion es relacionar los nombres escritos en DataDSL con objetos reales durante la ejecucion.

Ejemplo:

```text
datos -> DataFrame
ventas_limpias -> DataFrame
resumen -> DataFrame
```

---

# Motor de procesamiento

El archivo:

```text
src/MotorDatos.py
```

utiliza pandas para ejecutar operaciones como:

- `read_csv`
- seleccion de columnas
- filtros
- ordenamiento
- tratamiento de nulos
- agrupamiento
- agregaciones
- exportacion con `to_csv`

---

# Visitor

El archivo:

```text
src/DataDSLVisitorImpl.py
```

implementa el patron Visitor.

Su funcion es recorrer el arbol generado por ANTLR e interpretar cada instruccion.

Ejemplo:

```text
-> crear total := cantidad * precio
```

El Visitor reconoce la instruccion y solicita al MotorDatos que cree la nueva columna.

---

# Errores semanticos

El archivo:

```text
src/ErroresSemanticos.py
```

define errores como:

```text
VariableNoDefinidaError
ColumnaNoExisteError
TipoIncompatibleError
OperacionNoPermitidaError
ArchivoNoExisteError
```

Estos errores ocurren cuando una instruccion esta correctamente escrita, pero no puede ejecutarse de forma valida.

---

# Pruebas

El proyecto utiliza `pytest`.

Para ejecutar todas las pruebas:

```bash
pytest
```

Tambien puede usarse:

```bash
pytest -v
```

Las pruebas incluidas son:

```text
tests/test_carga.py
```

Verifica la carga de archivos CSV.

```text
tests/test_filtros.py
```

Verifica el filtrado de registros.

```text
tests/test_semantica.py
```

Verifica errores semanticos esperados.

```text
tests/test_integracion.py
```

Verifica un flujo completo de procesamiento.

La prueba de integracion realiza:

```text
cargar
-> seleccionar
-> filtrar
-> crear columna
-> agrupar
-> resumir
-> exportar
```

---

# Documentacion

La carpeta:

```text
docs/
```

contiene:

## alcance.md

Describe:

- Objetivo.
- Entradas.
- Salidas.
- Funcionalidades.
- Limitaciones.

## instrucciones.md

Documenta todas las instrucciones disponibles en DataDSL.

## gramatica_ebnf.md

Contiene la representacion formal del lenguaje en EBNF.

## reglas_semanticas.md

Explica las reglas semanticas y los errores que pueden aparecer durante la ejecucion.

---

# Resultado esperado del segundo corte

El objetivo principal es que DataDSL pueda procesar datos reales y generar una tabla resumen.

Un flujo completo debe ser capaz de:

```text
CSV de entrada
    |
    v
Carga
    |
    v
Transformacion
    |
    v
Filtrado
    |
    v
Agrupamiento
    |
    v
Estadisticas
    |
    v
CSV de salida
```

El resultado principal se puede exportar mediante:

```text
guardar resumen como "salidas/resumen_ciudades.csv";
```

---

# Estado actual

Esta version corresponde al segundo corte del proyecto.

Actualmente se encuentra implementada la estructura necesaria para:

- Semantica.
- Visitor.
- Tabla de simbolos.
- Procesamiento de datos.
- Validaciones semanticas.
- Pruebas unitarias.
- Prueba de integracion.
- Programas completos.
- Exportacion de resultados.

Las visualizaciones completas se desarrollaran principalmente en el tercer corte.
