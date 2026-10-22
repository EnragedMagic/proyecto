grammar DataDSL;

// ======================================================
// GRAMATICA - SINTAXIS - RECONOCIMIENTO
// Este archivo define la gramatica de DataDSL usando ANTLR4
// Sirve para indicar que estructuras son validas dentro del lenguaje
// ANTLR usa esa gramatica para generar el lexer y el parser, y luego el visitor interpreta 
// El arbol generado para ejecutar las operaciones sobre los datos
// ======================================================


// Un programa puede contener cero o mas instrucciones.
// EOF significa que ANTLR debe llegar correctamente
// hasta el final del archivo.
programa
    : instruccion* EOF
    ;


// Cada instruccion termina con punto y coma.
// En el segundo corte agregamos "guardar" para exportar CSV.
instruccion
    : asignacion FIN
    | guardado FIN
    | visualizacion FIN
    ;


// Una asignacion guarda un resultado dentro de una variable.
//
// Ejemplo:
// datos := abrir "ventas.csv";
//
// Ejemplo:
// ventas := datos -> tomar [ciudad, precio];
asignacion
    : ID ASIGNAR contenido
    ;


// El contenido de una variable puede venir de:
// 1. La lectura de un CSV.
// 2. Un flujo de transformaciones.
// 3. Una expresion.
contenido
    : lectura
    | flujo
    | expresion
    ;


// Permite cargar un archivo CSV.
//
// Ejemplo:
// datos := abrir "datos/ventas.csv";
lectura
    : ABRIR STRING
    ;


// Un flujo comienza con una variable existente
// y aplica una o mas operaciones usando ->
//
// Ejemplo:
// ventas := datos
// -> tomar [ciudad, precio]
// -> cuando precio > 100;
flujo
    : ID paso+
    ;


// Cada "paso" representa una transformacion
// que se aplicara sobre un conjunto de datos.
//
// Estas son las operaciones principales del segundo corte.
paso
    : FLECHA seleccion
    | FLECHA filtro
    | FLECHA ordenamiento
    | FLECHA columnaCalculada
    | FLECHA rellenarNulos
    | FLECHA eliminarNulos
    | FLECHA agrupacion
    | FLECHA resumen
    ;


// ======================================================
// OPERACIONES SOBRE LOS DATOS
// ======================================================


// Selecciona un grupo de columnas.
//
// Ejemplo:
// -> tomar [ciudad, producto, precio]
seleccion
    : TOMAR CORCHETE_IZQ columnas CORCHETE_DER
    ;


// Lista de una o varias columnas separadas por coma.
//
// Ejemplo:
// ciudad, producto, precio
columnas
    : ID (COMA ID)*
    ;


// Filtra registros utilizando una expresion.
//
// Ejemplo:
// -> cuando precio > 100
//
// Ejemplo:
// -> cuando precio > 100 y cantidad > 0
filtro
    : CUANDO expresion
    ;


// Ordena los registros usando una columna.
//
// Ejemplo:
// -> ordenar por precio
//
// Tambien puede indicarse el sentido:
//
// -> ordenar por precio asc
// -> ordenar por precio desc
ordenamiento
    : ORDENAR POR ID (ASC | DESC)?
    ;


// Permite crear una nueva columna calculada.
//
// Ejemplo:
// -> crear total := cantidad * precio
columnaCalculada
    : CREAR ID ASIGNAR expresion
    ;


// Permite reemplazar valores faltantes de una columna.
//
// Ejemplo:
// -> rellenar precio con 0
rellenarNulos
    : RELLENAR ID CON expresion
    ;


// Permite eliminar filas que tengan valores faltantes
// en una o varias columnas.
//
// Ejemplo:
// -> eliminar_nulos [precio, cantidad]
eliminarNulos
    : ELIMINAR_NULOS CORCHETE_IZQ columnas CORCHETE_DER
    ;


// Agrupa los datos por una o varias columnas.
//
// Ejemplo:
// -> agrupar por [ciudad]
agrupacion
    : AGRUPAR POR CORCHETE_IZQ columnas CORCHETE_DER
    ;


// "resumir" define una o varias estadisticas
// que se calcularan sobre los datos.
//
// Ejemplo:
// -> resumir ingreso := suma(total),
//            promedio := media(total),
//            registros := contar()
resumen
    : RESUMIR agregacion (COMA agregacion)*
    ;


// Una agregacion guarda el resultado de una funcion
// estadistica con un nombre.
//
// Ejemplo:
// ingreso := suma(total)
agregacion
    : ID ASIGNAR funcionAgregacion
    ;


// Funciones disponibles para resumir datos.
//
// Algunas necesitan una columna:
// suma(total)
// media(precio)
//
// contar() no necesita columna.
funcionAgregacion
    : SUMA PAREN_IZQ ID PAREN_DER
    | MEDIA PAREN_IZQ ID PAREN_DER
    | MEDIANA PAREN_IZQ ID PAREN_DER
    | MINIMO PAREN_IZQ ID PAREN_DER
    | MAXIMO PAREN_IZQ ID PAREN_DER
    | DESVIACION PAREN_IZQ ID PAREN_DER
    | CONTAR PAREN_IZQ PAREN_DER
    ;


// Guarda un conjunto de datos en un archivo CSV.
//
// Ejemplo:
// guardar resumen como "salidas/resumen.csv";
guardado
    : GUARDAR ID COMO STRING
    ;


// La visualizacion continua siendo reconocida.
// La implementacion completa de graficas corresponde
// principalmente al tercer corte.
//
// Ejemplo:
// mostrar barras de resumen;
visualizacion
    : MOSTRAR BARRAS DE ID
    ;


// ======================================================
// EXPRESIONES
// ======================================================


// Punto de entrada para las expresiones.
expresion
    : expresionLogica
    ;


// Permite operadores logicos.
//
// Ejemplo:
// precio > 100 y cantidad > 0
expresionLogica
    : comparacion ((Y | O) comparacion)*
    ;


// Permite comparaciones.
//
// Ejemplos:
// precio > 100
// ciudad == "Bogota"
comparacion
    : suma ((MAYOR
           | MENOR
           | MAYOR_IGUAL
           | MENOR_IGUAL
           | IGUAL
           | DIFERENTE) suma)?
    ;


// Suma y resta.
//
// Ejemplo:
// precio + impuesto
suma
    : producto ((MAS | MENOS) producto)*
    ;


// Multiplicacion, division y modulo.
//
// Ejemplo:
// cantidad * precio
producto
    : potencia ((MULTIPLICAR | DIVIDIR | MODULO) potencia)*
    ;


// Potencia.
//
// Ejemplo:
// numero ^ 2
potencia
    : valor (POTENCIA valor)*
    ;


// Valores basicos que pueden aparecer en una expresion.
valor
    : NUMBER
    | STRING
    | VERDADERO
    | FALSO
    | ID
    | PAREN_IZQ expresion PAREN_DER
    ;


// ======================================================
// TOKENS / PALABRAS RESERVADAS
// El lexer convierte el texto en unidades llamadas tokens.
// Las palabras reservadas deben aparecer antes de ID.
// ======================================================

ABRIR
    : 'abrir'
    ;

TOMAR
    : 'tomar'
    ;

CUANDO
    : 'cuando'
    ;

ORDENAR
    : 'ordenar'
    ;

POR
    : 'por'
    ;

ASC
    : 'asc'
    ;

DESC
    : 'desc'
    ;

CREAR
    : 'crear'
    ;

RELLENAR
    : 'rellenar'
    ;

CON
    : 'con'
    ;

ELIMINAR_NULOS
    : 'eliminar_nulos'
    ;

AGRUPAR
    : 'agrupar'
    ;

RESUMIR
    : 'resumir'
    ;

GUARDAR
    : 'guardar'
    ;

COMO
    : 'como'
    ;

MOSTRAR
    : 'mostrar'
    ;

BARRAS
    : 'barras'
    ;

DE
    : 'de'
    ;

SUMA
    : 'suma'
    ;

MEDIA
    : 'media'
    ;

MEDIANA
    : 'mediana'
    ;

MINIMO
    : 'minimo'
    ;

MAXIMO
    : 'maximo'
    ;

DESVIACION
    : 'desviacion'
    ;

CONTAR
    : 'contar'
    ;

VERDADERO
    : 'verdadero'
    ;

FALSO
    : 'falso'
    ;

Y
    : 'y'
    ;

O
    : 'o'
    ;


// ======================================================
// OPERADORES Y SIMBOLOS
// ======================================================

FLECHA
    : '->'
    ;

ASIGNAR
    : ':='
    ;

MAYOR_IGUAL
    : '>='
    ;

MENOR_IGUAL
    : '<='
    ;

IGUAL
    : '=='
    ;

DIFERENTE
    : '!='
    ;

MAYOR
    : '>'
    ;

MENOR
    : '<'
    ;

MAS
    : '+'
    ;

MENOS
    : '-'
    ;

MULTIPLICAR
    : '*'
    ;

DIVIDIR
    : '/'
    ;

MODULO
    : '%'
    ;

POTENCIA
    : '^'
    ;

PAREN_IZQ
    : '('
    ;

PAREN_DER
    : ')'
    ;

CORCHETE_IZQ
    : '['
    ;

CORCHETE_DER
    : ']'
    ;

COMA
    : ','
    ;

FIN
    : ';'
    ;


// ======================================================
// LITERALES E IDENTIFICADORES
// ======================================================


// Numero entero o decimal.
//
// Ejemplos:
// 10
// 25.5
NUMBER
    : [0-9]+ ('.' [0-9]+)?
    ;


// Texto entre comillas dobles.
//
// Ejemplo:
// "ventas.csv"
STRING
    : '"' (~["\r\n])* '"'
    ;


// Nombre utilizado para variables y columnas.
//
// Ejemplos:
// datos
// ventas_limpias
// precio2026
ID
    : [a-zA-Z_] [a-zA-Z0-9_]*
    ;


// Los comentarios que empiezan con # son ignorados
// por el lexer.
//
// Ejemplo:
// # Este es un comentario
COMENTARIO
    : '#' ~[\r\n]* -> skip
    ;


// Los espacios, saltos de linea y tabulaciones
// tambien son ignorados.
ESPACIO
    : [ \t\r\n]+ -> skip
    ;
