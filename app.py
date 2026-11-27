import html

import pandas as pd
import streamlit as st

import db
import logica as lg

st.set_page_config(page_title="Feria Justa", page_icon="🥬", layout="wide")
db.crear_tablas()

# Declara la página en español para que el navegador no la "traduzca" y cambie los números
try:
    st.iframe("<script>const d = window.parent.document.documentElement;"
              "d.lang = 'es'; d.setAttribute('translate', 'no');</script>", height=1)
except Exception:
    pass

ICONOS = {"Frutas": "🍎", "Raíces y bulbos": "🥕", "Frutos y otros": "🍅", "Hojas y tallos": "🥬"}


def etiqueta(cat):
    return f"{ICONOS.get(cat, '🛒')} {cat}"


def clp(x):
    """Formato chileno: $8.790"""
    return "$" + f"{x:,.0f}".replace(",", ".")


ESTILO = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700&family=Nunito+Sans:wght@400;600;700&display=swap');
html, body, .stApp { font-family: 'Nunito Sans', sans-serif; }
h1, h2, h3, .marca { font-family: 'Barlow Condensed', sans-serif !important; font-weight: 700 !important; color: #17492A; }
h1 { font-size: 3.2rem !important; line-height: 1.05 !important; }
footer, #MainMenu { visibility: hidden; }
header[data-testid="stHeader"] { background: transparent; }
.block-container { max-width: 1100px; padding-top: 2.5rem; }
.marca { font-size: 2rem; margin-bottom: .2rem; }
.stButton > button, .stDownloadButton > button { border-radius: 10px; font-weight: 700; min-height: 2.8rem; }
div[data-testid="stMetric"] { background: #fff; border: 1px solid #D5E2D0; border-radius: 12px; padding: 14px 16px; }
div[data-testid="stMetricValue"] { font-family: 'Barlow Condensed', sans-serif; font-weight: 700; color: #17492A; font-size: 2rem; }
div[data-testid="stMetricLabel"] *, div[data-testid="stMetricValue"] * { overflow: visible !important; text-overflow: clip !important; white-space: normal !important; }
.boleta { background: #FFFEF7; border: 1px solid #D9D4BE; border-radius: 4px 4px 14px 14px; box-shadow: 0 2px 0 #E4DFC9; overflow: hidden; }
.toldo { height: 16px; background: repeating-linear-gradient(90deg, #1F6B3A 0 24px, #FFFEF7 24px 48px); }
.cuerpo { padding: 1.1rem 1.4rem 1.3rem; }
.b-titulo { font-family: 'Barlow Condensed', sans-serif; font-weight: 700; font-size: 1.9rem; color: #17492A; line-height: 1.1; }
.b-sub { color: #5E6B61; font-size: .9rem; margin-bottom: .9rem; }
.fila { display: flex; align-items: baseline; gap: .5rem; padding: .28rem 0; font-size: 1.02rem; color: #1E2A22; }
.fila .nom { font-weight: 700; }
.fila .puntos { flex: 1; border-bottom: 2px dotted #B9C4B2; transform: translateY(-3px); }
.fila .cant { color: #5E6B61; font-variant-numeric: tabular-nums; }
.fila .monto { min-width: 4.8rem; text-align: right; font-weight: 700; font-variant-numeric: tabular-nums; }
.fila.listo .nom, .fila.listo .monto { color: #8A958B; font-weight: 600; }
.total { display: flex; justify-content: space-between; margin-top: .9rem; padding-top: .7rem; border-top: 2px solid #17492A;
         font-family: 'Barlow Condensed', sans-serif; font-size: 1.8rem; font-weight: 700; color: #17492A; }

/* ---- rediseño ---- */
.stApp { background: #FBF8EF; }
.portada { background: #17492A; border-radius: 18px; overflow: hidden; margin-bottom: 1.4rem; box-shadow: 0 8px 22px rgba(23,73,42,.18); }
.portada .toldo { height: 20px; background: repeating-linear-gradient(90deg, #D9482B 0 32px, #FFF8E7 32px 64px); }
.portada-texto { padding: 1.3rem 1.7rem 1.5rem; }
.portada-titulo { font-family: 'Barlow Condensed', sans-serif; font-weight: 700; font-size: 2.8rem; line-height: 1.05; color: #FFF8E7; }
.portada-sub { color: #DCEBD8; font-size: 1.05rem; margin-top: .45rem; }
.st-key-acceso, .st-key-planificar, .st-key-despensa { background: #FFFFFF; border-radius: 16px; box-shadow: 0 4px 16px rgba(30,42,34,.07); }
section[data-testid="stSidebar"] { background: #17492A; }
section[data-testid="stSidebar"] p, section[data-testid="stSidebar"] .marca { color: #FFF8E7 !important; }
section[data-testid="stSidebar"] div[role="radiogroup"] label { padding: .45rem .7rem; border-radius: 10px; width: 100%; }
section[data-testid="stSidebar"] div[role="radiogroup"] label:hover { background: rgba(255,248,231,.12); }
section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) { background: rgba(255,248,231,.2); }
section[data-testid="stSidebar"] .stButton > button { background: transparent; border: 1px solid #A9C7AE; }
section[data-testid="stSidebar"] button { color: #FFF8E7; }
.stButton > button[kind="primary"] { background: #B93A20; border-color: #B93A20; color: #FFFFFF; }
.stButton > button[kind="primary"]:hover { background: #972D17; border-color: #972D17; color: #FFFFFF; }
div[data-testid="stMetric"] { border-left: 6px solid #D9482B; box-shadow: 0 3px 10px rgba(30,42,34,.06); }
@media (max-width: 600px) { .portada-titulo { font-size: 2.1rem; } }
</style>
"""
st.markdown(ESTILO, unsafe_allow_html=True)


def portada(titulo, texto):
    st.markdown(f'<div class="portada"><div class="toldo"></div><div class="portada-texto">'
                f'<div class="portada-titulo">{titulo}</div><div class="portada-sub">{texto}</div>'
                f'</div></div>', unsafe_allow_html=True)


def boleta_html(df, total, integrantes, escenario):
    filas = ""
    for _, r in df.iterrows():
        if r["Comprar"] > 0:
            cant, monto, clase = lg.cantidad_txt(r["Comprar"], r["Producto"]), clp(r["Subtotal"]), ""
        else:
            cant, monto, clase = "ya lo tienes", "—", " listo"
        filas += (f'<div class="fila{clase}"><span class="nom">{html.escape(lg.nombre(r["Producto"]))}</span>'
                  f'<span class="puntos"></span><span class="cant">{cant}</span>'
                  f'<span class="monto">{monto}</span></div>')
    personas = "persona" if integrantes == 1 else "personas"
    return (f'<div class="boleta"><div class="toldo"></div><div class="cuerpo">'
            f'<div class="b-titulo">Tu lista de compras</div>'
            f'<div class="b-sub">Hogar de {integrantes} {personas}, consumo {escenario}</div>'
            f'{filas}<div class="total"><span>Total estimado</span><span>{clp(total)}</span></div>'
            f'</div></div>')


# ================= INICIO DE SESIÓN =================
if "uid" not in st.session_state:
    _, centro, _ = st.columns([1, 1.5, 1])
    with centro:
        st.image("portada.png", width="stretch")
        st.write("Calcula cuánta fruta y verdura comprar para tu hogar y compara con tu presupuesto.")
        with st.container(border=True, key="acceso"):
            tab_in, tab_reg = st.tabs(["Iniciar sesión", "Crear cuenta"])
            with tab_in:
                usuario = st.text_input("Usuario", key="login_user")
                clave = st.text_input("Clave", type="password", key="login_pass")
                if st.button("Entrar", type="primary", width="stretch"):
                    uid = db.iniciar_sesion(usuario, clave)
                    if uid:
                        st.session_state["uid"] = uid
                        st.session_state["nombre"] = usuario.strip()
                        st.rerun()
                    else:
                        st.error("Usuario o clave incorrectos.")
            with tab_reg:
                nuevo = st.text_input("Elige un usuario (mínimo 3 caracteres)", key="reg_user")
                clave1 = st.text_input("Elige una clave (mínimo 4 caracteres)", type="password", key="reg_pass")
                if st.button("Crear cuenta", type="primary", width="stretch"):
                    try:
                        db.registrar_usuario(nuevo, clave1)
                        st.success("Cuenta creada. Ahora inicia sesión.")
                    except ValueError as e:
                        st.error(str(e))
    st.stop()

uid = st.session_state["uid"]

# ================= MENÚ LATERAL =================
st.sidebar.markdown("<div class='marca'>Feria Justa</div>", unsafe_allow_html=True)
st.sidebar.caption(f"Sesión de {st.session_state['nombre']}")
pagina = st.sidebar.radio("Menú", ["Planificar compra", "Mi despensa", "Historial", "Comparar escenarios"],
                          label_visibility="collapsed")
st.sidebar.divider()
if st.sidebar.button("Cerrar sesión", width="stretch"):
    st.session_state.clear()
    st.rerun()
st.sidebar.caption("Cantidades y precios son estimaciones de ejemplo, sujetos a variación semanal y de temporada.")

# ================= PLANIFICAR =================
if pagina == "Planificar compra":
    portada("🛒 Tu compra de la semana", "Cuéntanos cómo es tu hogar. Para los productos del cuadro Productos, descontamos lo que tengas en Mi despensa.")
    despensa = db.obtener_despensa(uid)

    with st.container(border=True, key="planificar"):
        c1, c2, c3 = st.columns(3)
        integrantes = c1.number_input("Integrantes del hogar", 1, 15, 3)
        escenario = c2.selectbox("Nivel de consumo", lg.ESCENARIOS, index=min(1, len(lg.ESCENARIOS) - 1),
                                 format_func=str.capitalize)
        presupuesto = c3.number_input("Presupuesto semanal (CLP)", 0, 500000, 15000, step=1000)
        cats = st.multiselect("Categorías", lg.CATEGORIAS, default=lg.CATEGORIAS, format_func=etiqueta)
        opciones = lg.productos_de(cats)
        productos = st.multiselect("Productos", opciones, default=opciones[:8], format_func=lg.nombre)
        st.markdown("**Otros productos (escribe los que quieras)**")
        st.caption("Elige el producto y anota la cantidad total. El precio se pone solo.")
        otros = st.data_editor(
            pd.DataFrame({"Producto": pd.Series(dtype="str"), "Cantidad": pd.Series(dtype="float")}),
            num_rows="dynamic", hide_index=True, width="stretch", key="otros_lista",
            column_config={
                "Producto": st.column_config.SelectboxColumn(options=list(lg.PRECIOS_OTROS)),
                "Cantidad": st.column_config.NumberColumn(min_value=0.0),
            })
        precios = {}
        with st.expander("Ajustar precios (CLP por unidad o por kilo)"):
            pc = st.columns(3)
            for i, p in enumerate(productos):
                with pc[i % 3]:
                    precios[p] = st.number_input(f"{lg.nombre(p)} (por {'kg' if lg.UNIDADES[p] == 'kg' else 'unidad'})",
                                                 0, 100000, int(lg.PRECIOS_BASE[p]), step=50, key=f"precio_{p}")

    existencias = {p: despensa.get(p, 0.0) for p in productos}

    if st.button("Calcular lista de compras", type="primary"):
        extras = [x for x in otros.to_dict("records")
                  if any(pd.notna(x[k]) and str(x[k]).strip() for k in ("Producto", "Cantidad"))]
        if not productos and not extras:
            st.warning("Elige al menos un producto para calcular tu lista.")
            st.stop()
        try:
            df, total, ev = lg.calcular_lista(productos, escenario, integrantes, existencias, precios, presupuesto)
            df, total, ev = lg.agregar_extras(df, total, presupuesto, extras)
        except ValueError as e:
            st.error(str(e))
            st.stop()
        st.session_state["resultado"] = {"df": df, "total": total, "ev": ev,
                                         "integrantes": integrantes, "escenario": escenario}

    r = st.session_state.get("resultado")
    if r:
        ev = r["ev"]
        izq, der = st.columns([3, 2], gap="large")
        with izq:
            st.markdown(boleta_html(r["df"], r["total"], r["integrantes"], r["escenario"]), unsafe_allow_html=True)
        with der:
            st.metric("Costo estimado", clp(r["total"]))
            st.metric("Presupuesto", clp(ev["presupuesto"]))
            if ev["presupuesto"] > 0:
                st.progress(min(r["total"] / ev["presupuesto"], 1.0))
            if ev["alcanza"]:
                st.success(f"Estás dentro del presupuesto. Te sobran {clp(ev['diferencia'])}.")
            else:
                st.warning(f"Te pasas por {clp(-ev['diferencia'])}. Prueba con un consumo más bajo o quita algún producto.")
            # CSV listo para Excel en español: separador ";", coma decimal y tildes (UTF-8 con BOM)
            lista = r["df"].copy()
            lista["Producto"] = lista["Producto"].map(lg.nombre)
            lista = lista.rename(columns={"Precio": "Precio unitario (CLP)", "Subtotal": "Subtotal (CLP)"})
            st.download_button("Descargar lista (Excel)", lista.to_csv(index=False, sep=";", decimal=",").encode("utf-8-sig"),
                               "lista_compras.csv", "text/csv", width="stretch")
            if st.button("Guardar esta compra", type="primary", width="stretch"):
                filas = [{"producto": x["Producto"], "kg": x["Comprar"], "subtotal": x["Subtotal"]}
                         for _, x in r["df"].iterrows() if x["Comprar"] > 0]
                if filas:
                    db.registrar_compra(uid, filas, r["total"])
                    st.success("Compra guardada. Tu despensa se actualizó.")
                else:
                    st.info("No había nada que comprar, así que no se guardó nada.")
                del st.session_state["resultado"]

# ================= DESPENSA =================
elif pagina == "Mi despensa":
    portada("🧺 Mi despensa", "Anota cuánto tienes en casa. Al calcular tu compra, se descuenta automáticamente.")
    despensa = db.obtener_despensa(uid)

    filtro = st.selectbox("Categoría", ["Todas"] + lg.CATEGORIAS,
                          format_func=lambda c: c if c == "Todas" else etiqueta(c))
    mostrados = lg.PRODUCTOS if filtro == "Todas" else lg.productos_de([filtro])

    nuevo = {}
    with st.container(border=True, key="despensa"):
        cols = st.columns(3)
        for i, p in enumerate(mostrados):
            with cols[i % 3]:
                nuevo[p] = st.number_input(f"{lg.nombre(p)} ({lg.abrev(p)})", 0.0, 1000.0,
                                           float(despensa.get(p, 0.0)),
                                           step=0.5 if lg.UNIDADES[p] == "kg" else 1.0, key=f"desp_{p}")
    if st.button("Guardar despensa", type="primary"):
        db.guardar_despensa(uid, nuevo)
        st.success("Despensa guardada.")

# ================= HISTORIAL =================
elif pagina == "Historial":
    portada("🧾 Mis compras", "Revisa las listas que has guardado.")
    compras = db.historial(uid)
    if not compras:
        st.info("Todavía no has guardado compras. Calcula tu lista y pulsa Guardar esta compra.")
    else:
        st.dataframe(pd.DataFrame(compras).rename(columns={"id": "N°", "fecha": "Fecha", "total": "Total"}),
                     hide_index=True, width="stretch",
                     column_config={"Total": st.column_config.NumberColumn(format="$%d")})
        elegida = st.selectbox("Ver el detalle de la compra N°", [c["id"] for c in compras])
        detalle = pd.DataFrame([{"Producto": lg.nombre(d["producto"]),
                                 "Cantidad": lg.cantidad_txt(d["kg"], d["producto"]) if d["producto"] in lg.UNIDADES else d["kg"],
                                 "Subtotal": d["subtotal"]} for d in db.detalle_compra(elegida)])
        st.dataframe(detalle, hide_index=True, width="stretch",
                     column_config={"Subtotal": st.column_config.NumberColumn(format="$%d")})

# ================= COMPARAR =================
else:
    portada("📊 Comparar escenarios", "Mira cuánto necesita tu hogar y cuánto cuesta según el nivel de consumo.")
    integrantes = st.number_input("Integrantes del hogar", 1, 15, 3)
    base, hogar, costos = lg.comparar(integrantes, lg.PRECIOS_BASE)

    st.subheader("Matriz de consumo por persona")
    st.caption("Filas: escenarios. Columnas: productos.")
    st.dataframe(lg.tabla_matriz(base))
    st.subheader(f"Matriz del hogar ({integrantes} × la matriz por persona)")
    st.dataframe(lg.tabla_matriz(hogar))
    st.subheader("Costo semanal por escenario")
    st.caption("Matriz del hogar × vector de precios de ejemplo.")
    st.bar_chart(pd.Series(costos, index=[e.capitalize() for e in lg.ESCENARIOS]))
    st.info(f"Pasar de consumo {lg.ESCENARIOS[0]} a {lg.ESCENARIOS[-1]} cuesta {clp(costos[-1] - costos[0])} más por semana.")
