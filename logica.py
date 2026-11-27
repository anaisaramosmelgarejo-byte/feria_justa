"""logica.py (Ana): adaptador entre la interfaz y los módulos del equipo.

    catalogo.py          -> productos, unidades, escenarios y consumos (compartido)
    funciones_calculo.py -> reglas de cálculo (Jazmin)
    matrices_feria.py    -> matrices y operaciones (Dafne)

Aquí solo se conectan; no se repite ningún cálculo.
"""
import pandas as pd

import catalogo
import funciones_calculo as fc
import matrices_feria as mf
from precios_otros import PRECIOS_OTROS

PRODUCTOS = catalogo.PRODUCTOS
ESCENARIOS = catalogo.ESCENARIOS
UNIDADES = catalogo.UNIDADES
PRECIOS_BASE = dict(catalogo.PRECIOS_EJEMPLO)

# Solo presentación: nombre con tilde y categoría de cada producto.
# Se leen de catalogo.py si los trae (NOMBRES y CATEGORIA_PRODUCTO, que genera generar_catalogo.py);
# si un producto no los tiene, se muestra igual (capitalizado, categoría "Otros").
NOMBRES = {"manzanas": "Manzanas", "platanos": "Plátanos", "zanahorias": "Zanahorias",
           "tomates": "Tomates", "paltas": "Paltas"}
NOMBRES.update(getattr(catalogo, "NOMBRES", {}))
_CATEGORIAS = {"manzanas": "Frutas", "platanos": "Frutas", "paltas": "Frutas",
               "zanahorias": "Raíces y bulbos", "tomates": "Frutos y otros"}
_CATEGORIAS.update(getattr(catalogo, "CATEGORIA_PRODUCTO", {}))
_ORDEN = ["Hojas y tallos", "Raíces y bulbos", "Frutos y otros", "Frutas"]


def nombre(p):
    return NOMBRES.get(p, p[:1].upper() + p[1:])


def categoria(p):
    return _CATEGORIAS.get(p, "Otros")


_cats = set(categoria(p) for p in PRODUCTOS)
CATEGORIAS = [c for c in _ORDEN if c in _cats] + sorted(_cats - set(_ORDEN))


def productos_de(categorias):
    return [p for p in PRODUCTOS if categoria(p) in categorias]


def abrev(p):
    return "kg" if UNIDADES[p] == "kg" else "unid."


def cantidad_txt(valor, p):
    """1,6 kg  /  5 unid."""
    # Los productos propios llevan la unidad al final del nombre: "Lechuga (unid.)"
    unidad = UNIDADES.get(p) or ("kg" if p.endswith("(kg)") else "unidades")
    if unidad == "kg":
        s = f"{valor:.2f}".rstrip("0").rstrip(".") or "0"
        return s.replace(".", ",") + " kg"
    return f"{valor:g} unid."


def calcular_lista(productos, escenario, integrantes, existencias, precios, presupuesto):
    """Usa generar_lista_compras (Jazmin). Devuelve (DataFrame, total, evaluación del presupuesto)."""
    r = fc.generar_lista_compras(integrantes, escenario, productos, precios,
                                 existencias=existencias, presupuesto=presupuesto)
    df = pd.DataFrame([{"Producto": i["producto"], "Unidad": i["unidad"], "Necesito": i["necesaria"],
                        "En casa": i["en_casa"], "Comprar": i["a_comprar"],
                        "Precio": i["precio_unitario"], "Subtotal": i["subtotal"]} for i in r["items"]])
    return df, r["total"], r["presupuesto"]


def agregar_extras(df, total, presupuesto, extras):
    """Suma a la lista los otros productos con precio (no usan matrices ni despensa)."""
    filas = []
    for x in extras:
        producto = x["Producto"]
        if producto not in PRECIOS_OTROS or pd.isna(x["Cantidad"]) or x["Cantidad"] <= 0:
            raise ValueError("En Otros productos elige el producto y una cantidad mayor que 0.")
        unidad = "kg" if producto.endswith("(kg)") else "unid."
        cantidad, precio = float(x["Cantidad"]), PRECIOS_OTROS[producto]
        if unidad == "unid." and not cantidad.is_integer():
            raise ValueError(f"{producto}: las unidades deben ser un número entero.")
        subtotal = fc.calcular_subtotal(cantidad, precio)
        filas.append({"Producto": producto, "Unidad": "kg" if unidad == "kg" else "unidades",
                      "Necesito": cantidad, "En casa": 0, "Comprar": cantidad,
                      "Precio": precio, "Subtotal": subtotal})
    if not filas:
        return df, total, fc.evaluar_presupuesto(total, presupuesto)
    nuevas = pd.DataFrame(filas)
    df = nuevas if df.empty else pd.concat([df, nuevas], ignore_index=True)
    total = fc.calcular_total([total] + [f["Subtotal"] for f in filas])
    return df, total, fc.evaluar_presupuesto(total, presupuesto)


def comparar(integrantes, precios):
    """Usa las matrices de Dafne. Devuelve (matriz por persona, matriz del hogar, costo por escenario)."""
    base = mf.crear_matriz_consumo()
    hogar = mf.matriz_del_hogar(integrantes)
    costos = mf.costo_por_escenario(hogar, precios)
    return base, hogar, costos


def tabla_matriz(matriz):
    columnas = [f"{nombre(p)} ({abrev(p)})" for p in PRODUCTOS]
    return pd.DataFrame(matriz, index=[e.capitalize() for e in ESCENARIOS], columns=columnas)