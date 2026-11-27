# Feria Justa

Aplicación web (prototipo) que ayuda a hogares a planificar su compra semanal de frutas y verduras.

## Equipo y archivos

| Integrante | Archivos |
|---|---|
| Daniela (análisis y diseño) | `docs/` |
| Jazmin (funciones matemáticas) | `funciones_calculo.py`, `test_funciones_calculo.py`, `docs/explicacion_matematica.md` |
| Dafne (matrices) | `matrices_feria.py`, `test_matrices_feria.py` |
| Ana (interfaz e integración) | `app.py`, `logica.py`, `db.py`, `test_integracion.py`, `.streamlit/config.toml` |
| Compartido | `catalogo.py` (productos, unidades, escenarios y consumos) |

`logica.py` conecta la interfaz con los módulos de Jazmin y Dafne; no repite ningún cálculo.

## Cómo ejecutar

```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Se abre en http://localhost:8501. Para detener la app: `Ctrl + C`.

## Pruebas

```
python -m unittest test_funciones_calculo test_matrices_feria test_integracion
```

## Importante

- Los consumos son supuestos de demostración, no recomendaciones nutricionales.
- Los precios son de ejemplo y el usuario puede ajustarlos en la pantalla; no son precios oficiales.
- La base de datos (`feria_justa.db`) se crea sola la primera vez que se abre la app.
