# ======================================================
# PROGRAMA PRINCIPAL DE DATADSL
# ======================================================
#
# Este archivo es el punto de entrada del proyecto.
#
# Se encarga de:
#
# 1. Leer un archivo .dsl.
# 2. Enviarlo al Lexer.
# 3. Enviarlo al Parser.
# 4. Detectar errores lexicos o sintacticos.
# 5. Generar el arbol de analisis.
# 6. Ejecutar el Visitor.
# 7. Procesar realmente los datos.
#
# En resumen:
# este archivo conecta todo el proyecto.
# ======================================================


import sys
import os

from antlr4 import FileStream
from antlr4 import CommonTokenStream


# ------------------------------------------------------
# CARPETA GENERATED
# ------------------------------------------------------
#
# ANTLR genera automaticamente el Lexer, Parser y Visitor
# dentro de la carpeta "generated".
#
# Esta linea permite que Python pueda importar
# esos archivos generados.
# ------------------------------------------------------

sys.path.insert(
    0,
    os.path.join(
        os.path.dirname(__file__),
        "generated"
    )
)


# Archivos generados automaticamente por ANTLR.
from DataDSLLexer import DataDSLLexer
from DataDSLParser import DataDSLParser


# Manejo de errores lexicos y sintacticos.
from ErrorListener import DataDSLErrorListener


# Visitor implementado por nosotros.
from src.DataDSLVisitorImpl import DataDSLVisitorImpl


# Errores semanticos propios de DataDSL.
from src.ErroresSemanticos import ErrorSemantico


def analizar_archivo(ruta):

    # --------------------------------------------------
    # 1. LEER ARCHIVO DSL
    # --------------------------------------------------

    entrada = FileStream(
        ruta,
        encoding="utf-8"
    )


    # --------------------------------------------------
    # 2. LEXER
    # --------------------------------------------------
    #
    # El Lexer transforma el texto en tokens.
    #
    # Ejemplo:
    #
    # datos := abrir "ventas.csv";
    #
    # se transforma aproximadamente en:
    #
    # ID ASIGNAR ABRIR STRING FIN
    # --------------------------------------------------

    lexer = DataDSLLexer(
        entrada
    )

    errores_lexer = DataDSLErrorListener()

    lexer.removeErrorListeners()
    lexer.addErrorListener(
        errores_lexer
    )


    # --------------------------------------------------
    # 3. TOKENS
    # --------------------------------------------------

    tokens = CommonTokenStream(
        lexer
    )


    # --------------------------------------------------
    # 4. PARSER
    # --------------------------------------------------
    #
    # El Parser verifica que los tokens cumplan
    # las reglas definidas en DataDSL.g4.
    # --------------------------------------------------

    parser = DataDSLParser(
        tokens
    )

    errores_parser = DataDSLErrorListener()

    parser.removeErrorListeners()
    parser.addErrorListener(
        errores_parser
    )


    # --------------------------------------------------
    # 5. GENERAR ARBOL SINTACTICO
    # --------------------------------------------------

    arbol = parser.programa()


    # --------------------------------------------------
    # 6. CONTAR ERRORES
    # --------------------------------------------------

    total_errores = (
        len(errores_lexer.errores)
        +
        len(errores_parser.errores)
    )


    # --------------------------------------------------
    # 7. SI HAY ERRORES, NO SE EJECUTA
    # --------------------------------------------------

    if total_errores > 0:

        print()

        print(
            f"El programa contiene "
            f"{total_errores} error(es)."
        )

        return


    # --------------------------------------------------
    # 8. PROGRAMA SINTACTICAMENTE VALIDO
    # --------------------------------------------------

    print(
        "Programa sintacticamente valido."
    )

    print()


    # --------------------------------------------------
    # 9. MOSTRAR ARBOL
    # --------------------------------------------------
    #
    # Esto ayuda a demostrar durante la sustentacion
    # como ANTLR interpreto el programa.
    # --------------------------------------------------

    print(
        "Arbol de analisis:"
    )

    print()

    print(
        arbol.toStringTree(
            recog=parser
        )
    )

    print()


    # --------------------------------------------------
    # 10. EJECUTAR VISITOR
    # --------------------------------------------------
    #
    # Una vez sabemos que la sintaxis es valida,
    # el Visitor recorre el arbol y ejecuta
    # la semantica del lenguaje.
    # --------------------------------------------------

    visitor = DataDSLVisitorImpl()

    try:

        visitor.visit(
            arbol
        )

        print()

        print(
            "Ejecucion finalizada correctamente."
        )


    # --------------------------------------------------
    # ERROR SEMANTICO
    # --------------------------------------------------
    #
    # Aqui llegan errores como:
    #
    # - Variable inexistente.
    # - Columna inexistente.
    # - Archivo inexistente.
    # - Operacion no permitida.
    # --------------------------------------------------

    except ErrorSemantico as error:

        print()

        print(
            str(error)
        )


    # --------------------------------------------------
    # ERROR INESPERADO
    # --------------------------------------------------
    #
    # Sirve como proteccion adicional por si aparece
    # algun problema que todavia no haya sido controlado.
    # --------------------------------------------------

    except Exception as error:

        print()

        print(
            f"Error inesperado: {error}"
        )


# ======================================================
# PUNTO DE ENTRADA
# ======================================================
#
# Esta parte se ejecuta cuando usamos:
#
# python main.py archivo.dsl
# ======================================================

if __name__ == "__main__":

    # Debe recibirse exactamente un archivo.
    if len(sys.argv) != 2:

        print(
            "Uso: python main.py archivo.dsl"
        )

        sys.exit(1)


    archivo = sys.argv[1]


    # Verificar que el archivo DSL exista.
    if not os.path.exists(
        archivo
    ):

        print(
            f"El archivo '{archivo}' no existe."
        )

        sys.exit(1)


    analizar_archivo(
        archivo
    )
