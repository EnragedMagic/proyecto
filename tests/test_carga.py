# ======================================================
# PRUEBA UNITARIA - CARGA DE CSV
# ======================================================
#
# Esta prueba verifica que MotorDatos pueda abrir
# correctamente un archivo CSV real.
#
# Si la carga funciona:
# - Debe devolver un DataFrame.
# - El DataFrame debe contener filas.
# - Debe reconocer columnas como ciudad y precio.
#
# En resumen:
# esta prueba confirma que la entrada de datos funciona.
# ======================================================


from src.MotorDatos import MotorDatos


def test_carga_csv():

    datos = MotorDatos.abrir_csv(
        "datos/ventas.csv"
    )

    # Verifica que el archivo tenga al menos una fila.
    assert len(datos) > 0

    # Verifica que existan columnas importantes.
    assert "ciudad" in datos.columns
    assert "precio" in datos.columns
