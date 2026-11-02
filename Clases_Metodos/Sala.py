import re

from BaseDeDatos.conexion import consultar
from Clases_Metodos.Butacas import Butaca

LETRAS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


class Sala:
    def __init__(self, id_sala, numero, tipo, precio, filas, butacas_por_fila, horario, id_pelicula):
        self.id_sala = id_sala
        self.numero = numero
        self.tipo = tipo                  # "2D" o "3D"
        self.precio = precio              # precio de la entrada sin descuento
        self.filas = filas
        self.butacas_por_fila = butacas_por_fila
        self.horario = horario            # "21:00" (las funciones son todos los días)
        self.id_pelicula = id_pelicula

    @classmethod
    def buscar(cls, id_sala):
        filas = consultar("SELECT * FROM salas WHERE id = ?", (id_sala,))
        if not filas:
            return None
        f = filas[0]
        return cls(f["id"], f["numero"], f["tipo"], f["precio"], f["filas"],
                   f["butacas_por_fila"], f["horario"], f["pelicula_id"])

    @property
    def capacidad(self):
        return self.filas * self.butacas_por_fila

    def butacas(self, fecha):
        """Devuelve las butacas de la sala (una lista por fila) marcando las ya reservadas en esa fecha."""
        ocupadas = {f["butaca"] for f in consultar(
            "SELECT butaca FROM reservas WHERE sala_id = ? AND fecha = ?", (self.id_sala, fecha))}
        resultado = []
        for i in range(self.filas):
            letra = LETRAS[i]
            fila = [Butaca(letra, n, f"{letra}{n}" in ocupadas) for n in range(1, self.butacas_por_fila + 1)]
            resultado.append(fila)
        return resultado

    def lugares_libres(self, fecha):
        cantidad = consultar("SELECT COUNT(*) AS c FROM reservas WHERE sala_id = ? AND fecha = ?",
                             (self.id_sala, fecha))[0]["c"]
        return self.capacidad - cantidad

    @staticmethod
    def validar_datos(datos):
        """Revisa los datos que carga el administrador. Devuelve un texto de error o None."""
        if datos["tipo"] not in ("2D", "3D"):
            return "El tipo de sala debe ser 2D o 3D."
        if datos["precio"] <= 0:
            return "El precio debe ser mayor a 0."
        if not 1 <= datos["filas"] <= 26:
            return "La sala debe tener entre 1 y 26 filas."
        if not 1 <= datos["butacas_por_fila"] <= 20:
            return "Cada fila debe tener entre 1 y 20 butacas."
        if not re.fullmatch(r"([01]\d|2[0-3]):[0-5]\d", datos["horario"]):
            return "El horario debe tener el formato HH:MM (por ejemplo 21:30)."
        return None

    def __str__(self):
        return f"Sala {self.numero} ({self.tipo})"
