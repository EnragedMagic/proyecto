# ======================================================
# PRUEBA DE INTEGRACION
# ======================================================
#
# Esta prueba verifica que varias partes del proyecto
# puedan trabajar juntas en un flujo completo.
#
# A diferencia de una prueba unitaria, aqui no se prueba
# una sola funcion de forma aislada.
#
# Se prueba una secuencia completa:
#
# 1. Cargar un CSV.
# 2. Seleccionar columnas.
# 3. Filtrar datos.
# 4. Crear una columna calculada.
# 5. Agrupar.
# 6. Resumir.
# 7. Exportar el resultado a CSV.
#
# En resumen:
# esta prueba comprueba que los componentes principales
# del motor funcionen correctamente en conjunto.
# ======================================================


import os

from src.MotorDatos import MotorDatos


def test_flujo_completo():

    # 1. Cargar los datos reales.
    datos = MotorDatos.abrir_csv(
        "datos/ventas.csv"
    )

    # 2. Seleccionar columnas.
    datos = MotorDatos.tomar_columnas(
        datos,
        [
            "ciudad",
            "producto",
            "cantidad",
            "precio"
        ]
    )

    # 3. Filtrar filas con cantidad mayor a cero.
    condicion = datos["cantidad"] > 0

    datos = MotorDatos.filtrar(
        datos,
        condicion
    )

    # 4. Crear la columna total.
    total = (
        datos["cantidad"]
        * datos["precio"]
    )

    datos = MotorDatos.crear_columna(
        datos,
        "total",
        total
    )

    # 5. Agrupar por ciudad.
    agrupados = MotorDatos.agrupar(
        datos,
        ["ciudad"]
    )

    # 6. Crear una tabla resumen.
    resumen = MotorDatos.resumir(
        agrupados,
        [
            (
                "ingreso",
                "suma",
                "total"
            ),
            (
                "promedio",
                "media",
                "total"
            ),
            (
                "registros",
                "contar",
                None
            )
        ]
    )

    # 7. Exportar la tabla resumen.
    ruta_salida = (
        "salidas/test_resumen.csv"
    )

    MotorDatos.guardar_csv(
        resumen,
        ruta_salida
    )

    # Verificamos que se haya creado el archivo.
    assert os.path.exists(
        ruta_salida
    )

    # Verificamos que el resultado tenga filas.
    assert len(resumen) > 0

    # Verificamos columnas del resumen.
    assert "ciudad" in resumen.columns
    assert "ingreso" in resumen.columns
    assert "promedio" in resumen.columns
    assert "registros" in resumen.columns
