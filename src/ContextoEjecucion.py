# ======================================================
# CONTEXTO DE EJECUCION / TABLA DE SIMBOLOS
# ======================================================
#
# Este archivo administra las variables creadas
# durante la ejecucion de un programa DataDSL.
#
# Ejemplo:
#
# datos := abrir "datos/ventas.csv";
#
# Internamente se guarda algo equivalente a:
#
# "datos" -> DataFrame
#
# La tabla de simbolos permite:
#
# - Guardar variables.
# - Consultar variables.
# - Verificar si una variable existe.
# - Evitar usar variables no declaradas.
#
# En resumen:
# este archivo funciona como la memoria del programa.
# ======================================================


class ContextoEjecucion:

    def __init__(self):

        # Diccionario que funciona como tabla de simbolos.
        #
        # Clave:
        # nombre de la variable escrita en DataDSL.
        #
        # Valor:
        # objeto real asociado a esa variable.
        #
        # Ejemplo:
        #
        # {
        #     "datos": DataFrame(...),
        #     "ventas": DataFrame(...),
        #     "resumen": DataFrame(...)
        # }

        self.simbolos = {}


    def guardar(self, nombre, valor):
        """
        Guarda una variable dentro de la tabla de simbolos.

        nombre:
        nombre utilizado dentro del programa DataDSL.

        valor:
        objeto real asociado a esa variable.
        """

        self.simbolos[nombre] = valor


    def obtener(self, nombre):
        """
        Recupera el valor asociado a una variable.

        Si la variable no existe se genera un error,
        porque no se puede utilizar una variable
        que nunca fue declarada.
        """

        if nombre not in self.simbolos:

            raise Exception(
                f"Error semantico: "
                f"la variable '{nombre}' no existe."
            )

        return self.simbolos[nombre]


    def existe(self, nombre):
        """
        Comprueba si una variable existe.

        Devuelve:

        True  -> la variable existe.
        False -> la variable no existe.
        """

        return nombre in self.simbolos


    def mostrar_simbolos(self):
        """
        Devuelve una lista con los nombres
        de todas las variables almacenadas.

        Puede utilizarse para depuracion
        o para mostrar la tabla de simbolos
        durante la sustentacion.
        """

        return list(
            self.simbolos.keys()
        )
