"""
Panel de administración (solo para usuarios administradores).

Las pestañas Películas, Salas y Productos usan la misma clase TablaABM
(Alta, Baja y Modificación), así no repetimos el mismo código tres veces.
"""
import sqlite3
import tkinter as tk
from tkinter import messagebox as mb
from tkinter import ttk

from BaseDeDatos.conexion import consultar, ejecutar
from Clases_Metodos.Descuento import DIAS
from Clases_Metodos.Sala import Sala
from Ventanas.comun import GRIS, a_texto_fecha, centrar


class TablaABM(tk.Frame):
    """
    campos: lista de (columna, título, tipo) donde tipo es "texto", "entero" o "decimal".
    opciones: {columna: función que devuelve [(valor, texto), ...]} para mostrar una lista desplegable.
    validar: función que recibe los datos y devuelve un texto de error o None.
    """

    def __init__(self, master, tabla, campos, opciones=None, validar=None):
        super().__init__(master)
        self.tabla_db = tabla
        self.campos = campos
        self.opciones = opciones or {}
        self.validar = validar
        self.id_elegido = None

        formulario = tk.Frame(self)
        formulario.pack(side="left", fill="y", padx=10, pady=10)
        self.entradas = {}
        for i, (columna, titulo, tipo) in enumerate(campos):
            tk.Label(formulario, text=titulo + ":").grid(row=i, column=0, sticky="e", pady=3)
            if columna in self.opciones:
                entrada = ttk.Combobox(formulario, state="readonly", width=25,
                                       postcommand=lambda c=columna: self.actualizar_opciones(c))
            else:
                entrada = tk.Entry(formulario, width=28)
            entrada.grid(row=i, column=1, pady=3)
            self.entradas[columna] = entrada

        botones = tk.Frame(formulario)
        botones.grid(row=len(campos), column=0, columnspan=2, pady=10)
        tk.Button(botones, text="Agregar", bg=GRIS, width=10, command=self.agregar).grid(row=0, column=0, padx=2, pady=2)
        tk.Button(botones, text="Guardar cambios", bg=GRIS, width=14, command=self.modificar).grid(row=0, column=1, padx=2, pady=2)
        tk.Button(botones, text="Eliminar", bg=GRIS, width=10, command=self.eliminar).grid(row=1, column=0, padx=2, pady=2)
        tk.Button(botones, text="Limpiar", bg=GRIS, width=14, command=self.limpiar).grid(row=1, column=1, padx=2, pady=2)

        titulos = [titulo for _, titulo, _ in campos]
        self.tabla = ttk.Treeview(self, columns=titulos, show="headings", height=16)
        for titulo in titulos:
            self.tabla.heading(titulo, text=titulo)
            self.tabla.column(titulo, width=95, anchor="center")
        self.tabla.pack(side="left", fill="both", expand=True, padx=(0, 10), pady=10)
        self.tabla.bind("<<TreeviewSelect>>", self.al_seleccionar)
        self.cargar()

    # --- listas desplegables ---
    def actualizar_opciones(self, columna):
        self.entradas[columna]["values"] = [texto for _, texto in self.opciones[columna]()]

    def texto_de_opcion(self, columna, valor):
        for v, texto in self.opciones[columna]():
            if v == valor:
                return texto
        return valor

    def valor_de_opcion(self, columna, texto):
        for v, t in self.opciones[columna]():
            if t == texto:
                return v
        return None

    # --- tabla ---
    def cargar(self):
        self.tabla.delete(*self.tabla.get_children())
        columnas = ", ".join(c for c, _, _ in self.campos)
        for fila in consultar(f"SELECT id, {columnas} FROM {self.tabla_db} ORDER BY id"):
            valores = []
            for columna, _, _ in self.campos:
                valor = fila[columna]
                valores.append(self.texto_de_opcion(columna, valor) if columna in self.opciones else valor)
            self.tabla.insert("", "end", iid=fila["id"], values=valores)

    def al_seleccionar(self, evento=None):
        seleccion = self.tabla.selection()
        if not seleccion:
            return
        self.id_elegido = int(seleccion[0])
        for (columna, _, _), valor in zip(self.campos, self.tabla.item(seleccion[0])["values"]):
            entrada = self.entradas[columna]
            if isinstance(entrada, ttk.Combobox):
                self.actualizar_opciones(columna)
                entrada.set(valor)
            else:
                entrada.delete(0, "end")
                entrada.insert(0, valor)

    def limpiar(self):
        self.id_elegido = None
        self.tabla.selection_remove(self.tabla.selection())
        for entrada in self.entradas.values():
            if isinstance(entrada, ttk.Combobox):
                entrada.set("")
            else:
                entrada.delete(0, "end")

    def leer_formulario(self):
        """Lee y convierte los datos del formulario. Devuelve un diccionario o None si hay errores."""
        datos = {}
        for columna, titulo, tipo in self.campos:
            texto = self.entradas[columna].get().strip()
            if texto == "":
                mb.showerror("Faltan datos", f"Complete el campo '{titulo}'.", parent=self)
                return None
            if columna in self.opciones:
                datos[columna] = self.valor_de_opcion(columna, texto)
                continue
            try:
                if tipo == "entero":
                    texto = int(texto)
                elif tipo == "decimal":
                    texto = float(texto.replace(",", "."))
            except ValueError:
                mb.showerror("Dato inválido", f"'{titulo}' debe ser un número.", parent=self)
                return None
            datos[columna] = texto
        if self.validar:
            error = self.validar(datos)
            if error:
                mb.showerror("Dato inválido", error, parent=self)
                return None
        return datos

    # --- botones ---
    def guardar_en_db(self, sql, parametros):
        try:
            ejecutar(sql, parametros)
        except sqlite3.IntegrityError:
            mb.showerror("No se pudo guardar",
                         "El dato está repetido o lo está usando otro registro "
                         "(por ejemplo, una sala que ya tiene reservas).", parent=self)
            return False
        self.limpiar()
        self.cargar()
        return True

    def agregar(self):
        datos = self.leer_formulario()
        if datos:
            columnas = ", ".join(datos)
            signos = ", ".join("?" for _ in datos)
            self.guardar_en_db(f"INSERT INTO {self.tabla_db} ({columnas}) VALUES ({signos})", list(datos.values()))

    def modificar(self):
        if self.id_elegido is None:
            mb.showwarning("Modificar", "Seleccione un registro de la tabla.", parent=self)
            return
        datos = self.leer_formulario()
        if datos:
            cambios = ", ".join(f"{c} = ?" for c in datos)
            self.guardar_en_db(f"UPDATE {self.tabla_db} SET {cambios} WHERE id = ?",
                               list(datos.values()) + [self.id_elegido])

    def eliminar(self):
        if self.id_elegido is None:
            mb.showwarning("Eliminar", "Seleccione un registro de la tabla.", parent=self)
            return
        if mb.askyesno("Eliminar", "¿Seguro que quiere eliminar el registro seleccionado?", parent=self):
            self.guardar_en_db(f"DELETE FROM {self.tabla_db} WHERE id = ?", (self.id_elegido,))


class PestaniaDescuentos(tk.Frame):
    """Permite cambiar el porcentaje de descuento de cada día."""

    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, text="Descuento para clientes con tarjeta (%)", font=("Arial", 13, "bold")).grid(
            row=0, column=0, columnspan=2, pady=15, padx=20)
        self.valores = []
        porcentajes = {f["dia"]: f["porcentaje"] for f in consultar("SELECT * FROM descuentos")}
        for dia, nombre in enumerate(DIAS):
            tk.Label(self, text=nombre + ":").grid(row=dia + 1, column=0, sticky="e", padx=10, pady=3)
            valor = tk.IntVar(value=int(porcentajes.get(dia, 0)))
            tk.Spinbox(self, from_=0, to=100, textvariable=valor, width=6).grid(row=dia + 1, column=1, sticky="w")
            self.valores.append(valor)
        tk.Button(self, text="Guardar descuentos", bg=GRIS, command=self.guardar).grid(row=9, column=0, columnspan=2, pady=15)

    def guardar(self):
        try:
            nuevos = [v.get() for v in self.valores]
        except tk.TclError:
            mb.showerror("Descuentos", "Los descuentos deben ser números enteros.", parent=self)
            return
        if any(not 0 <= n <= 100 for n in nuevos):
            mb.showerror("Descuentos", "Los descuentos deben estar entre 0 y 100.", parent=self)
            return
        for dia, porcentaje in enumerate(nuevos):
            ejecutar("INSERT OR REPLACE INTO descuentos (dia, porcentaje) VALUES (?, ?)", (dia, porcentaje))
        mb.showinfo("Descuentos", "Descuentos guardados.", parent=self)


class PestaniaReservas(tk.Frame):
    """Ver las reservas de todos los clientes, o filtrar por un cliente."""

    def __init__(self, master):
        super().__init__(master)
        arriba = tk.Frame(self)
        arriba.pack(pady=10)
        tk.Label(arriba, text="Buscar cliente (nombre, apellido o correo):").pack(side="left")
        self.buscar = tk.Entry(arriba, width=30)
        self.buscar.pack(side="left", padx=5)
        self.buscar.bind("<Return>", lambda e: self.cargar())
        tk.Button(arriba, text="Buscar", bg=GRIS, command=self.cargar).pack(side="left")
        tk.Button(arriba, text="Ver todas", bg=GRIS, command=self.ver_todas).pack(side="left", padx=5)

        columnas = ["Cliente", "Correo", "Película", "Sala", "Fecha", "Butaca", "Pagado"]
        self.tabla = ttk.Treeview(self, columns=columnas, show="headings", height=15)
        for c in columnas:
            self.tabla.heading(c, text=c)
            self.tabla.column(c, width=115, anchor="center")
        self.tabla.pack(fill="both", expand=True, padx=10)
        self.total = tk.Label(self)
        self.total.pack(pady=5)
        self.cargar()

    def ver_todas(self):
        self.buscar.delete(0, "end")
        self.cargar()

    def cargar(self):
        self.tabla.delete(*self.tabla.get_children())
        texto = f"%{self.buscar.get().strip()}%"
        filas = consultar(
            "SELECT u.nombre || ' ' || u.apellido AS cliente, u.correo, p.nombre AS pelicula, s.numero, "
            "r.fecha, s.horario, r.butaca, r.precio FROM reservas r "
            "JOIN usuarios u ON u.id = r.usuario_id JOIN salas s ON s.id = r.sala_id "
            "JOIN peliculas p ON p.id = s.pelicula_id "
            "WHERE u.nombre LIKE ? OR u.apellido LIKE ? OR u.correo LIKE ? ORDER BY r.fecha DESC",
            (texto, texto, texto))
        for f in filas:
            self.tabla.insert("", "end", values=(f["cliente"], f["correo"], f["pelicula"], f["numero"],
                                                 f"{a_texto_fecha(f['fecha'])} {f['horario']}", f["butaca"],
                                                 f"${f['precio']:,.2f}"))
        self.total.config(text=f"{len(filas)} entrada(s) - Total: ${sum(f['precio'] for f in filas):,.2f}")


def lista_peliculas():
    return [(f["id"], f"{f['id']} - {f['nombre']}") for f in consultar("SELECT id, nombre FROM peliculas ORDER BY nombre")]


class VentanaAdmin(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Administración - Cinemar")
        centrar(self, 1050, 520)
        pestanias = ttk.Notebook(self)
        pestanias.pack(fill="both", expand=True)

        peliculas = TablaABM(pestanias, "peliculas", [
            ("nombre", "Nombre", "texto"), ("sinopsis", "Sinopsis", "texto"),
            ("clasificacion", "Clasificación", "texto"), ("genero", "Género", "texto"),
            ("duracion", "Duración (min)", "entero"), ("director", "Director", "texto"),
            ("actores", "Actores", "texto")])
        salas = TablaABM(pestanias, "salas", [
            ("numero", "N° de sala", "entero"), ("pelicula_id", "Película", "entero"),
            ("tipo", "Tipo", "texto"), ("precio", "Precio", "decimal"),
            ("filas", "Filas", "entero"), ("butacas_por_fila", "Butacas por fila", "entero"),
            ("horario", "Horario (HH:MM)", "texto")],
            opciones={"pelicula_id": lista_peliculas, "tipo": lambda: [("2D", "2D"), ("3D", "3D")]},
            validar=Sala.validar_datos)
        productos = TablaABM(pestanias, "productos", [
            ("nombre", "Nombre", "texto"), ("precio", "Precio", "decimal")])

        pestanias.add(PestaniaReservas(pestanias), text="Reservas")
        pestanias.add(salas, text="Salas")
        pestanias.add(peliculas, text="Películas")
        pestanias.add(productos, text="Productos")
        pestanias.add(PestaniaDescuentos(pestanias), text="Descuentos")
        # al volver a la pestaña Salas, se actualiza por si cambió el nombre de una película
        pestanias.bind("<<NotebookTabChanged>>", lambda e: salas.cargar())
