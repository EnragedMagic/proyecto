# ======================================================
# ERRORES SEMANTICOS
# ======================================================
# SENTIDO - VALIDACION - ERRORES
# Este archivo define errores propios de DataDSL.
#
# Un error semantico ocurre cuando una instruccion
# esta bien escrita, pero no tiene sentido al ejecutarse.
#
# Ejemplos:
#
# - Usar una variable que no existe.
# - Pedir una columna que no existe.
# - Aplicar una operacion a un tipo de dato incorrecto.
# - Intentar guardar o procesar un resultado invalido.
#
# En resumen:
# la sintaxis puede ser correcta, pero el significado
# de la instruccion puede ser incorrecto.
# ======================================================


class ErrorSemantico(Exception):
    """
    Clase base para todos los errores semanticos de DataDSL.

    Hereda de Exception para poder detener la ejecucion
    cuando se encuentra una operacion invalida.
    """

    pass


class VariableNoDefinidaError(ErrorSemantico):
    """
    Se produce cuando el programa intenta usar
    una variable que nunca fue declarada.

    Ejemplo:

    resultado := datos_inexistentes
    -> tomar [precio];
    """

    def __init__(self, nombre):
        mensaje = (
            f"Error semantico: la variable '{nombre}' "
            f"no ha sido definida."
        )

        super().__init__(mensaje)


class ColumnaNoExisteError(ErrorSemantico):
    """
    Se produce cuando se intenta utilizar una columna
    que no existe dentro del conjunto de datos.

    Ejemplo:

    datos := abrir "ventas.csv";

    resultado := datos
    -> tomar [columna_inexistente];
    """

    def __init__(self, columna):
        mensaje = (
            f"Error semantico: la columna '{columna}' "
            f"no existe en el conjunto de datos."
        )

        super().__init__(mensaje)


class TipoIncompatibleError(ErrorSemantico):
    """
    Se produce cuando una operacion intenta trabajar
    con un tipo de dato que no es compatible.

    Ejemplo:

    intentar hacer una operacion numerica sobre
    una columna de texto.
    """

    def __init__(self, mensaje):
        super().__init__(
            f"Error semantico: tipo incompatible. {mensaje}"
        )


class OperacionNoPermitidaError(ErrorSemantico):
    """
    Se produce cuando una operacion no puede realizarse
    sobre los datos actuales.

    Este error sirve para controlar casos que sean
    validos sintacticamente pero invalidos durante
    la ejecucion.
    """

    def __init__(self, mensaje):
        super().__init__(
            f"Error semantico: operacion no permitida. {mensaje}"
        )


class ArchivoNoExisteError(ErrorSemantico):
    """
    Se produce cuando DataDSL intenta abrir
    un archivo CSV que no existe.

    Ejemplo:

    datos := abrir "archivo_que_no_existe.csv";
    """

    def __init__(self, ruta):
        mensaje = (
            f"Error semantico: no se encontro "
            f"el archivo '{ruta}'."
        )

        super().__init__(mensaje)
