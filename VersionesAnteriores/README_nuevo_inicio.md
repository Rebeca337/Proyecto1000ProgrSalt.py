## Trabajo_Final_Cinemar

Sistema de gestión de un cine hecho en **Python + Tkinter + SQLite**.

### Cómo ejecutarlo

1. Tener instalado Python 3.8 o superior (en Windows ya trae Tkinter y SQLite).
2. Abrir una terminal en esta carpeta y ejecutar:

```
python main.py
```

La base de datos (`BaseDeDatos/cinemar.db`) se crea sola la primera vez, con datos de ejemplo
y con los usuarios, películas y productos de la versión anterior.

**Usuario administrador:** `admin@cinemar.com` / contraseña `admin123`
(los clientes pueden crear su cuenta desde la ventana de inicio de sesión).

### Estructura

```
main.py                  -> ventana principal (menú). Es el archivo que se ejecuta.
BaseDeDatos/
    conexion.py          -> conexión a la base, creación de tablas y datos iniciales
Clases_Metodos/          -> clases del sistema (lógica, sin ventanas)
    Usuario, CrearCuenta, InicioSesion, Peliculas, Sala, Butacas,
    Reserva, Descuento, Comprobante
Ventanas/                -> pantallas de Tkinter
    usuarios.py          -> iniciar sesión y registrarse
    cartelera.py         -> cartelera, elegir butacas, mis reservas
    candy.py             -> productos del candy
    admin.py             -> panel de administración
    comun.py             -> funciones compartidas (centrar ventana, imágenes, fechas)
Imagenes/                -> fondos de las ventanas
DiagramaUML/             -> diagrama de clases
VersionesAnteriores/     -> código y bases de datos de la primera versión (como referencia)
```

### Qué hace

**Cliente:** registrarse, iniciar sesión, ver la cartelera, reservar butacas (elige fecha y
butacas en un mapa de la sala), ver sus reservas y el historial de entradas, y modificar una
reserva (cambiar fecha o butaca) siempre que la función no haya empezado.

**Administración:** ver las reservas de todos los clientes o buscar las de un cliente, crear,
modificar y eliminar salas (con su película, tipo 2D/3D, precio, tamaño y horario), películas
y productos, y modificar la tabla de descuentos.

**Reglas que respeta el sistema:**
- No se puede vender más entradas que butacas: cada butaca se puede reservar una sola vez por
  función (lo controla la base de datos con `UNIQUE(sala_id, fecha, butaca)`).
- El descuento se aplica solo a clientes con tarjeta de descuento, según el día de la semana.
- La reserva implica el pago: al confirmar se muestra el comprobante con el total.
- Las contraseñas se guardan encriptadas (SHA-256) y todas las consultas usan parámetros `?`
  para evitar inyección SQL.

### Cambios respecto de la primera versión

- Una sola base de datos en lugar de tres, y un solo `main.py` que une todas las ventanas.
- Se arreglaron las rutas de las imágenes (antes buscaban `ProyectoCinemar/imagenes/`).
- Se arregló la tabla de Películas (los encabezados hacían que se cerrara con error).
- Se agregaron las reservas reales de butacas, los descuentos, "Mis reservas" y el panel de
  administración, que antes no estaban.
- Las clases ahora tienen métodos que usa el programa (por ejemplo `Descuento.aplicar()`,
  `Sala.butacas()`, `Reserva.se_puede_modificar()`).

---

