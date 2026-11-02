from BaseDeDatos.conexion import consultar, encriptar
from Clases_Metodos.Usuario import Usuario


class InicioSesion:
    def __init__(self, correo, contrasenia):
        self.correo = correo.strip().lower()
        self.contrasenia = contrasenia

    def validar(self):
        """Devuelve el Usuario si el correo y la contraseña son correctos, o None."""
        if not self.correo or not self.contrasenia:
            return None
        filas = consultar("SELECT * FROM usuarios WHERE correo = ? AND contrasenia = ?",
                          (self.correo, encriptar(self.contrasenia)))
        if filas:
            return Usuario.desde_fila(filas[0])
        return None
