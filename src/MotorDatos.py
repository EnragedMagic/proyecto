# ======================================================
# MOTOR DE PROCESAMIENTO DE DATOS
# ======================================================
# Tablas - Procesamiento - Datos
# Este archivo contiene las operaciones reales que
# DataDSL puede realizar sobre los datos.
#
# La gramatica solo reconoce instrucciones.
# El Visitor interpreta esas instrucciones.
# El MotorDatos ejecuta las operaciones usando pandas.
#
# Ejemplo:
#
# datos := abrir "ventas.csv";
#
# La gramatica reconoce "abrir".
# El Visitor recibe esa instruccion.
# MotorDatos utiliza pandas para leer el CSV.
#
# En resumen:
# este archivo transforma los DataFrames.
# ======================================================


import os
import pandas as pd

from src.ErroresSemanticos import (
    ArchivoNoExisteError,
    ColumnaNoExisteError,
    OperacionNoPermitidaError
)


class MotorDatos:

    # --------------------------------------------------
    # CARGAR CSV
    # --------------------------------------------------

    @staticmethod
    def abrir_csv(ruta):
        """
        Lee un archivo CSV y devuelve un DataFrame.

        Un DataFrame es la estructura que utiliza pandas
        para representar datos en forma de tabla.
        """

        if not os.path.exists(ruta):
            raise ArchivoNoExisteError(ruta)

        try:
            return pd.read_csv(ruta)

        except Exception as error:
            raise OperacionNoPermitidaError(
                f"No fue posible leer el archivo '{ruta}': {error}"
            )


    # --------------------------------------------------
    # SELECCIONAR COLUMNAS
    # --------------------------------------------------

    @staticmethod
    def tomar_columnas(datos, columnas):
        """
        Devuelve un nuevo DataFrame que contiene
        solamente las columnas indicadas.
        """

        MotorDatos._validar_columnas(datos, columnas)

        # Se usa copy() para evitar modificar
        # silenciosamente el DataFrame original.
        return datos[columnas].copy()


    # --------------------------------------------------
    # FILTRAR DATOS
    # --------------------------------------------------

    @staticmethod
    def filtrar(datos, condicion):
        """
        Recibe una condicion booleana creada por el Visitor.

        Ejemplo conceptual:

        precio > 100

        pandas genera una serie de valores True/False
        y solo conserva las filas donde el resultado es True.
        """

        try:
            return datos[condicion].copy()

        except Exception as error:
            raise OperacionNoPermitidaError(
                f"No fue posible aplicar el filtro: {error}"
            )


    # --------------------------------------------------
    # ORDENAR
    # --------------------------------------------------

    @staticmethod
    def ordenar(datos, columna, direccion="asc"):
        """
        Ordena el DataFrame utilizando una columna.

        asc  -> menor a mayor
        desc -> mayor a menor
        """

        MotorDatos._validar_columnas(
            datos,
            [columna]
        )

        ascendente = direccion != "desc"

        return datos.sort_values(
            by=columna,
            ascending=ascendente
        ).copy()


    # --------------------------------------------------
    # CREAR COLUMNA
    # --------------------------------------------------

    @staticmethod
    def crear_columna(datos, nombre, valores):
        """
        Crea una nueva columna dentro de una copia
        del DataFrame.

        Ejemplo del DSL:

        -> crear total := cantidad * precio
        """

        resultado = datos.copy()

        resultado[nombre] = valores

        return resultado


    # --------------------------------------------------
    # RELLENAR VALORES NULOS
    # --------------------------------------------------

    @staticmethod
    def rellenar_nulos(datos, columna, valor):
        """
        Reemplaza valores faltantes de una columna.

        Ejemplo:

        -> rellenar precio con 0
        """

        MotorDatos._validar_columnas(
            datos,
            [columna]
        )

        resultado = datos.copy()

        resultado[columna] = resultado[columna].fillna(valor)

        return resultado


    # --------------------------------------------------
    # ELIMINAR FILAS CON NULOS
    # --------------------------------------------------

    @staticmethod
    def eliminar_nulos(datos, columnas):
        """
        Elimina las filas donde alguna de las columnas
        indicadas tenga un valor faltante.
        """

        MotorDatos._validar_columnas(
            datos,
            columnas
        )

        return datos.dropna(
            subset=columnas
        ).copy()


    # --------------------------------------------------
    # AGRUPAR DATOS
    # --------------------------------------------------

    @staticmethod
    def agrupar(datos, columnas):
        """
        Prepara un agrupamiento usando una o varias columnas.

        Ejemplo:

        -> agrupar por [ciudad]

        El resultado es un objeto GroupBy de pandas,
        que despues puede ser utilizado por resumir().
        """

        MotorDatos._validar_columnas(
            datos,
            columnas
        )

        return datos.groupby(
            columnas,
            dropna=False
        )


    # --------------------------------------------------
    # RESUMIR DATOS
    # --------------------------------------------------

    @staticmethod
    def resumir(datos_agrupados, agregaciones):
        """
        Calcula estadisticas sobre datos agrupados.

        agregaciones es una lista con informacion como:

        [
            ("ingreso", "suma", "total"),
            ("promedio", "media", "total"),
            ("registros", "contar", None)
        ]

        El Visitor construira esta informacion
        a partir del programa escrito en DataDSL.
        """

        resultados = []

        for nombre, funcion, columna in agregaciones:

            if funcion == "contar":
                serie = datos_agrupados.size()
                serie.name = nombre
                resultados.append(serie)
                continue

            datos_originales = datos_agrupados.obj

            MotorDatos._validar_columnas(
                datos_originales,
                [columna]
            )

            grupo_columna = datos_agrupados[columna]

            if funcion == "suma":
                serie = grupo_columna.sum()

            elif funcion == "media":
                serie = grupo_columna.mean()

            elif funcion == "mediana":
                serie = grupo_columna.median()

            elif funcion == "minimo":
                serie = grupo_columna.min()

            elif funcion == "maximo":
                serie = grupo_columna.max()

            elif funcion == "desviacion":
                serie = grupo_columna.std()

            else:
                raise OperacionNoPermitidaError(
                    f"La funcion '{funcion}' no existe."
                )

            serie.name = nombre
            resultados.append(serie)

        # concat une todas las estadisticas calculadas
        # en una sola tabla.
        resumen = pd.concat(
            resultados,
            axis=1
        )

        # reset_index convierte las columnas usadas
        # para agrupar nuevamente en columnas normales.
        return resumen.reset_index()


    # --------------------------------------------------
    # GUARDAR CSV
    # --------------------------------------------------

    @staticmethod
    def guardar_csv(datos, ruta):
        """
        Exporta un DataFrame a un archivo CSV.

        Ejemplo del DSL:

        guardar resumen como "salidas/resumen.csv";
        """

        carpeta = os.path.dirname(ruta)

        # Si la ruta contiene una carpeta y esta no existe,
        # se crea automaticamente.
        if carpeta:
            os.makedirs(
                carpeta,
                exist_ok=True
            )

        datos.to_csv(
            ruta,
            index=False
        )

        return ruta


    # --------------------------------------------------
    # VALIDACION DE COLUMNAS
    # --------------------------------------------------

    @staticmethod
    def _validar_columnas(datos, columnas):
        """
        Comprueba que todas las columnas solicitadas
        existan dentro del DataFrame.

        El guion bajo indica que este metodo esta pensado
        para uso interno del MotorDatos.
        """

        for columna in columnas:

            if columna not in datos.columns:
                raise ColumnaNoExisteError(
                    columna
                )
