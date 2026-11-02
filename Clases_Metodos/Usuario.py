class Usuario:
    def __init__(self, id_usuario, nombre, apellido, correo, fecha_nacimiento, tiene_tarjeta=False, es_admin=False):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.apellido = apellido
        self.correo = correo
        self.fecha_nacimiento = fecha_nacimiento
        self.tiene_tarjeta = bool(tiene_tarjeta)  # tarjeta de descuento del cine
        self.es_admin = bool(es_admin)

    @classmethod
    def desde_fila(cls, fila):
        """Crea un Usuario a partir de una fila de la tabla usuarios."""
        return cls(fila["id"], fila["nombre"], fila["apellido"], fila["correo"],
                   fila["fecha_nacimiento"], fila["tiene_tarjeta"], fila["es_admin"])

    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"

    def __str__(self):
        return f"{self.nombre_completo()} ({self.correo})"
