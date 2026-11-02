"""Ventanas de inicio de sesión y de registro."""
import sqlite3
import tkinter as tk
from tkinter import messagebox as mb

from Clases_Metodos.CrearCuenta import CrearCuenta
from Clases_Metodos.InicioSesion import InicioSesion
from Ventanas.comun import GRIS, ROJO, centrar, poner_fondo


def campo(contenedor, texto, oculto=False):
    """Crea una etiqueta y una caja de texto debajo. Devuelve la caja de texto."""
    tk.Label(contenedor, text=texto, font=("Arial", 12, "bold"), fg=ROJO, bg="white").pack(anchor="w", padx=40)
    entrada = tk.Entry(contenedor, font=("Arial", 13), bg="lightgray", show="*" if oculto else "")
    entrada.pack(fill="x", padx=40, pady=(0, 8), ipady=4)
    return entrada


class VentanaLogin(tk.Toplevel):
    def __init__(self, master, al_ingresar):
        super().__init__(master)
        self.al_ingresar = al_ingresar  # función que se llama cuando el login es correcto
        self.title("Iniciar sesión")
        self.resizable(False, False)
        centrar(self, 1100, 600)
        poner_fondo(self, "proyecto01-1.png")

        caja = tk.Frame(self, bg="white")
        caja.place(x=365, y=120, width=370, height=360)
        tk.Label(caja, text="Iniciar Sesión", font=("Arial", 28, "bold"), fg=ROJO, bg="white").pack(pady=(25, 15))
        self.correo = campo(caja, "Correo")
        self.contrasenia = campo(caja, "Contraseña", oculto=True)
        tk.Button(caja, text="Ingresar", width=20, bg=GRIS, command=self.ingresar).pack(pady=(12, 6))
        tk.Button(caja, text="¿No tenés cuenta? Crear cuenta", bd=0, bg="white", fg=ROJO,
                  cursor="hand2", command=self.ir_a_registro).pack()

        self.bind("<Return>", lambda evento: self.ingresar())
        self.correo.focus()

    def ingresar(self):
        usuario = InicioSesion(self.correo.get(), self.contrasenia.get()).validar()
        if usuario is None:
            mb.showerror("Login incorrecto", "Correo o contraseña incorrectos.", parent=self)
            return
        self.destroy()
        self.al_ingresar(usuario)

    def ir_a_registro(self):
        master, al_ingresar = self.master, self.al_ingresar
        self.destroy()
        # cuando termina el registro, volvemos a mostrar el login
        VentanaRegistro(master, al_terminar=lambda: VentanaLogin(master, al_ingresar))


class VentanaRegistro(tk.Toplevel):
    def __init__(self, master, al_terminar=None):
        super().__init__(master)
        self.al_terminar = al_terminar
        self.title("Registro de usuario")
        self.resizable(False, False)
        centrar(self, 1100, 600)
        poner_fondo(self, "CINE.Proyecto1.png")

        caja = tk.Frame(self, bg="white")
        caja.place(x=80, y=20, width=360, height=560)
        tk.Label(caja, text="Crear cuenta", font=("Arial", 22, "bold"), fg=ROJO, bg="white").pack(pady=(12, 6))
        self.nombre = campo(caja, "Nombre")
        self.apellido = campo(caja, "Apellido")
        self.correo = campo(caja, "Correo")
        self.contrasenia = campo(caja, "Contraseña", oculto=True)
        self.repetir = campo(caja, "Repetir contraseña", oculto=True)
        self.fecha = campo(caja, "Fecha de nacimiento (dd/mm/aaaa)")
        self.tarjeta = tk.BooleanVar()
        tk.Checkbutton(caja, text="Tengo tarjeta de descuento Cinemar", variable=self.tarjeta,
                       bg="white").pack(anchor="w", padx=36)
        tk.Button(caja, text="Registrarme", width=20, bg=GRIS, command=self.registrar).pack(pady=8)
        self.nombre.focus()

    def registrar(self):
        cuenta = CrearCuenta(self.nombre.get(), self.apellido.get(), self.correo.get(),
                             self.contrasenia.get(), self.repetir.get(), self.fecha.get(), self.tarjeta.get())
        errores = cuenta.validar()
        if errores:
            mb.showerror("Revise los datos", "\n".join(errores), parent=self)
            return
        try:
            cuenta.guardar()
        except sqlite3.IntegrityError:
            mb.showerror("Correo en uso", "Ya existe una cuenta con ese correo.", parent=self)
            return
        mb.showinfo("Registro correcto", "¡Tu cuenta fue creada! Ya podés iniciar sesión.", parent=self)
        self.destroy()
        if self.al_terminar:
            self.al_terminar()
