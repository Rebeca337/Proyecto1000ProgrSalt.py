"""Cartelera (ver salas), reserva de butacas y "Mis reservas"."""
import sqlite3
import tkinter as tk
from datetime import datetime
from tkinter import messagebox as mb
from tkinter import ttk

from BaseDeDatos.conexion import consultar
from Clases_Metodos.Comprobante import Comprobante
from Clases_Metodos.Descuento import Descuento, precio_final
from Clases_Metodos.Peliculas import Pelicula
from Clases_Metodos.Reserva import Reserva
from Clases_Metodos.Sala import Sala
from Ventanas.comun import GRIS, ROJO, a_texto_fecha, centrar, proximos_dias


def crear_tabla(contenedor, columnas, alto=10):
    """Crea una tabla (Treeview) con las columnas indicadas: [(titulo, ancho), ...]."""
    tabla = ttk.Treeview(contenedor, columns=[c[0] for c in columnas], show="headings", height=alto)
    for titulo, ancho in columnas:
        tabla.heading(titulo, text=titulo)
        tabla.column(titulo, width=ancho, anchor="center")
    return tabla


class VentanaCartelera(tk.Toplevel):
    """Lista de salas con su película. Cualquiera la puede ver; para reservar hay que iniciar sesión."""

    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        self.title("Cartelera")
        self.resizable(False, False)
        centrar(self, 900, 480)

        tk.Label(self, text="Cartelera - funciones todos los días", font=("Arial", 18, "bold"), fg=ROJO).pack(pady=10)
        self.tabla = crear_tabla(self, [("Sala", 60), ("Película", 230), ("Tipo", 60), ("Horario", 80),
                                        ("Precio", 90), ("Clasificación", 100), ("Duración", 90)])
        self.tabla.pack(padx=15)
        self.tabla.bind("<<TreeviewSelect>>", self.mostrar_detalle)

        self.detalle = tk.Label(self, text="Seleccione una función para ver los detalles.",
                                justify="left", wraplength=850, font=("Arial", 10))
        self.detalle.pack(pady=10, padx=15, anchor="w")
        tk.Button(self, text="Reservar butacas", bg=GRIS, width=25, command=self.reservar).pack(pady=5)
        self.cargar()

    def cargar(self):
        self.tabla.delete(*self.tabla.get_children())
        filas = consultar("SELECT s.id, s.numero, p.nombre, s.tipo, s.horario, s.precio, p.clasificacion, p.duracion "
                          "FROM salas s JOIN peliculas p ON p.id = s.pelicula_id ORDER BY s.horario")
        for f in filas:
            # iid = id de la sala, así sabemos cuál se eligió
            self.tabla.insert("", "end", iid=f["id"], values=(f["numero"], f["nombre"], f["tipo"], f["horario"],
                                                              f"${f['precio']:,.0f}", f["clasificacion"],
                                                              f"{f['duracion']} min"))

    def sala_elegida(self):
        seleccion = self.tabla.selection()
        return Sala.buscar(int(seleccion[0])) if seleccion else None

    def mostrar_detalle(self, evento=None):
        sala = self.sala_elegida()
        if sala:
            self.detalle.config(text=Pelicula.buscar(sala.id_pelicula).ficha())

    def reservar(self):
        sala = self.sala_elegida()
        if sala is None:
            mb.showwarning("Cartelera", "Seleccione una función de la lista.", parent=self)
            return
        # si no inició sesión, primero se abre el login
        self.app.pedir_usuario(lambda: VentanaButacas(self, self.app.usuario, sala))


class VentanaButacas(tk.Toplevel):
    """Mapa de butacas. Sirve para reservar nuevas o para modificar una reserva (si se pasa 'reserva')."""
    LIBRE, OCUPADA, ELEGIDA, ACTUAL = "#2ecc71", "#e74c3c", "#f1c40f", "#3498db"

    def __init__(self, master, usuario, sala, reserva=None, al_terminar=None):
        super().__init__(master)
        self.usuario = usuario
        self.sala = sala
        self.reserva = reserva            # None = reserva nueva
        self.al_terminar = al_terminar
        self.elegidas = []
        self.pelicula = Pelicula.buscar(sala.id_pelicula)
        self.title("Modificar reserva" if reserva else "Elegir butacas")
        self.resizable(False, False)

        tk.Label(self, text=f"{self.pelicula} - {sala} - {sala.horario} hs",
                 font=("Arial", 16, "bold"), fg=ROJO).pack(pady=(10, 4))

        arriba = tk.Frame(self)
        arriba.pack()
        tk.Label(arriba, text="Fecha:").pack(side="left")
        # solo se ofrecen fechas cuya función todavía no empezó
        self.dias = [(t, d) for t, d in proximos_dias()
                     if datetime.strptime(f"{d} {sala.horario}", "%Y-%m-%d %H:%M") > datetime.now()]
        self.combo_fecha = ttk.Combobox(arriba, values=[t for t, d in self.dias], state="readonly", width=18)
        self.combo_fecha.pack(side="left", padx=5)
        self.combo_fecha.current(0)
        self.combo_fecha.bind("<<ComboboxSelected>>", lambda e: self.dibujar_butacas())

        tk.Label(self, text="PANTALLA", bg="gray20", fg="white", width=40).pack(pady=(12, 6))
        self.mapa = tk.Frame(self)
        self.mapa.pack(padx=20)

        referencias = tk.Frame(self)
        referencias.pack(pady=6)
        lista = [(self.LIBRE, "Libre"), (self.OCUPADA, "Ocupada"), (self.ELEGIDA, "Elegida")]
        if reserva:
            lista.append((self.ACTUAL, "Tu butaca actual"))
        for color, texto in lista:
            tk.Label(referencias, bg=color, width=2).pack(side="left", padx=(10, 3))
            tk.Label(referencias, text=texto).pack(side="left")

        self.info = tk.Label(self, font=("Arial", 11))
        self.info.pack(pady=4)
        tk.Button(self, text="Confirmar", bg=GRIS, width=20, command=self.confirmar).pack(pady=(0, 12))
        self.dibujar_butacas()

    def fecha_elegida(self):
        return self.dias[self.combo_fecha.current()][1]

    def dibujar_butacas(self):
        for widget in self.mapa.winfo_children():
            widget.destroy()
        self.elegidas = []
        fecha = self.fecha_elegida().isoformat()
        for i, fila in enumerate(self.sala.butacas(fecha)):
            tk.Label(self.mapa, text=fila[0].fila, width=2).grid(row=i, column=0)
            for j, butaca in enumerate(fila):
                es_actual = self.reserva and self.reserva.fecha == fecha and self.reserva.butaca == butaca.codigo
                if es_actual:
                    color, estado = self.ACTUAL, "disabled"
                elif butaca.reservada:
                    color, estado = self.OCUPADA, "disabled"
                else:
                    color, estado = self.LIBRE, "normal"
                boton = tk.Button(self.mapa, text=butaca.numero, width=3, bg=color, state=estado,
                                  disabledforeground="white")
                boton.config(command=lambda c=butaca.codigo, b=boton: self.elegir(c, b))
                boton.grid(row=i, column=j + 1, padx=1, pady=1)
        self.actualizar_info()

    def elegir(self, codigo, boton):
        if codigo in self.elegidas:
            self.elegidas.remove(codigo)
            boton.config(bg=self.LIBRE)
            return self.actualizar_info()
        if self.reserva and self.elegidas:
            mb.showinfo("Modificar", "Al modificar se cambia una sola butaca.", parent=self)
            return
        self.elegidas.append(codigo)
        boton.config(bg=self.ELEGIDA)
        self.actualizar_info()

    def precio_entrada(self):
        return precio_final(self.sala.precio, self.fecha_elegida(), self.usuario.tiene_tarjeta)

    def actualizar_info(self):
        fecha = self.fecha_elegida()
        texto = f"Precio por entrada: ${self.precio_entrada():,.2f}"
        if self.usuario.tiene_tarjeta:
            descuento = Descuento.del_dia(fecha)
            texto += f"  (tarjeta: {descuento.porcentaje:g}% los {descuento.nombre_dia.lower()})"
        texto += f"   |   Libres: {self.sala.lugares_libres(fecha.isoformat())} de {self.sala.capacidad}"
        if self.elegidas and not self.reserva:
            texto += f"\nElegidas: {', '.join(self.elegidas)}  -  Total: ${self.precio_entrada() * len(self.elegidas):,.2f}"
        self.info.config(text=texto)

    def confirmar(self):
        if not self.elegidas:
            mb.showwarning("Butacas", "Elija al menos una butaca.", parent=self)
            return
        fecha = self.fecha_elegida()
        try:
            if self.reserva:
                self.reserva.modificar(fecha.isoformat(), self.elegidas[0], self.precio_entrada())
                mb.showinfo("Reserva modificada", f"Ahora tu butaca es la {self.elegidas[0]} "
                                                  f"del {fecha:%d/%m/%Y}.", parent=self)
            else:
                total = self.precio_entrada() * len(self.elegidas)
                if not mb.askyesno("Confirmar pago", f"¿Pagar ${total:,.2f} por {len(self.elegidas)} entrada(s)?",
                                   parent=self):
                    return
                Reserva.reservar(self.usuario.id_usuario, self.sala.id_sala, fecha.isoformat(),
                                 self.elegidas, self.precio_entrada())
                comprobante = Comprobante(self.usuario.nombre_completo(), self.pelicula, self.sala,
                                          f"{fecha:%d/%m/%Y}", self.elegidas, self.precio_entrada())
                mb.showinfo("¡Reserva confirmada!", comprobante.texto(), parent=self)
        except sqlite3.IntegrityError:
            # alguien reservó la misma butaca justo antes
            mb.showerror("Butaca ocupada", "Una de las butacas ya fue reservada. Elija otra.", parent=self)
            return self.dibujar_butacas()
        except ValueError as error:
            mb.showerror("No se puede modificar", str(error), parent=self)
            return
        self.destroy()
        if self.al_terminar:
            self.al_terminar()


class VentanaMisReservas(tk.Toplevel):
    """Reservas del cliente: las próximas y el historial de entradas."""

    def __init__(self, master, usuario):
        super().__init__(master)
        self.usuario = usuario
        self.title("Mis reservas")
        self.resizable(False, False)
        centrar(self, 820, 420)
        tk.Label(self, text=f"Reservas de {usuario.nombre_completo()}", font=("Arial", 18, "bold"), fg=ROJO).pack(pady=10)
        self.tabla = crear_tabla(self, [("Película", 220), ("Sala", 70), ("Fecha", 100), ("Horario", 80),
                                        ("Butaca", 70), ("Pagado", 100), ("Estado", 100)], alto=12)
        self.tabla.pack(padx=15)
        tk.Button(self, text="Modificar reserva seleccionada", bg=GRIS, command=self.modificar).pack(pady=10)
        self.cargar()

    def cargar(self):
        self.tabla.delete(*self.tabla.get_children())
        self.reservas = {}
        filas = consultar("SELECT r.*, s.numero, s.horario, p.nombre AS pelicula FROM reservas r "
                          "JOIN salas s ON s.id = r.sala_id JOIN peliculas p ON p.id = s.pelicula_id "
                          "WHERE r.usuario_id = ? ORDER BY r.fecha DESC, s.horario DESC", (self.usuario.id_usuario,))
        for f in filas:
            reserva = Reserva(f["id"], f["usuario_id"], f["sala_id"], f["fecha"], f["butaca"], f["precio"], f["horario"])
            self.reservas[str(f["id"])] = reserva
            estado = "Próxima" if reserva.se_puede_modificar() else "Ya fue"
            self.tabla.insert("", "end", iid=f["id"], values=(f["pelicula"], f["numero"], a_texto_fecha(f["fecha"]),
                                                              f["horario"], f["butaca"], f"${f['precio']:,.2f}", estado))

    def modificar(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            mb.showwarning("Mis reservas", "Seleccione una reserva.", parent=self)
            return
        reserva = self.reservas[seleccion[0]]
        if not reserva.se_puede_modificar():
            mb.showerror("Mis reservas", "Solo se pueden modificar reservas de funciones que no empezaron.", parent=self)
            return
        VentanaButacas(self, self.usuario, Sala.buscar(reserva.id_sala), reserva=reserva, al_terminar=self.cargar)
