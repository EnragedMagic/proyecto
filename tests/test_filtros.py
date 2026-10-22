# ======================================================
# PRUEBA UNITARIA - FILTRADO DE DATOS
# ======================================================
#
# Esta prueba verifica que MotorDatos pueda filtrar
# correctamente un conjunto de datos.
#
# Se cargan las ventas reales y luego se conservan
# solamente las filas donde cantidad > 0.
#
# La prueba confirma que:
# - El filtro devuelve datos.
# - Ninguna fila resultante tiene cantidad igual o menor a 0.
#
# En resumen:
# esta prueba confirma que los filtros funcionan.
# ======================================================


from src.MotorDatos import MotorDatos


def test_filtrado():

    datos = MotorDatos.abrir_csv(
        "datos/ventas.csv"
    )

    condicion = datos["cantidad"] > 0

    resultado = MotorDatos.filtrar(
        datos,
        condicion
    )

    # Debe quedar al menos una fila despues del filtro.
    assert len(resultado) > 0

    # Todas las filas deben cumplir cantidad > 0.
    assert (resultado["cantidad"] > 0).all()
