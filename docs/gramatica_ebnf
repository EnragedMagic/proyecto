# Gramatica EBNF de DataDSL

La siguiente gramatica describe la estructura principal del lenguaje DataDSL en formato EBNF.

```ebnf
programa = { instruccion } ;

instruccion = asignacion, ";"
            | visualizacion, ";" ;

asignacion = identificador, ":=", contenido ;

contenido = lectura
          | flujo
          | expresion ;

lectura = "abrir", cadena ;

flujo = identificador, paso, { paso } ;

paso = "->", seleccion
     | "->", filtro ;

seleccion = "tomar", "[", columnas, "]" ;

columnas = identificador, { ",", identificador } ;

filtro = "cuando", expresion ;

visualizacion = "mostrar", "barras", "de", identificador ;

expresion = expresion_logica ;

expresion_logica = comparacion, { ("y" | "o"), comparacion } ;

comparacion = suma, [ (">" | "<" | ">=" | "<=" | "==" | "!="), suma ] ;

suma = producto, { ("+" | "-"), producto } ;

producto = valor, { ("*" | "/"), valor } ;

valor = numero
      | cadena
      | booleano
      | identificador
      | "(", expresion, ")" ;

booleano = "verdadero"
         | "falso" ;

identificador = (letra | "_"), { letra | digito | "_" } ;

numero = digito, { digito }, [ ".", digito, { digito } ] ;

cadena = '"', { caracter }, '"' ;
```

## Ejemplo de programa valido

```text
datos := abrir "ventas.csv";

ventas := datos
-> tomar [ciudad, producto, precio]
-> cuando precio > 100 y ciudad == "Bogota";

mostrar barras de ventas;
```

## Explicacion general

La regla `programa` permite que un archivo contenga varias instrucciones.

Una instruccion puede ser una asignacion o una visualizacion.

La regla `asignacion` utiliza `:=` para guardar un valor en una variable.

La regla `lectura` reconoce la apertura de un archivo CSV mediante la palabra `abrir`.

La regla `flujo` permite encadenar operaciones usando `->`.

Las operaciones disponibles en esta primera fase son `tomar` y `cuando`.

La regla `tomar` permite indicar una lista de columnas.

La regla `cuando` permite escribir una condicion.

La regla `visualizacion` reconoce una instruccion como:

```text
mostrar barras de ventas;
```

En esta primera fase esta instruccion solo se reconoce de forma sintactica y no genera una grafica real.

Las reglas de expresion permiten usar valores, identificadores, operaciones aritmeticas, comparaciones y operadores logicos.
