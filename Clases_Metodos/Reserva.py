from datetime import datetime

from BaseDeDatos.conexion import ejecutar, ejecutar_varios


class Reserva:
    def __init__(self, id_reserva, id_usuario, id_sala, fecha, butaca, precio, horario):
        self.id_reserva = id_reserva
        self.id_usuario = id_usuario
        self.id_sala = id_sala
        self.fecha = fecha        # "2026-11-02"
        self.butaca = butaca      # "B4"
        self.precio = precio      # lo que se pagó (la reserva implica el pago)
        self.horario = horario    # horario de la función, "21:00"

    def fecha_hora_funcion(self):
        return datetime.strptime(f"{self.fecha} {self.horario}", "%Y-%m-%d %H:%M")

    def se_puede_modificar(self):
        """Las reservas solo se pueden modificar antes de la función."""
        return self.fecha_hora_funcion() > datetime.now()

    def modificar(self, nueva_fecha, nueva_butaca, nuevo_precio):
        if not self.se_puede_modificar():
            raise ValueError("La función ya empezó, la reserva no se puede modificar.")
        ejecutar("UPDATE reservas SET fecha = ?, butaca = ?, precio = ? WHERE id = ?",
                 (nueva_fecha, nueva_butaca, nuevo_precio, self.id_reserva))
        self.fecha, self.butaca, self.precio = nueva_fecha, nueva_butaca, nuevo_precio

    @staticmethod
    def reservar(id_usuario, id_sala, fecha, butacas, precio):
        """Guarda una reserva por cada butaca. Si alguna ya estaba ocupada no se guarda ninguna."""
        ejecutar_varios(
            "INSERT INTO reservas (usuario_id, sala_id, fecha, butaca, precio) VALUES (?, ?, ?, ?, ?)",
            [(id_usuario, id_sala, fecha, b, precio) for b in butacas])
