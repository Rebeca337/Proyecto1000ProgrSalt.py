"""
CINEMAR - Sistema de gestión de un cine
Ejecutar este archivo para abrir el programa:   python main.py
"""
import tkinter as tk
from tkinter import messagebox as mb

from BaseDeDatos.conexion import crear_base
from Ventanas.admin import VentanaAdmin
from Ventanas.candy import VentanaCandy
from Ventanas.cartelera import VentanaCartelera, VentanaMisReservas
from Ventanas.comun import centrar, cargar_imagen, poner_fondo
from Ventanas.usuarios import VentanaLogin


class App:
    def __init__(self):
        crear_base()
        self.usuario = None  # usuario que inició sesión (None = nadie)

        self.ventana = tk.Tk()
        self.ventana.title("C  I  N  E  M  A  R")
        self.ventana.resizable(False, False)
        centrar(self.ventana, 1269, 639)
        poner_fondo(self.ventana, "test1.png")

        # menú de arriba
        estilo = {"bd": 0, "bg": "white", "font": ("Arial", 10, "bold"), "cursor": "hand2"}
        tk.Button(self.ventana, text="Cartelera", command=self.abrir_cartelera, **estilo).place(x=480, y=10)
        tk.Button(self.ventana, text="Candy", command=lambda: VentanaCandy(self.ventana), **estilo).place(x=580, y=10)
        tk.Button(self.ventana, text="Mis reservas", command=self.abrir_mis_reservas, **estilo).place(x=660, y=10)
        self.boton_admin = tk.Button(self.ventana, text="Administración", command=lambda: VentanaAdmin(self.ventana), **estilo)

        self.saludo = tk.Label(self.ventana, text="", bg="white", font=("Arial", 10))
        icono = cargar_imagen("logintes.png")
        if icono:
            icono = icono.subsample(30, 30)  # achicamos la imagen
        self.boton_sesion = tk.Button(self.ventana, image=icono, text="Ingresar", compound="left",
                                      command=self.boton_sesion_click, **estilo)
        self.boton_sesion.image = icono
        self.boton_sesion.place(x=1150, y=8)
        self.actualizar_menu()

    # --- sesión ---
    def pedir_usuario(self, accion):
        """Ejecuta 'accion' si hay alguien logueado; si no, primero abre el login."""
        if self.usuario:
            accion()
        else:
            VentanaLogin(self.ventana, al_ingresar=lambda usuario: (self.iniciar_sesion(usuario), accion()))

    def iniciar_sesion(self, usuario):
        self.usuario = usuario
        self.actualizar_menu()

    def boton_sesion_click(self):
        if self.usuario is None:
            VentanaLogin(self.ventana, al_ingresar=self.iniciar_sesion)
        elif mb.askyesno("Cerrar sesión", "¿Desea cerrar la sesión?"):
            self.usuario = None
            self.actualizar_menu()

    def actualizar_menu(self):
        if self.usuario:
            self.saludo.config(text=f"Hola, {self.usuario.nombre}")
            self.saludo.place(x=1000, y=12)
            self.boton_sesion.config(text="Salir")
        else:
            self.saludo.place_forget()
            self.boton_sesion.config(text="Ingresar")
        # el botón de administración solo lo ven los administradores
        if self.usuario and self.usuario.es_admin:
            self.boton_admin.place(x=790, y=10)
        else:
            self.boton_admin.place_forget()

    # --- ventanas ---
    def abrir_cartelera(self):
        VentanaCartelera(self.ventana, self)

    def abrir_mis_reservas(self):
        self.pedir_usuario(lambda: VentanaMisReservas(self.ventana, self.usuario))

    def iniciar(self):
        self.ventana.mainloop()  # un solo mainloop para todo el programa


if __name__ == "__main__":
    App().iniciar()
