"""
funciones_calculo.py - Integrante 2 (Jazmin): funciones matematicas.

Reglas de calculo (ver explicacion_matematica.md):
    cantidad_semanal   f(x) = c * v * x
    cantidad_a_comprar g(q) = max(0, q - e)
    subtotal           s = q * p
    total              T = suma de subtotales
Las cantidades son ESTIMACIONES, no recomendaciones nutricionales.
"""
import math
from catalogo import PRODUCTOS, ESCENARIOS, UNIDADES, CONSUMO_POR_PERSONA


class ErrorDeValidacion(ValueError):
    """Se lanza cuando una entrada es negativa, invalida o inconsistente."""


# ---------------------------------------------------------------- validacion
def validar_numero(valor, nombre="valor", entero=False):
    """Valida que 'valor' sea un numero finito y >= 0. Devuelve el valor."""
    if isinstance(valor, bool) or not isinstance(valor, (int, float)):
        raise ErrorDeValidacion(f"{nombre} debe ser un numero.")
    if isinstance(valor, float) and (math.isnan(valor) or math.isinf(valor)):
        raise ErrorDeValidacion(f"{nombre} no es un numero valido.")
    if valor < 0:
        raise ErrorDeValidacion(f"{nombre} no puede ser negativo.")
    if entero and int(valor) != valor:
        raise ErrorDeValidacion(f"{nombre} debe ser un numero entero.")
    return valor


def validar_producto(producto):
    if producto not in PRODUCTOS:
        raise ErrorDeValidacion(f"Producto desconocido: {producto!r}.")
    return producto


def validar_escenario(escenario):
    if escenario not in ESCENARIOS:
        raise ErrorDeValidacion(f"Escenario desconocido: {escenario!r}.")
    return escenario


# ------------------------------------------------------------------ cantidades
def calcular_cantidad_semanal(consumo_por_persona, integrantes, veces_por_semana=1):
    """
    f(x) = c * v * x
    consumo_por_persona (c): cantidad por persona cada vez.
    integrantes (x): personas del hogar (entero >= 1 en la interfaz; 0 permitido).
    veces_por_semana (v): frecuencia.
    Ejemplo: calcular_cantidad_semanal(2, 4) -> 8   (el ejemplo del enunciado)
    """
    validar_numero(consumo_por_persona, "consumo_por_persona")
    validar_numero(integrantes, "integrantes", entero=True)
    validar_numero(veces_por_semana, "veces_por_semana")
    return consumo_por_persona * integrantes * veces_por_semana


def calcular_cantidad_por_escenario(producto, escenario, integrantes):
    """Cantidad semanal de un producto segun escenario (bajo/medio/alto)."""
    validar_producto(producto)
    validar_escenario(escenario)
    fila = ESCENARIOS.index(escenario)
    col = PRODUCTOS.index(producto)
    return calcular_cantidad_semanal(CONSUMO_POR_PERSONA[fila][col], integrantes)


def descontar_existencias(cantidad_necesaria, existencia=0):
    """g(q) = max(0, q - e). Nunca devuelve negativos."""
    validar_numero(cantidad_necesaria, "cantidad_necesaria")
    validar_numero(existencia, "existencia")
    return max(0, cantidad_necesaria - existencia)


def redondear_compra(cantidad, unidad):
    """
    Redondea HACIA ARRIBA para no quedarse corto:
    'unidades' -> entero; 'kg' -> multiplos de 0,1 kg.
    """
    validar_numero(cantidad, "cantidad")
    if unidad == "unidades":
        return math.ceil(round(cantidad, 6))
    if unidad == "kg":
        return math.ceil(round(cantidad * 10, 6)) / 10
    raise ErrorDeValidacion(f"Unidad no soportada: {unidad!r}.")


# -------------------------------------------------------------- costos
def calcular_subtotal(cantidad, precio_unitario):
    """s = q * p (precio por unidad o por kg)."""
    validar_numero(cantidad, "cantidad")
    validar_numero(precio_unitario, "precio_unitario")
    return round(cantidad * precio_unitario, 2)


def calcular_total(subtotales):
    """T = suma de subtotales."""
    total = 0
    for s in subtotales:
        total += validar_numero(s, "subtotal")
    return round(total, 2)


def evaluar_presupuesto(total, presupuesto):
    """Compara el costo estimado con el presupuesto del usuario."""
    validar_numero(total, "total")
    validar_numero(presupuesto, "presupuesto")
    return {
        "total": total,
        "presupuesto": presupuesto,
        "diferencia": round(presupuesto - total, 2),  # >0 sobra, <0 falta
        "alcanza": total <= presupuesto,
    }


# ------------------------------------------------------- lista de compras
def generar_lista_compras(integrantes, escenario, productos, precios,
                          existencias=None, presupuesto=None):
    """
    Une todas las reglas. Devuelve:
    {"items": [...], "total": float, "presupuesto": dict|None, "nota": str}
    - productos: lista de nombres seleccionados (RF02)
    - precios: dict producto -> precio por unidad/kg (RF05)
    - existencias: dict opcional producto -> cantidad que ya hay en casa
    """
    validar_numero(integrantes, "integrantes", entero=True)
    if integrantes < 1:
        raise ErrorDeValidacion("El hogar debe tener al menos 1 integrante.")
    validar_escenario(escenario)
    existencias = existencias or {}

    items, subtotales = [], []
    for prod in productos:
        validar_producto(prod)
        if prod not in precios:
            raise ErrorDeValidacion(f"Falta el precio de {prod!r}.")
        necesaria = calcular_cantidad_por_escenario(prod, escenario, integrantes)
        faltante = descontar_existencias(necesaria, existencias.get(prod, 0))
        comprar = redondear_compra(faltante, UNIDADES[prod])
        subtotal = calcular_subtotal(comprar, precios[prod])
        subtotales.append(subtotal)
        items.append({
            "producto": prod,
            "unidad": UNIDADES[prod],
            "necesaria": necesaria,
            "en_casa": existencias.get(prod, 0),
            "a_comprar": comprar,
            "precio_unitario": precios[prod],
            "subtotal": subtotal,
        })

    total = calcular_total(subtotales)
    return {
        "items": items,
        "total": total,
        "presupuesto": evaluar_presupuesto(total, presupuesto)
                       if presupuesto is not None else None,
        "nota": "Cantidades y costos son estimaciones; no son recomendaciones "
                "nutricionales ni precios oficiales.",
    }


if __name__ == "__main__":
    print(calcular_cantidad_semanal(2, 4))  # 8
    r = generar_lista_compras(4, "medio", ["manzanas", "zanahorias"],
                              {"manzanas": 300, "zanahorias": 1200},
                              existencias={"manzanas": 3}, presupuesto=5000)
    for it in r["items"]:
        print(it)
    print("Total:", r["total"], r["presupuesto"])
