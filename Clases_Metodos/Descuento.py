from BaseDeDatos.conexion import consultar

DIAS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]


class Descuento:
    def __init__(self, dia, porcentaje):
        self.dia = dia                # 0 = lunes ... 6 = domingo
        self.porcentaje = porcentaje

    @property
    def nombre_dia(self):
        return DIAS[self.dia]

    @classmethod
    def del_dia(cls, fecha):
        """Busca el descuento que corresponde al día de la semana de esa fecha."""
        dia = fecha.weekday()
        filas = consultar("SELECT porcentaje FROM descuentos WHERE dia = ?", (dia,))
        return cls(dia, filas[0]["porcentaje"] if filas else 0)

    def aplicar(self, precio):
        return round(precio * (1 - self.porcentaje / 100), 2)


def precio_final(precio, fecha, tiene_tarjeta):
    """Solo los clientes con tarjeta de descuento pagan menos."""
    if not tiene_tarjeta:
        return precio
    return Descuento.del_dia(fecha).aplicar(precio)
