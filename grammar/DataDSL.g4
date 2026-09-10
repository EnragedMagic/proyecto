grammar DataDSL;

programa
    : instruccion* EOF
    ;

instruccion
    : asignacion FIN
    | visualizacion FIN
    ;

asignacion
    : ID ASIGNAR contenido
    ;

contenido
    : lectura
    | flujo
    | expresion
    ;

lectura
    : ABRIR STRING
    ;

flujo
    : ID paso+
    ;

paso
    : FLECHA seleccion
    | FLECHA filtro
    ;

seleccion
    : TOMAR CORCHETE_IZQ columnas CORCHETE_DER
    ;

columnas
    : ID (COMA ID)*
    ;

filtro
    : CUANDO expresion
    ;

visualizacion
    : MOSTRAR BARRAS DE ID
    ;

expresion
    : expresionLogica
    ;

expresionLogica
    : comparacion ((Y | O) comparacion)*
    ;

comparacion
    : suma ((MAYOR | MENOR | MAYOR_IGUAL | MENOR_IGUAL | IGUAL | DIFERENTE) suma)?
    ;

suma
    : producto ((MAS | MENOS) producto)*
    ;

producto
    : valor ((MULTIPLICAR | DIVIDIR) valor)*
    ;

valor
    : NUMBER
    | STRING
    | VERDADERO
    | FALSO
    | ID
    | PAREN_IZQ expresion PAREN_DER
    ;

ABRIR
    : 'abrir'
    ;

TOMAR
    : 'tomar'
    ;

CUANDO
    : 'cuando'
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

NUMBER
    : [0-9]+ ('.' [0-9]+)?
    ;

STRING
    : '"' (~["\r\n])* '"'
    ;

ID
    : [a-zA-Z_] [a-zA-Z0-9_]*
    ;

COMENTARIO
    : '#' ~[\r\n]* -> skip
    ;

ESPACIO
    : [ \t\r\n]+ -> skip
    ;
