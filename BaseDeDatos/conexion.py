"""
Conexión a la base de datos del cine.

Antes había 3 bases separadas (login, películas y productos).
Ahora todo está en un solo archivo: BaseDeDatos/cinemar.db
La base se crea sola la primera vez que se ejecuta el programa.
"""
import hashlib
import os
import sqlite3

CARPETA = os.path.dirname(os.path.abspath(__file__))
RUTA_DB = os.path.join(CARPETA, "cinemar.db")
# Bases de la versión anterior (solo se usan para copiar los datos viejos)
CARPETA_VIEJA = os.path.join(os.path.dirname(CARPETA), "VersionesAnteriores", "BaseDeDatos")


def conectar():
    conexion = sqlite3.connect(RUTA_DB)
    conexion.row_factory = sqlite3.Row  # permite usar fila["nombre"]
    conexion.execute("PRAGMA foreign_keys = ON")
    return conexion


def consultar(sql, parametros=()):
    """Ejecuta un SELECT y devuelve la lista de filas."""
    conexion = conectar()
    try:
        return conexion.execute(sql, parametros).fetchall()
    finally:
        conexion.close()


def ejecutar(sql, parametros=()):
    """Ejecuta un INSERT / UPDATE / DELETE y guarda los cambios."""
    conexion = conectar()
    try:
        with conexion:  # hace commit solo, o rollback si hay error
            cursor = conexion.execute(sql, parametros)
            return cursor.lastrowid
    finally:
        conexion.close()


def ejecutar_varios(sql, lista_parametros):
    """Ejecuta la misma consulta varias veces. Si una falla, no se guarda ninguna."""
    conexion = conectar()
    try:
        with conexion:
            conexion.executemany(sql, lista_parametros)
    finally:
        conexion.close()


def encriptar(contrasenia):
    """Las contraseñas no se guardan tal cual, sino su 'huella' (hash SHA-256)."""
    return hashlib.sha256(str(contrasenia).encode("utf-8")).hexdigest()


TABLAS = """
CREATE TABLE IF NOT EXISTS usuarios (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre           TEXT NOT NULL,
    apellido         TEXT NOT NULL,
    correo           TEXT NOT NULL UNIQUE,
    contrasenia      TEXT NOT NULL,
    fecha_nacimiento TEXT NOT NULL,
    tiene_tarjeta    INTEGER NOT NULL DEFAULT 0,
    es_admin         INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS peliculas (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre        TEXT NOT NULL,
    sinopsis      TEXT,
    clasificacion TEXT,
    genero        TEXT,
    duracion      INTEGER,
    director      TEXT,
    actores       TEXT
);

CREATE TABLE IF NOT EXISTS salas (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    numero           INTEGER NOT NULL UNIQUE,
    tipo             TEXT NOT NULL,
    precio           REAL NOT NULL,
    filas            INTEGER NOT NULL,
    butacas_por_fila INTEGER NOT NULL,
    horario          TEXT NOT NULL,
    pelicula_id      INTEGER NOT NULL REFERENCES peliculas(id)
);

-- UNIQUE(sala_id, fecha, butaca): una butaca no se puede vender dos veces
CREATE TABLE IF NOT EXISTS reservas (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL REFERENCES usuarios(id),
    sala_id    INTEGER NOT NULL REFERENCES salas(id),
    fecha      TEXT NOT NULL,
    butaca     TEXT NOT NULL,
    precio     REAL NOT NULL,
    UNIQUE (sala_id, fecha, butaca)
);

CREATE TABLE IF NOT EXISTS productos (
    id     INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    precio REAL NOT NULL
);

-- dia: 0 = lunes ... 6 = domingo
CREATE TABLE IF NOT EXISTS descuentos (
    dia        INTEGER PRIMARY KEY,
    porcentaje REAL NOT NULL
);
"""


def crear_base():
    """Crea las tablas si no existen y carga datos iniciales la primera vez."""
    es_nueva = not os.path.exists(RUTA_DB)
    conexion = conectar()
    try:
        conexion.executescript(TABLAS)
    finally:
        conexion.close()
    if es_nueva:
        cargar_datos_iniciales()


def cargar_datos_iniciales():
    # Descuentos del README: lunes y miércoles 20%, martes y jueves 15%, vie/sáb/dom 10%
    ejecutar_varios("INSERT INTO descuentos VALUES (?, ?)",
                    [(0, 20), (1, 15), (2, 20), (3, 15), (4, 10), (5, 10), (6, 10)])

    # Usuario administrador para poder entrar al panel de administración
    ejecutar("INSERT INTO usuarios (nombre, apellido, correo, contrasenia, fecha_nacimiento, es_admin) "
             "VALUES ('Admin', 'Cinemar', 'admin@cinemar.com', ?, '01/01/2000', 1)", (encriptar("admin123"),))

    # Películas y salas de ejemplo
    p1 = ejecutar("INSERT INTO peliculas (nombre, sinopsis, clasificacion, genero, duracion, director, actores) "
                  "VALUES ('Intensamente 2', 'Riley entra en la adolescencia y aparecen emociones nuevas.', "
                  "'ATP', 'Animación', 96, 'Kelsey Mann', 'Amy Poehler, Maya Hawke')")
    p2 = ejecutar("INSERT INTO peliculas (nombre, sinopsis, clasificacion, genero, duracion, director, actores) "
                  "VALUES ('Duna: Parte Dos', 'Paul Atreides se une a los Fremen en el desierto de Arrakis.', "
                  "'+13', 'Ciencia ficción', 166, 'Denis Villeneuve', 'Timothée Chalamet, Zendaya')")
    ejecutar("INSERT INTO salas (numero, tipo, precio, filas, butacas_por_fila, horario, pelicula_id) "
             "VALUES (1, '2D', 4000, 6, 8, '18:30', ?)", (p1,))
    ejecutar("INSERT INTO salas (numero, tipo, precio, filas, butacas_por_fila, horario, pelicula_id) "
             "VALUES (2, '3D', 5500, 8, 10, '21:00', ?)", (p2,))

    copiar_datos_viejos()


def _leer_base_vieja(nombre_archivo, sql):
    ruta = os.path.join(CARPETA_VIEJA, nombre_archivo)
    if not os.path.exists(ruta):
        return []
    try:
        conexion = sqlite3.connect(ruta)
        filas = conexion.execute(sql).fetchall()
        conexion.close()
        return filas
    except sqlite3.Error:
        return []


def copiar_datos_viejos():
    """Copia usuarios, películas y productos de las bases de la versión anterior."""
    for nombre, apellido, contrasenia, correo, fecha in _leer_base_vieja(
            "BaseDeDatosLogin.db", "SELECT nombre, apellido, contrasenia, correo, fecha_de_nacimiento FROM registro"):
        # INSERT OR IGNORE: si el correo ya existe, no lo repite
        ejecutar("INSERT OR IGNORE INTO usuarios (nombre, apellido, correo, contrasenia, fecha_nacimiento) "
                 "VALUES (?, ?, ?, ?, ?)",
                 (nombre, apellido, str(correo).strip().lower(), encriptar(contrasenia), str(fecha)))

    for fila in _leer_base_vieja("BaseDeDatosPelicula.db",
                                 "SELECT nombre, sinopsis, clasificacion, genero, duracion, director, actores FROM pelicula"):
        ejecutar("INSERT INTO peliculas (nombre, sinopsis, clasificacion, genero, duracion, director, actores) "
                 "VALUES (?, ?, ?, ?, ?, ?, ?)", fila)

    for fila in _leer_base_vieja("BaseDeDatos.db", "SELECT nombre, precio FROM productos"):
        ejecutar("INSERT INTO productos (nombre, precio) VALUES (?, ?)", fila)
