"""Funciones que usan todas las ventanas."""
import os
import tkinter as tk
from datetime import date, timedelta

from Clases_Metodos.Descuento import DIAS

CARPETA_IMAGENES = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Imagenes")
ROJO = "#f50743"
GRIS = "#ABB2B9"


def centrar(ventana, ancho, alto):
    """Abre la ventana siempre en el centro de la pantalla."""
    x = (ventana.winfo_screenwidth() - ancho) // 2
    y = (ventana.winfo_screenheight() - alto) // 2
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")


def cargar_imagen(nombre_archivo):
    """Carga una imagen de la carpeta Imagenes. Si no está, devuelve None (y el programa sigue)."""
    try:
        return tk.PhotoImage(file=os.path.join(CARPETA_IMAGENES, nombre_archivo))
    except tk.TclError:
        return None


def poner_fondo(ventana, nombre_archivo):
    imagen = cargar_imagen(nombre_archivo)
    if imagen:
        fondo = tk.Label(ventana, image=imagen, bd=0)
        fondo.image = imagen  # guardamos la imagen para que Python no la borre
        fondo.place(x=0, y=0, relwidth=1, relheight=1)


def proximos_dias(cantidad=7):
    """Devuelve [(texto, fecha), ...] para los próximos días. Ej: ("Lunes 02/11", date)."""
    hoy = date.today()
    return [(f"{DIAS[d.weekday()]} {d:%d/%m}", d) for d in (hoy + timedelta(days=i) for i in range(cantidad))]


def a_texto_fecha(fecha_iso):
    """'2026-11-02' -> '02/11/2026'"""
    anio, mes, dia = fecha_iso.split("-")
    return f"{dia}/{mes}/{anio}"
