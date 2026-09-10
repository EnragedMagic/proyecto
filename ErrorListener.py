from antlr4.error.ErrorListener import ErrorListener


class DataDSLErrorListener(ErrorListener):

    def __init__(self):
        super().__init__()
        self.errores = []

    def syntaxError(
        self,
        recognizer,
        offendingSymbol,
        line,
        column,
        msg,
        e
    ):
        error = f"Error en linea {line}, columna {column}: {msg}"
        self.errores.append(error)
        print(error)
