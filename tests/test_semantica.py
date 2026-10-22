# ======================================================
# PRUEBAS UNITARIAS - ERRORES SEMANTICOS
# ======================================================
#
# Este archivo verifica que DataDSL detecte correctamente
# operaciones que tienen una sintaxis valida, pero que
# no tienen sentido durante la ejecucion.
#
# En este caso se prueban errores como:
#
# - Pedir una columna que no existe.
# - Intentar abrir un archivo inexistente.
#
# En resumen:
# esta prueba confirma que las validaciones semanticas
# funcionan correctamente.
# ======================================================


import pytest

from src.MotorDatos import MotorDatos
from src.ErroresSemanticos import (
    ColumnaNoExisteError,
    ArchivoNoExisteError
)


def test_columna_inexistente():

    datos = MotorDatos.abrir_csv(
        "datos/ventas.csv"
    )

    # Intentamos seleccionar una columna
    # que no existe dentro del CSV.
    with pytest.raises(ColumnaNoExisteError):

        MotorDatos.tomar_columnas(
            datos,
            ["ciudad", "dinosaurio"]
        )


def test_archivo_inexistente():

    # Intentamos abrir un archivo que no existe.
    with pytest.raises(ArchivoNoExisteError):

        MotorDatos.abrir_csv(
            "datos/no_existe.csv"
        )
