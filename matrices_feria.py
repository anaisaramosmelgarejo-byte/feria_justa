"""
matrices_feria.py - Integrante 3 (Dafne): matrices y operaciones.

Estructura: una matriz es una lista de filas (listas de numeros).
    filas    -> escenarios (bajo, medio, alto)  [catalogo.ESCENARIOS]
    columnas -> productos                        [catalogo.PRODUCTOS]
Dimensiones: m x n = (escenarios) x (productos).
Se usa Python puro (sin NumPy) para que el curso pueda ver cada operacion.
"""
from catalogo import PRODUCTOS, ESCENARIOS, CONSUMO_POR_PERSONA, UNIDADES


class ErrorDeMatriz(ValueError):
    """Matriz mal formada o operacion con dimensiones incompatibles."""


# ------------------------------------------------------------- creacion
def crear_matriz_consumo():
    """Copia de la matriz base de consumo POR PERSONA (escenarios x productos)."""
    return [fila[:] for fila in CONSUMO_POR_PERSONA]


def validar_matriz(matriz):
    """Debe ser rectangular, no vacia y con numeros >= 0."""
    if not isinstance(matriz, list) or not matriz:
        raise ErrorDeMatriz("La matriz debe ser una lista no vacia de filas.")
    ancho = None
    for i, fila in enumerate(matriz):
        if not isinstance(fila, list) or not fila:
            raise ErrorDeMatriz(f"La fila {i} no es valida.")
        if ancho is None:
            ancho = len(fila)
        elif len(fila) != ancho:
            raise ErrorDeMatriz("Todas las filas deben tener el mismo largo.")
        for x in fila:
            if isinstance(x, bool) or not isinstance(x, (int, float)):
                raise ErrorDeMatriz(f"Valor no numerico en fila {i}: {x!r}.")
            if x < 0:
                raise ErrorDeMatriz(f"Valor negativo en fila {i}: {x}.")
    return matriz


def dimensiones(matriz):
    """Devuelve (filas, columnas)."""
    validar_matriz(matriz)
    return len(matriz), len(matriz[0])


# ------------------------------------------------------------- acceso
def obtener_fila(matriz, escenario):
    """Fila completa de un escenario (por nombre o por indice)."""
    validar_matriz(matriz)
    i = ESCENARIOS.index(escenario) if isinstance(escenario, str) else escenario
    return matriz[i][:]


def obtener_columna(matriz, producto):
    """Columna completa de un producto (por nombre o por indice)."""
    validar_matriz(matriz)
    j = PRODUCTOS.index(producto) if isinstance(producto, str) else producto
    return [fila[j] for fila in matriz]


def obtener_elemento(matriz, escenario, producto):
    return obtener_fila(matriz, escenario)[
        PRODUCTOS.index(producto) if isinstance(producto, str) else producto]


# ------------------------------------------------------------ operaciones
def sumar_matrices(a, b):
    """C[i][j] = A[i][j] + B[i][j]. Requiere mismas dimensiones."""
    if dimensiones(a) != dimensiones(b):
        raise ErrorDeMatriz(f"Dimensiones incompatibles: {dimensiones(a)} vs {dimensiones(b)}.")
    return [[x + y for x, y in zip(fa, fb)] for fa, fb in zip(a, b)]


def restar_matrices(a, b):
    """C = A - B (puede dar negativos: es una diferencia, no una cantidad)."""
    if dimensiones(a) != dimensiones(b):
        raise ErrorDeMatriz(f"Dimensiones incompatibles: {dimensiones(a)} vs {dimensiones(b)}.")
    return [[x - y for x, y in zip(fa, fb)] for fa, fb in zip(a, b)]


def multiplicar_por_escalar(matriz, k):
    """C[i][j] = k * A[i][j]. Con k = integrantes pasa de 'por persona' a 'hogar'."""
    validar_matriz(matriz)
    if isinstance(k, bool) or not isinstance(k, (int, float)) or k < 0:
        raise ErrorDeMatriz("El escalar debe ser un numero >= 0.")
    return [[k * x for x in fila] for fila in matriz]


def transpuesta(matriz):
    validar_matriz(matriz)
    return [list(col) for col in zip(*matriz)]


# ---------------------------------------------------------------- totales
def totales_por_producto(matriz):
    """Suma de cada COLUMNA (total de cada producto en todos los escenarios)."""
    validar_matriz(matriz)
    return [sum(col) for col in zip(*matriz)]


def totales_por_escenario(matriz):
    """Suma de cada FILA (total de articulos/medidas en cada escenario)."""
    validar_matriz(matriz)
    return [sum(fila) for fila in matriz]


def matriz_del_hogar(integrantes, matriz_por_persona=None):
    """Cantidades semanales del hogar = integrantes * (matriz por persona)."""
    base = matriz_por_persona or crear_matriz_consumo()
    return multiplicar_por_escalar(base, integrantes)


def costo_por_escenario(matriz_hogar, precios):
    """
    Producto matriz x vector: costo[i] = suma_j( Q[i][j] * precio[j] ).
    precios: lista en el orden de PRODUCTOS o dict producto -> precio.
    """
    validar_matriz(matriz_hogar)
    if isinstance(precios, dict):
        precios = [precios[p] for p in PRODUCTOS]
    if len(precios) != len(matriz_hogar[0]):
        raise ErrorDeMatriz("El vector de precios no coincide con el numero de productos.")
    if any(p < 0 for p in precios):
        raise ErrorDeMatriz("Los precios no pueden ser negativos.")
    return [round(sum(q * p for q, p in zip(fila, precios)), 2) for fila in matriz_hogar]


# ------------------------------------------------------------ comparacion
def comparar_escenarios(matriz, escenario_a, escenario_b):
    """Diferencia (B - A) por producto, como dict producto -> diferencia."""
    fa, fb = obtener_fila(matriz, escenario_a), obtener_fila(matriz, escenario_b)
    return {p: round(y - x, 6) for p, x, y in zip(PRODUCTOS, fa, fb)}


def mostrar_matriz(matriz):
    """Texto legible con encabezados (util para demostracion)."""
    validar_matriz(matriz)
    ancho = 11
    lineas = [" " * 8 + "".join(f"{p:>{ancho}}" for p in PRODUCTOS[:len(matriz[0])])]
    for nombre, fila in zip(ESCENARIOS, matriz):
        lineas.append(f"{nombre:<8}" + "".join(f"{x:>{ancho}g}" for x in fila))
    return "\n".join(lineas)


if __name__ == "__main__":
    base = crear_matriz_consumo()
    hogar = matriz_del_hogar(4)
    print("Por persona:\n" + mostrar_matriz(base))
    print("\nHogar de 4:\n" + mostrar_matriz(hogar))
    print("\nTotales por producto:", totales_por_producto(hogar))
    print("Diferencia alto-bajo:", comparar_escenarios(hogar, "bajo", "alto"))
