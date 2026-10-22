# ======================================================
# VISITOR DE DATADSL
# ======================================================
# Interpretar - Conectar - Ejecutar
# Este archivo recorre el arbol sintactico generado por
# ANTLR y ejecuta el significado de cada instruccion.
#
# La gramatica reconoce la estructura.
# El Visitor interpreta esa estructura.
# El MotorDatos ejecuta las operaciones con pandas.
# El ContextoEjecucion guarda las variables.
#
# Ejemplo:
#
# datos := abrir "ventas.csv";
#
# El parser reconoce que es una asignacion con una lectura.
# El Visitor ejecuta abrir_csv().
# Luego guarda el DataFrame en la variable "datos".
#
# En resumen:
# este archivo conecta sintaxis y ejecucion.
# ======================================================


from DataDSLVisitor import DataDSLVisitor

from src.ContextoEjecucion import ContextoEjecucion
from src.MotorDatos import MotorDatos
from src.ErroresSemanticos import (
    VariableNoDefinidaError,
    ColumnaNoExisteError,
    OperacionNoPermitidaError
)


class DataDSLVisitorImpl(DataDSLVisitor):

    def __init__(self):
        super().__init__()

        # ContextoEjecucion contiene la tabla de simbolos.
        # Aqui se guardan las variables creadas por DataDSL.
        self.contexto = ContextoEjecucion()

        # Guarda temporalmente las columnas utilizadas
        # en un agrupamiento para poder generar el resumen.
        self.ultimo_agrupamiento = None


    # --------------------------------------------------
    # PROGRAMA
    # --------------------------------------------------

    def visitPrograma(self, ctx):
        """
        Recorre todas las instrucciones del programa.
        """

        for instruccion in ctx.instruccion():
            self.visit(instruccion)

        return None


    # --------------------------------------------------
    # ASIGNACIONES
    # --------------------------------------------------

    def visitAsignacion(self, ctx):
        """
        Ejecuta una asignacion.

        Ejemplo:

        datos := abrir "ventas.csv";

        El lado izquierdo es el nombre de la variable.
        El lado derecho produce el valor que se guardara.
        """

        nombre = ctx.ID().getText()

        valor = self.visit(ctx.contenido())

        self.contexto.guardar(
            nombre,
            valor
        )

        print(
            f"Variable '{nombre}' guardada correctamente."
        )

        return valor


    # --------------------------------------------------
    # CONTENIDO
    # --------------------------------------------------

    def visitContenido(self, ctx):
        """
        Determina que tipo de contenido tiene
        una asignacion y visita la regla correspondiente.
        """

        if ctx.lectura():
            return self.visit(ctx.lectura())

        if ctx.flujo():
            return self.visit(ctx.flujo())

        if ctx.expresion():
            return self.visit(ctx.expresion())

        return None


    # --------------------------------------------------
    # ABRIR CSV
    # --------------------------------------------------

    def visitLectura(self, ctx):
        """
        Carga un archivo CSV mediante MotorDatos.

        Ejemplo:

        datos := abrir "datos/ventas.csv";
        """

        ruta = ctx.STRING().getText()

        # STRING incluye las comillas.
        # [1:-1] las elimina.
        ruta = ruta[1:-1]

        return MotorDatos.abrir_csv(
            ruta
        )


    # --------------------------------------------------
    # FLUJOS
    # --------------------------------------------------

    def visitFlujo(self, ctx):
        """
        Ejecuta una cadena de transformaciones.

        Ejemplo:

        ventas := datos
        -> tomar [ciudad, precio]
        -> cuando precio > 100;

        Primero recupera "datos" de la tabla de simbolos.
        Luego aplica cada paso en orden.
        """

        nombre_origen = ctx.ID().getText()

        if not self.contexto.existe(nombre_origen):
            raise VariableNoDefinidaError(
                nombre_origen
            )

        datos = self.contexto.obtener(
            nombre_origen
        )

        # Cada paso recibe el resultado del paso anterior.
        for paso in ctx.paso():
            datos = self._ejecutar_paso(
                paso,
                datos
            )

        return datos


    def _ejecutar_paso(self, ctx, datos):
        """
        Determina que tipo de operacion contiene
        un paso del pipeline.
        """

        if ctx.seleccion():
            return self._seleccionar(
                ctx.seleccion(),
                datos
            )

        if ctx.filtro():
            return self._filtrar(
                ctx.filtro(),
                datos
            )

        if ctx.ordenamiento():
            return self._ordenar(
                ctx.ordenamiento(),
                datos
            )

        if ctx.columnaCalculada():
            return self._crear_columna(
                ctx.columnaCalculada(),
                datos
            )

        if ctx.rellenarNulos():
            return self._rellenar_nulos(
                ctx.rellenarNulos(),
                datos
            )

        if ctx.eliminarNulos():
            return self._eliminar_nulos(
                ctx.eliminarNulos(),
                datos
            )

        if ctx.agrupacion():
            return self._agrupar(
                ctx.agrupacion(),
                datos
            )

        if ctx.resumen():
            return self._resumir(
                ctx.resumen(),
                datos
            )

        raise OperacionNoPermitidaError(
            "Paso del flujo no reconocido."
        )


    # --------------------------------------------------
    # SELECCION
    # --------------------------------------------------

    def _seleccionar(self, ctx, datos):
        """
        Obtiene las columnas escritas entre corchetes
        y solicita al MotorDatos que las seleccione.
        """

        columnas = self._obtener_columnas(
            ctx.columnas()
        )

        return MotorDatos.tomar_columnas(
            datos,
            columnas
        )


    # --------------------------------------------------
    # FILTRO
    # --------------------------------------------------

    def _filtrar(self, ctx, datos):
        """
        Evalua una expresion usando las columnas
        del DataFrame actual.

        Ejemplo:

        -> cuando precio > 100
        """

        condicion = self._evaluar_expresion(
            ctx.expresion(),
            datos
        )

        return MotorDatos.filtrar(
            datos,
            condicion
        )


    # --------------------------------------------------
    # ORDENAMIENTO
    # --------------------------------------------------

    def _ordenar(self, ctx, datos):
        """
        Ejecuta:

        -> ordenar por precio
        -> ordenar por precio desc
        """

        columna = ctx.ID().getText()

        direccion = "asc"

        if ctx.DESC():
            direccion = "desc"

        return MotorDatos.ordenar(
            datos,
            columna,
            direccion
        )


    # --------------------------------------------------
    # COLUMNA CALCULADA
    # --------------------------------------------------

    def _crear_columna(self, ctx, datos):
        """
        Crea una columna utilizando una expresion.

        Ejemplo:

        -> crear total := cantidad * precio
        """

        nombre = ctx.ID().getText()

        valores = self._evaluar_expresion(
            ctx.expresion(),
            datos
        )

        return MotorDatos.crear_columna(
            datos,
            nombre,
            valores
        )


    # --------------------------------------------------
    # VALORES NULOS
    # --------------------------------------------------

    def _rellenar_nulos(self, ctx, datos):
        """
        Ejecuta:

        -> rellenar precio con 0
        """

        columna = ctx.ID().getText()

        valor = self._evaluar_expresion(
            ctx.expresion(),
            datos
        )

        return MotorDatos.rellenar_nulos(
            datos,
            columna,
            valor
        )


    def _eliminar_nulos(self, ctx, datos):
        """
        Ejecuta:

        -> eliminar_nulos [precio, cantidad]
        """

        columnas = self._obtener_columnas(
            ctx.columnas()
        )

        return MotorDatos.eliminar_nulos(
            datos,
            columnas
        )


    # --------------------------------------------------
    # AGRUPAMIENTO
    # --------------------------------------------------

    def _agrupar(self, ctx, datos):
        """
        Ejecuta:

        -> agrupar por [ciudad]

        El resultado ya no es un DataFrame normal,
        sino un objeto GroupBy de pandas.
        """

        columnas = self._obtener_columnas(
            ctx.columnas()
        )

        self.ultimo_agrupamiento = columnas

        return MotorDatos.agrupar(
            datos,
            columnas
        )


    # --------------------------------------------------
    # RESUMEN
    # --------------------------------------------------

    def _resumir(self, ctx, datos):
        """
        Convierte las agregaciones del DSL
        en una estructura que entiende MotorDatos.

        Ejemplo:

        -> resumir ingreso := suma(total),
                   promedio := media(total)
        """

        agregaciones = []

        for agregacion_ctx in ctx.agregacion():

            nombre = agregacion_ctx.ID().getText()

            funcion_ctx = agregacion_ctx.funcionAgregacion()

            funcion, columna = self._leer_agregacion(
                funcion_ctx
            )

            agregaciones.append(
                (
                    nombre,
                    funcion,
                    columna
                )
            )

        return MotorDatos.resumir(
            datos,
            agregaciones
        )


    def _leer_agregacion(self, ctx):
        """
        Traduce una funcion escrita en DataDSL
        a un nombre que entiende MotorDatos.
        """

        if ctx.SUMA():
            return "suma", ctx.ID().getText()

        if ctx.MEDIA():
            return "media", ctx.ID().getText()

        if ctx.MEDIANA():
            return "mediana", ctx.ID().getText()

        if ctx.MINIMO():
            return "minimo", ctx.ID().getText()

        if ctx.MAXIMO():
            return "maximo", ctx.ID().getText()

        if ctx.DESVIACION():
            return "desviacion", ctx.ID().getText()

        if ctx.CONTAR():
            return "contar", None

        raise OperacionNoPermitidaError(
            "Funcion de agregacion desconocida."
        )


    # --------------------------------------------------
    # GUARDAR CSV
    # --------------------------------------------------

    def visitGuardado(self, ctx):
        """
        Guarda una variable en un archivo CSV.

        Ejemplo:

        guardar resumen como "salidas/resumen.csv";
        """

        nombre = ctx.ID().getText()

        if not self.contexto.existe(nombre):
            raise VariableNoDefinidaError(
                nombre
            )

        datos = self.contexto.obtener(
            nombre
        )

        ruta = ctx.STRING().getText()[1:-1]

        MotorDatos.guardar_csv(
            datos,
            ruta
        )

        print(
            f"Archivo guardado correctamente en '{ruta}'."
        )

        return ruta


    # --------------------------------------------------
    # VISUALIZACION
    # --------------------------------------------------

    def visitVisualizacion(self, ctx):
        """
        En el segundo corte mantenemos el reconocimiento
        de la instruccion de visualizacion.

        La implementacion completa de graficas corresponde
        al tercer corte.
        """

        nombre = ctx.ID().getText()

        if not self.contexto.existe(nombre):
            raise VariableNoDefinidaError(
                nombre
            )

        print(
            f"Visualizacion reconocida para '{nombre}'. "
            f"La grafica se implementara en el tercer corte."
        )

        return None


    # --------------------------------------------------
    # COLUMNAS
    # --------------------------------------------------

    def _obtener_columnas(self, ctx):
        """
        Convierte:

        [ciudad, producto, precio]

        en:

        ["ciudad", "producto", "precio"]
        """

        return [
            token.getText()
            for token in ctx.ID()
        ]


    # --------------------------------------------------
    # EVALUACION DE EXPRESIONES
    # --------------------------------------------------

    def _evaluar_expresion(self, ctx, datos):
        """
        Punto de entrada para evaluar expresiones.

        Ejemplos:

        precio > 100

        cantidad * precio

        precio > 100 y cantidad > 0
        """

        return self._evaluar_expresion_logica(
            ctx.expresionLogica(),
            datos
        )


    def _evaluar_expresion_logica(self, ctx, datos):

        comparaciones = ctx.comparacion()

        resultado = self._evaluar_comparacion(
            comparaciones[0],
            datos
        )

        for i in range(1, len(comparaciones)):

            derecha = self._evaluar_comparacion(
                comparaciones[i],
                datos
            )

            operador = ctx.getChild(
                (i * 2) - 1
            ).getText()

            if operador == "y":
                resultado = resultado & derecha

            elif operador == "o":
                resultado = resultado | derecha

        return resultado


    def _evaluar_comparacion(self, ctx, datos):

        valores = ctx.suma()

        izquierda = self._evaluar_suma(
            valores[0],
            datos
        )

        if len(valores) == 1:
            return izquierda

        derecha = self._evaluar_suma(
            valores[1],
            datos
        )

        operador = ctx.getChild(1).getText()

        if operador == ">":
            return izquierda > derecha

        if operador == "<":
            return izquierda < derecha

        if operador == ">=":
            return izquierda >= derecha

        if operador == "<=":
            return izquierda <= derecha

        if operador == "==":
            return izquierda == derecha

        if operador == "!=":
            return izquierda != derecha

        raise OperacionNoPermitidaError(
            f"Comparacion '{operador}' no soportada."
        )


    def _evaluar_suma(self, ctx, datos):

        productos = ctx.producto()

        resultado = self._evaluar_producto(
            productos[0],
            datos
        )

        for i in range(1, len(productos)):

            derecha = self._evaluar_producto(
                productos[i],
                datos
            )

            operador = ctx.getChild(
                (i * 2) - 1
            ).getText()

            if operador == "+":
                resultado = resultado + derecha

            elif operador == "-":
                resultado = resultado - derecha

        return resultado


    def _evaluar_producto(self, ctx, datos):

        potencias = ctx.potencia()

        resultado = self._evaluar_potencia(
            potencias[0],
            datos
        )

        for i in range(1, len(potencias)):

            derecha = self._evaluar_potencia(
                potencias[i],
                datos
            )

            operador = ctx.getChild(
                (i * 2) - 1
            ).getText()

            if operador == "*":
                resultado = resultado * derecha

            elif operador == "/":
                resultado = resultado / derecha

            elif operador == "%":
                resultado = resultado % derecha

        return resultado


    def _evaluar_potencia(self, ctx, datos):

        valores = ctx.valor()

        resultado = self._evaluar_valor(
            valores[0],
            datos
        )

        for i in range(1, len(valores)):

            derecha = self._evaluar_valor(
                valores[i],
                datos
            )

            resultado = resultado ** derecha

        return resultado


    def _evaluar_valor(self, ctx, datos):
        """
        Convierte los valores del DSL en valores
        que Python y pandas pueden utilizar.
        """

        if ctx.NUMBER():

            texto = ctx.NUMBER().getText()

            if "." in texto:
                return float(texto)

            return int(texto)


        if ctx.STRING():
            return ctx.STRING().getText()[1:-1]


        if ctx.VERDADERO():
            return True


        if ctx.FALSO():
            return False


        if ctx.ID():

            columna = ctx.ID().getText()

            if columna not in datos.columns:
                raise ColumnaNoExisteError(
                    columna
                )

            return datos[columna]


        if ctx.expresion():

            return self._evaluar_expresion(
                ctx.expresion(),
                datos
            )


        raise OperacionNoPermitidaError(
            "No fue posible evaluar el valor."
        )
