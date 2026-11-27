"""
catalogo.py - Convenciones COMPARTIDAS del proyecto Feria Justa.

GENERADO con generar_catalogo.py a partir de plantilla_productos.xlsx.
Para cambiar productos, precios o consumos: editar la plantilla y volver a generar.

IMPORTANTE: los consumos son SUPUESTOS DE DEMOSTRACION, no recomendaciones
nutricionales. Los precios son ingresados por el usuario o datos de ejemplo.
"""

# Orden de las COLUMNAS de las matrices
PRODUCTOS = [
    'manzanas',
    'platanos',
    'zanahorias',
    'tomates',
    'paltas',
]

# Orden de las FILAS de las matrices
ESCENARIOS = ["bajo", "medio", "alto"]

# Unidad de medida de cada producto
UNIDADES = {
    'manzanas': 'unidades',
    'platanos': 'unidades',
    'zanahorias': 'kg',
    'tomates': 'kg',
    'paltas': 'unidades',
}

# Consumo semanal estimado POR PERSONA (filas = escenarios, columnas = PRODUCTOS)
CONSUMO_POR_PERSONA = [
    [1, 2, 0.2, 0.25, 1],   # bajo
    [2, 3, 0.4, 0.5, 2],   # medio
    [3, 5, 0.6, 0.75, 3],   # alto
]

# Precios de EJEMPLO (CLP por unidad o por kg segun UNIDADES)
PRECIOS_EJEMPLO = {
    'manzanas': 200,
    'platanos': 260,
    'zanahorias': 800,
    'tomates': 1500,
    'paltas': 875,
}

# Solo para la interfaz: nombre que ve el usuario y categoria de cada producto
NOMBRES = {
    'manzanas': 'Manzana Roja (Fuji / Royal Gala)',
    'platanos': 'Plátano',
    'zanahorias': 'Zanahoria',
    'tomates': 'Tomate (Larga vida / Limachino)',
    'paltas': 'Palta (Hass / Negra de la Cruz / Edranol)',
}

CATEGORIA_PRODUCTO = {
    'manzanas': 'Frutas',
    'platanos': 'Frutas',
    'zanahorias': 'Raíces y bulbos',
    'tomates': 'Frutos y otros',
    'paltas': 'Frutas',
}
