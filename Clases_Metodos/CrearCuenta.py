from datetime import datetime

from BaseDeDatos.conexion import ejecutar, encriptar


class CrearCuenta:
    def __init__(self, nombre, apellido, correo, contrasenia, repetir_contrasenia, fecha_nacimiento, tiene_tarjeta=False):
        self.nombre = nombre.strip()
        self.apellido = apellido.strip()
        self.correo = correo.strip().lower()
        self.contrasenia = contrasenia
        self.repetir_contrasenia = repetir_contrasenia
        self.fecha_nacimiento = fecha_nacimiento.strip()
        self.tiene_tarjeta = tiene_tarjeta

    def validar_contrasenia(self):
        return self.contrasenia == self.repetir_contrasenia

    def validar_correo(self):
        partes = self.correo.split("@")
        return len(partes) == 2 and partes[0] != "" and "." in partes[1]

    def validar_fecha(self):
        try:
            fecha = datetime.strptime(self.fecha_nacimiento, "%d/%m/%Y")
        except ValueError:
            return False
        return fecha < datetime.now()

    def validar(self):
        """Devuelve una lista con los errores encontrados (vacía si está todo bien)."""
        campos = [self.nombre, self.apellido, self.correo, self.contrasenia,
                  self.repetir_contrasenia, self.fecha_nacimiento]
        if "" in campos:
            return ["Complete todos los campos."]
        errores = []
        if not self.validar_correo():
            errores.append("El correo no es válido.")
        if len(self.contrasenia) < 4:
            errores.append("La contraseña debe tener al menos 4 caracteres.")
        if not self.validar_contrasenia():
            errores.append("Las contraseñas no coinciden.")
        if not self.validar_fecha():
            errores.append("La fecha de nacimiento debe tener el formato dd/mm/aaaa.")
        return errores

    def guardar(self):
        """Guarda la cuenta. Si el correo ya existe, sqlite lanza IntegrityError."""
        return ejecutar(
            "INSERT INTO usuarios (nombre, apellido, correo, contrasenia, fecha_nacimiento, tiene_tarjeta) "
            "VALUES (?, ?, ?, ?, ?, ?)",  # los ? evitan la inyección SQL
            (self.nombre, self.apellido, self.correo, encriptar(self.contrasenia),
             self.fecha_nacimiento, int(self.tiene_tarjeta)))
