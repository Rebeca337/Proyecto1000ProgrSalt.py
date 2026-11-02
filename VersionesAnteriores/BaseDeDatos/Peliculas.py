from tkinter  import ttk
from tkinter  import  *
import  sqlite3

class Pelicula:
    # propiedad del directorio de conexión
    db_name= "BaseDeDatosPelicula.db"

    def __init__ ( self , ventanaP):
        # Inicializaciones
        self.ventanaP=ventanaP
        self.ventanaP.title("Peliculas")
        self.ventanaP.resizable(False,False)
        self.ventanaP.config(bg="black")

        # Crear un contenedor de marcos
        frame=LabelFrame(self.ventanaP,text="**************Peliculas**************")
        frame.grid(row=0,column=0,columnspan=3,pady=20)

        #Entrada de nombre
        Label(frame,text="Nombre:").grid(row=1,column=0)
        self.nombre=Entry(frame)
        self.nombre.focus()
        self.nombre.grid(row=1,column=1)

        #Entrada de sinopsis
        Label(frame,text="Sinopsis:").grid(row=2,column=0)
        self.sinopsis=Entry(frame)
        self.sinopsis.focus()
        self.sinopsis.grid(row=2,column=1)

        Label(frame,text="Clasificacion:").grid(row=3,column=0)
        self.clasificacion=Entry(frame)
        self.clasificacion.focus()
        self.clasificacion.grid(row=3,column=1)

        Label(frame,text="Genero:").grid(row=4,column=0)
        self.genero=Entry(frame)
        self.genero.focus()
        self.genero.grid(row=4,column=1)

        Label(frame,text="Duracion:").grid(row=5,column=0)
        self.duracion=Entry(frame)
        self.duracion.focus()
        self.duracion.grid(row=5,column=1)

        Label(frame,text="Director:").grid(row=6,column=0)
        self.director=Entry(frame)
        self.director.focus()
        self.director.grid(row=6,column=1)

        Label(frame,text="Actores:").grid(row=7,column=0)
        self.actores=Entry(frame)
        self.actores.focus()
        self.actores.grid(row=7,column=1)

        #Boton de agregar Pelicula
        ttk.Button(frame,text="Guardar Pelicula",command=self.AgregarPelicula).grid(row=8,columnspan=2,sticky= W + E)
        
        #mensajes de salida
        self.message=Label(text='',fg="red")
        self.message.grid(row=3,column=0,columnspan=2,sticky=W + E)


        #Tabla
        self.tree=ttk.Treeview(height=10,columns=("Nombre","Sinopsis","Clasificacion","Genero","Duracion","Director","Actores"))
        self.tree.grid(row=10,column=0,columnspan=2)
        self.tree.heading("#0Nombre",text="Nombre",anchor=CENTER)
        self.tree.heading("#1Sinopsis",text="Sinopsis",anchor=CENTER)
        self.tree.heading("#2Clasificacion",text="Clasificacion",anchor=CENTER)
        self.tree.heading("#3Genero",text="Genero",anchor=CENTER)
        self.tree.heading("#4Duracion",text="Duracion",anchor=CENTER)
        self.tree.heading("#5Director",text="Director",anchor=CENTER)
        self.tree.heading("#6Actores",text="Actores",anchor=CENTER)
        #Botones
        ttk .Button ( text=  "ELIMINAR", command=  self.EliminarPelicula).grid(row= 5 , column=0 , sticky=  W  +  E )
        ttk .Button ( text=  "EDITAR" , command=  self.EditarPelicula ).grid(row= 5 , column=1 , sticky=  W  +  E )
        
        self.ObtenerPelicula()
        #ejecuta la base de datos
    def EjecutarConsulta(self,consulta,parametros =()):
        with sqlite3.connect(self.db_name) as conexion: #Es más para determinar la configuración local que tendrá un bloque de código, lo que se conoce como "contexto".recuperar los valores anteriores. Un ejemplo sería la apertura de un fichero en este caso seria la base de datos
            cursor=conexion.cursor()                    
            resultado=cursor.execute(consulta,parametros)
            conexion.commit()
        return resultado
    
    def ObtenerPelicula(self):
        #Limpiar Tabla
        registro= self.tree.get_children()
        for elemento in registro:
            self.tree.delete(elemento)
        #Consultar datos
        consulta="SELECT * FROM pelicula"
        db_rows=self.EjecutarConsulta(consulta)
        #Rellenar datos
        for row in db_rows:
           self.tree.insert('',0,text=row[1],values=(row[2],row[3], row[4], row[5],row[6], row[7]))

    def validacion(self):
        return len(self.nombre.get())!= 0 and len(self.sinopsis.get())!= 0 and len(self.clasificacion.get())!= 0 and len(self.genero.get())!= 0 and len(self.duracion.get())!= 0 and len(self.director.get())!= 0 and len(self.actores.get())!= 0

    def AgregarPelicula(self):
        if self.validacion():
            consulta="INSERT INTO pelicula VALUES(NULL,?,?,?,?,?,?,?)"
            parametros=(self.nombre.get(), self.sinopsis.get(), self.clasificacion.get(), self.genero.get(), self.duracion.get(), self.director.get(), self.actores.get())
            self.EjecutarConsulta(consulta,parametros)
            self.message["text"]="Pelicula {} Agregada Con Exito".format(self.nombre.get())
            self.nombre.delete(0,END)
            self.sinopsis.delete(0,END)
            self.clasificacion.delete(0,END)
            self.genero.delete(0,END)
            self.duracion.delete(0,END)
            self.director.delete(0,END)
            self.actores.delete(0,END)

        else:
            self.message["text"]="Por Favor Ingrese Los Datos"
        self.ObtenerPelicula()

    def  EliminarPelicula (self):
        self.message["text"]= ''
        try:
            self.tree.item(self.tree.selection())["text"][0]
        except IndexError as e:
            self.message["text"]="Seleccione Un Registro"
            return
        self.message["text"]= ''
        nombre=self.tree.item(self.tree.selection())["text"]
        consulta="DELETE FROM pelicula WHERE nombre = ?"
        self.EjecutarConsulta(consulta,(nombre,))
        self.message["text"]="Registro {} Eliminado Con Exito".format(nombre)
        self.ObtenerPelicula()

    def EditarPelicula(self):
        self.message["text"]= ''
        try:
            self.tree.item(self.tree.selection())["values"][0]
        except IndexError as e:
            self.message["text"]=" Por Favor Seleccione Un Registro"
            return
        nombre=self.tree.item(self.tree.selection())["text"]
        sinopsis=self.tree.item(self.tree.selection())["values"][0]
        clasificacion=self.tree.item(self.tree.selection())["values"][1]
        genero=self.tree.item(self.tree.selection())["values"][2]
        duracion=self.tree.item(self.tree.selection())["values"][3]
        director=self.tree.item(self.tree.selection())["values"][4]
        actores=self.tree.item(self.tree.selection())["values"][5]
        self.Edit_Ventana=Toplevel()
        self.Edit_Ventana.title="Editar Pelicula"
        #self.Edit_Ventana.resizable(False,False)
       
        # nombre de pelicula
        Label(self.Edit_Ventana, text = "Nombre Actual:").grid(row = 0, column = 1)
        Entry(self.Edit_Ventana, textvariable = StringVar(self.Edit_Ventana, value = nombre), state = "readonly").grid(row = 0, column = 2)
        # nuevo nombre de pelicula
        Label(self.Edit_Ventana, text = "Nuevo Nombre:").grid(row = 1, column = 1)
        nuevo_nombre = Entry(self.Edit_Ventana)
        nuevo_nombre.grid(row = 1, column = 2)
        # sinopsis 
        Label(self.Edit_Ventana, text = "Sinopsis Actual:").grid(row = 2, column = 1)
        Entry(self.Edit_Ventana, textvariable = StringVar(self.Edit_Ventana, value = sinopsis), state = 'readonly').grid(row = 2, column = 2)
        #  nueva sinopsis
        Label(self.Edit_Ventana, text = "Nueva Sinopsis:").grid(row = 3, column = 1)
        sinopsis_vieja= Entry(self.Edit_Ventana)
        sinopsis_vieja.grid(row = 3, column = 2)
        #clasificacion
        Label(self.Edit_Ventana, text = "Clasificacion Actual:").grid(row = 4, column = 1)
        Entry(self.Edit_Ventana, textvariable = StringVar(self.Edit_Ventana, value = clasificacion), state = 'readonly').grid(row = 4, column = 2)
        #  nueva clasificacion
        Label(self.Edit_Ventana, text = "Nueva Clasificacion:").grid(row = 5, column = 1)
        clasificacion_vieja= Entry(self.Edit_Ventana)
        clasificacion_vieja.grid(row = 5, column = 2)
        #genero
        Label(self.Edit_Ventana, text = "Genero Actual:").grid(row = 6, column = 1)
        Entry(self.Edit_Ventana, textvariable = StringVar(self.Edit_Ventana, value = genero), state = 'readonly').grid(row = 6, column = 2)
        #nuevo genero
        Label(self.Edit_Ventana, text = "Nuevo Genero:").grid(row = 7, column = 1)
        genero_viejo= Entry(self.Edit_Ventana)
        genero_viejo.grid(row = 7, column = 2)
        #duracion
        Label(self.Edit_Ventana, text = "Duracion Actual:").grid(row = 8, column = 1)
        Entry(self.Edit_Ventana, textvariable = StringVar(self.Edit_Ventana, value =duracion), state = 'readonly').grid(row = 8, column = 2)
        #nueva duracion
        Label(self.Edit_Ventana, text = "Nueva Duracion:").grid(row = 9, column = 1)
        duracion_vieja= Entry(self.Edit_Ventana)
        duracion_vieja.grid(row = 9, column = 2)
        #director
        Label(self.Edit_Ventana, text = "Director Actual:").grid(row = 10, column = 1)
        Entry(self.Edit_Ventana, textvariable = StringVar(self.Edit_Ventana, value = director), state = 'readonly').grid(row = 10, column = 2)
        #Nuevo Director
        Label(self.Edit_Ventana, text = "Nuevo Director:").grid(row = 11, column = 1)
        director_viejo= Entry(self.Edit_Ventana)
        director_viejo.grid(row = 11, column = 2)
        #actores
        Label(self.Edit_Ventana, text = "Actores Actual:").grid(row = 12, column = 1)
        Entry(self.Edit_Ventana, textvariable = StringVar(self.Edit_Ventana, value = actores), state = 'readonly').grid(row = 12, column = 2)
        #Nuevo actores
        Label(self.Edit_Ventana, text = "Nuevo Actores:").grid(row = 13, column = 1)
        actores_viejo= Entry(self.Edit_Ventana)
        actores_viejo.grid(row = 13, column = 2)

        Button(self.Edit_Ventana,text="Actualizar",command=lambda:self.EditarRegistro(nuevo_nombre.get(),nombre,sinopsis_vieja.get(),sinopsis,clasificacion_vieja.get(),clasificacion,genero_viejo.get(),genero,duracion_vieja.get(),duracion,director_viejo.get(),director,actores_viejo.get(),actores)).grid(row=20,column=2,sticky= W)
        self.Edit_Ventana.mainloop()

    def EditarRegistro(self,nuevo_nombre,nombre,sinopsis_vieja,sinopsis,clasificacion_vieja,clasificacion,genero_viejo,genero,duracion_vieja,duracion,director_viejo,director,actores_viejo,actores):
        consulta="UPDATE pelicula SET nombre = ?,sinopsis = ?,clasificacion=?,genero=?,duracion=?,director=?,actores=? WHERE nombre = ? AND sinopsis = ? AND clasificacion = ? AND genero = ? AND duracion = ? AND director = ? AND actores = ? "
        parametros=(nuevo_nombre,sinopsis_vieja,clasificacion_vieja,genero_viejo,duracion_vieja,director_viejo,actores_viejo,nombre,sinopsis,clasificacion,genero,duracion,director,actores)
        self.EjecutarConsulta(consulta,parametros)
        self.Edit_Ventana.destroy()
        self.message["text"]=" Registro {} Actualizado Con Exito".format(nombre)
        self.ObtenerPelicula()


if __name__== "__main__":
    ventanap=Tk()
    aplicacion=Pelicula(ventanap)
    ventanap.mainloop()