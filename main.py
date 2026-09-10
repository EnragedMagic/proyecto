import sys
import os

from antlr4 import FileStream
from antlr4 import CommonTokenStream

sys.path.insert(
    0,
    os.path.join(
        os.path.dirname(__file__),
        "generated"
    )
)

from DataDSLLexer import DataDSLLexer
from DataDSLParser import DataDSLParser
from ErrorListener import DataDSLErrorListener


def analizar_archivo(ruta):

    entrada = FileStream(
        ruta,
        encoding="utf-8"
    )

    lexer = DataDSLLexer(entrada)

    errores_lexer = DataDSLErrorListener()
    lexer.removeErrorListeners()
    lexer.addErrorListener(errores_lexer)

    tokens = CommonTokenStream(lexer)

    parser = DataDSLParser(tokens)

    errores_parser = DataDSLErrorListener()
    parser.removeErrorListeners()
    parser.addErrorListener(errores_parser)

    arbol = parser.programa()

    total_errores = (
        len(errores_lexer.errores)
        + len(errores_parser.errores)
    )

    if total_errores == 0:
        print("Programa valido")
        print()
        print("Arbol de analisis:")
        print()
        print(
            arbol.toStringTree(
                recog=parser
            )
        )

    else:
        print()
        print(
            f"El programa contiene {total_errores} error(es)."
        )


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Uso: python main.py archivo.dsl")
        sys.exit(1)

    archivo = sys.argv[1]

    if not os.path.exists(archivo):
        print("El archivo no existe.")
        sys.exit(1)

    analizar_archivo(archivo)
