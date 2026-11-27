import hashlib
import hmac
import os
import sqlite3
from datetime import datetime

DB = "feria_justa.db"


def conectar():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys = ON")
    return con


def crear_tablas():
    con = conectar()
    con.executescript("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT UNIQUE NOT NULL,
        sal TEXT NOT NULL,
        clave_hash TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS despensa (
        usuario_id INTEGER NOT NULL REFERENCES usuarios(id),
        producto TEXT NOT NULL,
        kg REAL NOT NULL DEFAULT 0,
        PRIMARY KEY (usuario_id, producto)
    );
    CREATE TABLE IF NOT EXISTS compras (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER NOT NULL REFERENCES usuarios(id),
        fecha TEXT NOT NULL,
        total REAL NOT NULL
    );
    CREATE TABLE IF NOT EXISTS compras_detalle (
        compra_id INTEGER NOT NULL REFERENCES compras(id),
        producto TEXT NOT NULL,
        kg REAL NOT NULL,
        subtotal REAL NOT NULL
    );
    """)
    con.commit()
    con.close()


# ---------- Usuarios ----------
def _hash(clave, sal):
    return hashlib.pbkdf2_hmac("sha256", clave.encode(), sal, 100_000).hex()


def registrar_usuario(nombre, clave):
    nombre = nombre.strip()
    if len(nombre) < 3 or len(clave) < 4:
        raise ValueError("Usuario mínimo 3 caracteres y clave mínimo 4")
    sal = os.urandom(16)
    con = conectar()
    try:
        con.execute("INSERT INTO usuarios (nombre, sal, clave_hash) VALUES (?,?,?)",
                    (nombre, sal.hex(), _hash(clave, sal)))
        con.commit()
    except sqlite3.IntegrityError:
        raise ValueError("Ese usuario ya existe")
    finally:
        con.close()


def iniciar_sesion(nombre, clave):
    """Devuelve el id del usuario o None si los datos son incorrectos."""
    con = conectar()
    fila = con.execute("SELECT * FROM usuarios WHERE nombre = ?", (nombre.strip(),)).fetchone()
    con.close()
    if fila is None:
        return None
    esperado = _hash(clave, bytes.fromhex(fila["sal"]))
    return fila["id"] if hmac.compare_digest(esperado, fila["clave_hash"]) else None


# ---------- Despensa ----------
def obtener_despensa(uid):
    con = conectar()
    filas = con.execute("SELECT producto, kg FROM despensa WHERE usuario_id = ?", (uid,)).fetchall()
    con.close()
    return {f["producto"]: f["kg"] for f in filas}


def guardar_despensa(uid, stock):
    """Reemplaza las cantidades de la despensa. stock = {producto: kg}"""
    con = conectar()
    for producto, kg in stock.items():
        con.execute("""INSERT INTO despensa (usuario_id, producto, kg) VALUES (?,?,?)
                       ON CONFLICT(usuario_id, producto) DO UPDATE SET kg = excluded.kg""",
                    (uid, producto, kg))
    con.commit()
    con.close()


# ---------- Compras ----------
def registrar_compra(uid, filas, total):
    """filas = [{'producto':..., 'kg':..., 'subtotal':...}]. Guarda la compra
    y suma lo comprado a la despensa."""
    con = conectar()
    cur = con.execute("INSERT INTO compras (usuario_id, fecha, total) VALUES (?,?,?)",
                      (uid, datetime.now().strftime("%Y-%m-%d %H:%M"), total))
    compra_id = cur.lastrowid
    for f in filas:
        con.execute("INSERT INTO compras_detalle VALUES (?,?,?,?)",
                    (compra_id, f["producto"], f["kg"], f["subtotal"]))
        con.execute("""INSERT INTO despensa (usuario_id, producto, kg) VALUES (?,?,?)
                       ON CONFLICT(usuario_id, producto) DO UPDATE SET kg = kg + excluded.kg""",
                    (uid, f["producto"], f["kg"]))
    con.commit()
    con.close()


def historial(uid):
    con = conectar()
    filas = con.execute("SELECT id, fecha, total FROM compras WHERE usuario_id = ? ORDER BY id DESC",
                        (uid,)).fetchall()
    con.close()
    return [dict(f) for f in filas]


def detalle_compra(compra_id):
    con = conectar()
    filas = con.execute("SELECT producto, kg, subtotal FROM compras_detalle WHERE compra_id = ?",
                        (compra_id,)).fetchall()
    con.close()
    return [dict(f) for f in filas]
