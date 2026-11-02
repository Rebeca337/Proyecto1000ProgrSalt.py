"""Ventana Candy: muestra los productos y sus precios."""
import tkinter as tk
from tkinter import ttk

from BaseDeDatos.conexion import consultar
from Ventanas.comun import ROJO, centrar, poner_fondo


class VentanaCandy(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Candy")
        self.resizable(False, False)
        centrar(self, 850, 550)
        poner_fondo(self, "proyectoCANDY2.png")

        caja = tk.Frame(self, bg="white")
        caja.place(relx=0.5, rely=0.5, anchor="center", width=420, height=330)
        tk.Label(caja, text="Candy", font=("Arial", 22, "bold"), fg=ROJO, bg="white").pack(pady=10)
        tabla = ttk.Treeview(caja, columns=("Producto", "Precio"), show="headings", height=10)
        tabla.heading("Producto", text="Producto")
        tabla.heading("Precio", text="Precio")
        tabla.column("Producto", width=250)
        tabla.column("Precio", width=100, anchor="center")
        tabla.pack()
        for fila in consultar("SELECT nombre, precio FROM productos ORDER BY nombre"):
            tabla.insert("", "end", values=(fila["nombre"], f"${fila['precio']:,.2f}"))
