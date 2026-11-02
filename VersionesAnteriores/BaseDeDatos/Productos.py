from tkinter  import ttk
from tkinter  import  *
import  sqlite3

class Producto:
    # propiedad del directorio de conexión
    db_name= "BaseDeDatos.db"

    def __init__ ( self , ventana ):
        # Inicializaciones
        self.ventana=ventana
        self.ventana.title("Productos")
        self.ventana.resizable(False,False)
        self.ventana.config(bg="blue")
        # Crear un contenedor de marco
        frame=LabelFrame(self.ventana,text="*****Registrar Nuevo Producto*****")
        frame.grid(row=0,column=0,columnspan=3,pady=20)

        #Entrada de nombre
        Label(frame,text="Nombre:").grid(row=1,column=0)
        self.nombre=Entry(frame)
        self.nombre.focus()
        self.nombre.grid(row=1,column=1)

        #Entrada de precio
        Label(frame,text="Precio:").grid(row=2,column=0)
        self.precio=Entry(frame)
        #self.precio.focus()
        self.precio.grid(row=2,column=1)

        #Boton de agregar Producto
        ttk.Button(frame,text="Guardar Producto",command=self.AgregarProducto).grid(row=3,columnspan=2,sticky= W + E)
        
        #mensajes de salida
        self.message=Label(text='',fg="red")
        self.message.grid(row=3,column=0,columnspan=2,sticky=W + E)


        #Tabla
        self.tree=ttk.Treeview(height=10,columns=2)
        self.tree.grid(row=4,column=0,columnspan=2)
        self.tree.heading("#0",text="Nombre",anchor=CENTER)
        self.tree.heading("#1",text="Precio",anchor=CENTER)
        

        #Botones
        ttk .Button ( text=  "ELIMINAR" , command=  self.EliminarProducto).grid(row= 5 , column=0 , sticky=  W  +  E )
        ttk .Button ( text=  "EDITAR" , command=  self.EditarProducto ).grid(row= 5 , column=1 , sticky=  W  +  E )

        self.ObtenerProducto()
        #ejecuta la base de datos la conexion
    def EjecutarConsulta(self,consulta,parametros =()):
        with sqlite3.connect(self.db_name) as conexion: #Es más para determinar la configuración local que tendrá un bloque de código, lo que se conoce como "contexto".recuperar los valores anteriores. Un ejemplo sería la apertura de un fichero en este caso seria la base de datos
            cursor=conexion.cursor()
            resultado=cursor.execute(consulta,parametros)
            conexion.commit()
        return resultado
    
    def ObtenerProducto(self):
        #Limpiar Tabla
        registro= self.tree.get_children()
        for elemento in registro:
            self.tree.delete(elemento)
        #Consultar datos
        consulta="SELECT * FROM productos ORDER BY nombre DESC"
        db_rows=self.EjecutarConsulta(consulta)
        #Rellenar datos
        for row in db_rows:
           self.tree.insert('',0,text=row[1],values=row[2])
    #validamos datos
    def validacion(self):
        return len(self.nombre.get())!= 0 and len(self.precio.get())!= 0
    #agregamos los productos 
    def AgregarProducto(self):
        if self.validacion():
            consulta="INSERT INTO productos VALUES(NULL,?,?)"
            parametros=(self.nombre.get(), self.precio.get())
            self.EjecutarConsulta(consulta,parametros)
            self.message["text"]="productos {} Agregado Con Exito".format(self.nombre.get())
            self.nombre.delete(0,END)
            self.precio.delete(0,END)
        else:
            self.message["text"]="Nombre Y Precio Son Requeridos"
        self.ObtenerProducto()
    #eliminamos los productos de la base de datos 
    def  EliminarProducto (self):
        self.message["text"]= ''
        try:
            self.tree.item(self.tree.selection())["text"][0]
        except IndexError as e:
            self.message["text"]="Seleccione Un Registro"
            return
        self.message["text"]= ''
        nombre=self.tree.item(self.tree.selection())["text"]
        consulta="DELETE FROM productos WHERE nombre = ?"
        self.EjecutarConsulta(consulta,(nombre,))
        self.message["text"]="Registro {} Eliminado Con Exito".format(nombre)
        self.ObtenerProducto()
    #editamos los productos 
    def EditarProducto(self):
        self.message["text"]= ''
        try:
            self.tree.item(self.tree.selection())["values"][0]
        except IndexError as e:
            self.message["text"]=" Por Favor Seleccione Un Registro"
            return
        nombre=self.tree.item(self.tree.selection())["text"]
        precio_viejo=self.tree.item(self.tree.selection())["values"][0]
        self.Edit_Ventana=Toplevel()
        self.Edit_Ventana.title="Editar Producto"
        self.Edit_Ventana.resizable(False,False)
        
       
        # nombre actual
        Label(self.Edit_Ventana, text = "Nombre Actual:").grid(row = 0, column = 1)
        Entry(self.Edit_Ventana, textvariable = StringVar(self.Edit_Ventana, value = nombre), state = "readonly").grid(row = 0, column = 2)
       
        # nuevo nombre
        Label(self.Edit_Ventana, text = "Nuevo Nombre:").grid(row = 1, column = 1)
        nuevo_nombre = Entry(self.Edit_Ventana)
        nuevo_nombre.grid(row = 1, column = 2)

        # precio actual 
        Label(self.Edit_Ventana, text = "Precio Actual:").grid(row = 2, column = 1)
        Entry(self.Edit_Ventana, textvariable = StringVar(self.Edit_Ventana, value = precio_viejo), state = 'readonly').grid(row = 2, column = 2)
        # nuevo precio
        Label(self.Edit_Ventana, text = "Precio Nuevo:").grid(row = 3, column = 1)
        nuevo_precio= Entry(self.Edit_Ventana)
        nuevo_precio.grid(row = 3, column = 2)
       
        Button(self.Edit_Ventana,text="Actualizar",command=lambda:self.EditarRegistro(nuevo_nombre.get(),nombre,nuevo_precio.get(),precio_viejo)).grid(row=4,column=2,sticky= W)
        self.Edit_Ventana.mainloop()
    #por medio de la base de datos editamos el registro
    def EditarRegistro(self,nuevo_nombre,nombre,nuevo_precio,precio_viejo):
        consulta="UPDATE productos SET nombre = ?,precio = ? WHERE nombre = ? AND precio = ? "
        parametros=(nuevo_nombre,nuevo_precio,nombre,precio_viejo)
        self.EjecutarConsulta(consulta,parametros)
        self.Edit_Ventana.destroy()
        self.message["text"]=" Registro {} Actualizado Con Exito".format(nombre)
        self.ObtenerProducto()


if __name__== "__main__":
    ventana=Tk()
    aplicacion=Producto(ventana)
    ventana.mainloop()