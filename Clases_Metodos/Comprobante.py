from datetime import datetime


class Comprobante:
    def __init__(self, cliente, pelicula, sala, fecha, butacas, precio_unitario):
        self.cliente = cliente
        self.pelicula = pelicula
        self.sala = sala
        self.fecha = fecha
        self.butacas = butacas
        self.precio_unitario = precio_unitario
        self.fecha_de_compra = datetime.now()

    @property
    def total(self):
        return self.precio_unitario * len(self.butacas)

    def texto(self):
        return (f"CINEMAR - Comprobante de reserva\n\n"
                f"Cliente: {self.cliente}\n"
                f"Película: {self.pelicula}\n"
                f"{self.sala} - {self.fecha} a las {self.sala.horario}\n"
                f"Butacas: {', '.join(self.butacas)}\n"
                f"Precio por entrada: ${self.precio_unitario:,.2f}\n"
                f"TOTAL PAGADO: ${self.total:,.2f}\n\n"
                f"Fecha de compra: {self.fecha_de_compra:%d/%m/%Y %H:%M}")
