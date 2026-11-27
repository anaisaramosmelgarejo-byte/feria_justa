"""
generar_catalogo.py - Convierte plantilla_productos.xlsx en catalogo.py.

Uso (con la plantilla y este archivo en la misma carpeta que catalogo.py):
    python generar_catalogo.py

Solo pasan al catalogo las filas "Listo": con unidad (kg o unidades) y los 4 numeros
(precio, consumo bajo, medio y alto). Antes de escribir, hace una copia de seguridad
del catalogo.py actual. El orden de las filas es el orden de las columnas de las matrices.
"""
import shutil
from datetime import datetime
from pathlib import Path

from openpyxl import load_workbook

AQUI = Path(__file__).parent
PLANTILLA = AQUI / "plantilla_productos.xlsx"
SALIDA = AQUI / "catalogo.py"
UNIDADES_VALIDAS = ("kg", "unidades")


def numero_valido(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool) and x >= 0


def leer_filas():
    hoja = load_workbook(PLANTILLA, data_only=True)["Productos"]
    listas, faltan, vistos = [], [], set()
    for fila in hoja.iter_rows(min_row=2, values_only=True):
        clave, nombre, categoria, unidad, precio, bajo, medio, alto = fila[:8]
        if not clave:
            continue
        clave = str(clave).strip()
        if clave in vistos:
            raise SystemExit(f"Clave repetida en la plantilla: {clave!r}")
        vistos.add(clave)
        if unidad in UNIDADES_VALIDAS and all(numero_valido(n) for n in (precio, bajo, medio, alto)):
            listas.append((clave, str(nombre or clave).strip(), str(categoria or "Otros").strip(),
                           unidad, precio, [bajo, medio, alto]))
        else:
            faltan.append(clave)
    return listas, faltan


def escribir(listas):
    lineas = ['"""',
              "catalogo.py - Convenciones COMPARTIDAS del proyecto Feria Justa.", "",
              "GENERADO con generar_catalogo.py a partir de plantilla_productos.xlsx.",
              "Para cambiar productos, precios o consumos: editar la plantilla y volver a generar.", "",
              "IMPORTANTE: los consumos son SUPUESTOS DE DEMOSTRACION, no recomendaciones",
              "nutricionales. Los precios son ingresados por el usuario o datos de ejemplo.",
              '"""', "",
              "# Orden de las COLUMNAS de las matrices", "PRODUCTOS = ["]
    lineas += [f"    {c!r}," for c, *_ in listas] + ["]", "",
               "# Orden de las FILAS de las matrices", 'ESCENARIOS = ["bajo", "medio", "alto"]', "",
               "# Unidad de medida de cada producto", "UNIDADES = {"]
    lineas += [f"    {c!r}: {u!r}," for c, _, _, u, _, _ in listas] + ["}", "",
               "# Consumo semanal estimado POR PERSONA (filas = escenarios, columnas = PRODUCTOS)",
               "CONSUMO_POR_PERSONA = ["]
    for i, esc in enumerate(["bajo", "medio", "alto"]):
        lineas.append("    [" + ", ".join(repr(f[5][i]) for f in listas) + f"],   # {esc}")
    lineas += ["]", "", "# Precios de EJEMPLO (CLP por unidad o por kg segun UNIDADES)", "PRECIOS_EJEMPLO = {"]
    lineas += [f"    {c!r}: {p!r}," for c, _, _, _, p, _ in listas] + ["}", "",
               "# Solo para la interfaz: nombre que ve el usuario y categoria de cada producto",
               "NOMBRES = {"]
    lineas += [f"    {c!r}: {n!r}," for c, n, *_ in listas] + ["}", "", "CATEGORIA_PRODUCTO = {"]
    lineas += [f"    {c!r}: {cat!r}," for c, _, cat, *_ in listas] + ["}", ""]
    if SALIDA.exists():
        copia = SALIDA.with_name(f"catalogo_respaldo_{datetime.now():%Y%m%d_%H%M%S}.py")
        shutil.copy(SALIDA, copia)
        print(f"Copia de seguridad: {copia.name}")
    SALIDA.write_text("\n".join(lineas), encoding="utf-8")


if __name__ == "__main__":
    listas, faltan = leer_filas()
    if not listas:
        raise SystemExit("No hay ninguna fila 'Listo' en la plantilla.")
    escribir(listas)
    print(f"catalogo.py generado con {len(listas)} productos.")
    if faltan:
        print(f"Quedaron fuera {len(faltan)} productos con datos incompletos:")
        print("  " + ", ".join(faltan))
