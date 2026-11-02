from tkinter import *
import tkinter as Tk
import tkinter as ttk
import sqlite3
from tkinter import messagebox as mb
from tkinter.ttk import Treeview
#Creamos la ventana Principal 
ventana_principal=Tk()
ventana_principal.geometry("700x900")
ventana_principal.title("C  I  N  E  M  A  R")
ventana_principal.resizable(False,False)

#variable para conexion de base de datos
db=sqlite3.connect('BaseDeDatosLogin.db')
c=db.cursor()

 #Ventan Inicio De Sesion
def ventana1():
    global ventana1

    ventana1=Toplevel(ventana_principal)
    ventana1.title("Inicio Sesion")
    ventana1.geometry("1100x600")
    ventana1.resizable(False,False)

    #cargamos la imagen 
    img = PhotoImage(file="ProyectoCinemar/imagenes/proyecto01-1.png")
    Label(ventana1, image=img).pack()
    #creamos 1 frame en blanco para cargar los siguientes datos
    ventana1_registro=Frame(ventana1,bg="white")
    ventana1_registro.place(x=350,y=150,height=330,width=370)
    Label(ventana1_registro,text="Iniciar Sesion",font=("Arial",30,"bold"),fg="#f50743",bg="white").place(x=70,y=30)
    #nombre de usuario y el entry
    Label(ventana1_registro,text="Nombre de Usuario",font=("Arial",13,"bold"),fg="#f50743",bg="white").place(x=100,y=100)
    NombreUsuario=Entry(ventana1_registro,font=("time new roman",15),bg="lightgray")
    NombreUsuario.place(x=90,y=130,width=250,height=35)
    
    #contraseña y su entry
    Label(ventana1_registro,text="Contraseña",font=("Arial",13,"bold"),fg="#f50743",bg="white").place(x=100,y=170)
    Contrasenia=Entry(ventana1_registro,font=("time new roman",15),bg="lightgray",show="*")
    Contrasenia.place(x=90,y=190,width=250,height=35) 
    #decoramos con un label el recuperar contraseña
    Label(ventana1_registro,text="Recuperar Contraseña",bd=0,font=("time new roman",8,"bold")).place(x=90,y=240)
    #boton de crear cuenta que lleva a la siguiete ventana para el registro
    Button(ventana1_registro,text="Crear Cuenta",command=CrearCuenta,bd=0,font=("time new roman",8,"bold")).place(x=90,y=270)
    #aqui centramos la pantalla para que siempre se abra en el mismo lugar 
    widthtotal = ventana1.winfo_screenwidth()
    heighttotal = ventana1.winfo_screenheight()
    widthventana = 1269
    heightventana = 639
    width = round(widthtotal/2-widthventana/2)
    height = round(heighttotal/2-heightventana/2)
    ventana1.geometry(str(widthventana)+"x"+str(heightventana)+"+"+str(width)+"+"+str(height))
    #creamos la funcion para validar los datos 
    def vali():
        return len (NombreUsuario.get())!=0 and len (Contrasenia.get())!=0
    #creamos la funcion para realizar el login al obtener los datos de la base de datos
    def Login():
        if vali():
            usu=NombreUsuario.get()
            contr=Contrasenia.get()
            c.execute('SELECT * FROM registro WHERE nombre =? AND contrasenia =?',(usu,contr))
            if c.fetchall():
                mb.showinfo(title="Login Correcto",message="Usuario y Contraseña Correctos")
                ventana1.destroy()
            else:
                mb.showerror(title="Login incorrecto",message="Usuario o Contraseña Incorrecto")
    #el boton que lleva al inisio de sesion
    Enviar_btb=Button(ventana1,text="Iniciar Sesion",command=Login,width="20",height="1",bg="#ABB2B9")
    Enviar_btb.place(x=435,y=450)


    ventana1.mainloop()
#una funcion para poder esconder y destruir las ventanas
def ventanas():
    ventana1.iconify() #Permite minimizar la ventana que le indiquemos, esto es útil por ejemplo, para minimizar una ventana padre cuando se abre una ventana hija.
    ventana1.deiconify() #Al contrario de como vimos en 'iconify' que podíamos minimizar la ventana, con 'deiconify' podemos restaurar la ventana, como paso con 'iconify' veámoslo con unos ejemplo
    CrearCuenta.destroy()
    

# creamos la Ventana De Registro
def CrearCuenta():
    global CrearCuenta
    CrearCuenta=Toplevel()
    CrearCuenta.title("Registro De Usuario")
    CrearCuenta.geometry("1100x600")
    CrearCuenta.resizable(False,False)
    #cargamos la imagen
    img1 = PhotoImage(file="ProyectoCinemar/imagenes/CINE.Proyecto1.png")
    fondo2 = Label(CrearCuenta, image=img1).pack()
    #creamos el labely entry 
    Label(CrearCuenta,text="Nombre",font=("Arial",12,"bold"),fg="#f50743",bg="white").place(x=100,y=80)
    Nombre=Entry(CrearCuenta,font=("time new roman",12),bg="lightgray")
    Nombre.place(x=100,y=110,width=250,height=35)

    Label(CrearCuenta,text="Apellido",font=("Arial",12,"bold"),fg="#f50743",bg="white").place(x=100,y=150)
    Apellido=Entry(CrearCuenta,font=("time new roman",12),bg="lightgray")
    Apellido.place(x=100,y=180,width=250,height=35)

    Label(CrearCuenta,text="Contraseña",font=("Arial",12,"bold"),fg="#f50743",bg="white").place(x=100,y=220)
    Contrasenia=Entry(CrearCuenta,font=("time new roman",12),bg="lightgray",show="*")
    Contrasenia.place(x=100,y=250,width=250,height=35)

    Label(CrearCuenta,text="Repetir Contraseña",font=("Arial",12,"bold"),fg="#f50743",bg="white").place(x=100,y=297)
    Repetir_Contrasenia=Entry(CrearCuenta,font=("time new roman",12),bg="lightgray",show="*")
    Repetir_Contrasenia.place(x=100,y=330,width=250,height=35)

    Label(CrearCuenta,text="Correo",font=("Arial",12,"bold"),fg="#f50743",bg="white").place(x=100,y=370)
    Correo=Entry(CrearCuenta,font=("time new roman",12),bg="lightgray")
    Correo.place(x=100,y=400,width=250,height=35)

    Label(CrearCuenta,text="Fecha De Nacimiento",font=("Arial",12,"bold"),fg="#f50743",bg="white").place(x=100,y=440)
    Fecha_De_Nacimiento=Entry(CrearCuenta,font=("time new roman",12),bg="lightgray")
    Fecha_De_Nacimiento.place(x=100,y=470,width=250,height=35)
    #boton de inicio de sesion que te llevaria a la ventana para seleccionar pelicula y el producto
    Enviar_btb=Button(CrearCuenta,text="Inicio De Sesion",command=ventanas,width="25",height="0",bg="#ABB2B9")
    Enviar_btb.place(x=100,y=540)
    #otra funcion para validar datos al registrar usuario
    def validacion():#validar datos para que no cree una cuenta en blanco
        return len (Nombre.get())!=0 and len (Apellido.get())!=0 and len (Contrasenia.get())!=0 and len(Repetir_Contrasenia.get())!=0 and len(Correo.get())!=0 and len(Fecha_De_Nacimiento.get())!=0
    #funcion para guardar los datos de usuario en la base de datos
    def registro_boton():
        if validacion():
            nombre1=Nombre.get()		
            apellido1=Apellido.get()	
            contra=Contrasenia.get()		
            recontra=Repetir_Contrasenia.get()	
            correo1=Correo.get() 
            fecha=Fecha_De_Nacimiento.get()
            if(contra==recontra):		#Esta condicion nos permite saber si las contraseñas coinciden
			#El siguiente comando es el encargado de insertar los datos obtenidos en el registro
                c.execute("INSERT INTO registro values(NULL,\'"+nombre1+"\',\'"+apellido1+"\',\'"+contra+"\',\'"+recontra+"\',\'"+correo1+"\',\'"+fecha+"\')")
                db.commit()			#Confirmamos los datos
                mb.showinfo(title="Registro Correcto",message="Su registro fue exitoso.")
            else:	#Se ejecutara si las contraseñas no coinciden
                mb.showerror(title="Contraseña Incorrecta",message="Error \nLas contraseñas no coinciden.")	#Mostramos un mensaje
		  
        #aqui borramos los campos para poder registrar nuevamente si deseamos
        Nombre.delete(0,END)
        Apellido.delete(0,END)
        Contrasenia.delete(0,END)
        Repetir_Contrasenia.delete(0,END)
        Correo.delete(0,END)
        Fecha_De_Nacimiento.delete(0,END)
    #boton de registreo que guarda los datos ingresados por el usuario 
    Registro1_btb=Button(CrearCuenta,text="Registro",command=registro_boton,width="25",height="0",bg="#ABB2B9")
    Registro1_btb.place(x=100,y=510)
    #condicion para restaurar la ventana
    if(CrearCuenta):
        ventana1.withdraw() #Este metodo permite ocultar una ventana; la forma que podemos usar para restaurarla es con 'deiconify()' o 'iconify()', o a traves del metodo 'state' que nos puede resultar mas comodo de usar. No se requiere de ningun argumento para funcionar como sucede tanto con 'deiconify' e 'iconify'.

    #centramos la ventana
    widthtotal = CrearCuenta.winfo_screenwidth()
    heighttotal = CrearCuenta.winfo_screenheight()
    widthventana = 1100
    heightventana = 600
    width = round(widthtotal/2-widthventana/2)
    height = round(heighttotal/2-heightventana/2)
    CrearCuenta.geometry(str(widthventana)+"x"+str(heightventana)+"+"+str(width)+"+"+str(height))
    
    CrearCuenta.mainloop()

#Ventana para  butacas y Peliculas    
def Pelicula():
    Pelicula=Toplevel()
    Pelicula.title("Lista De Peliculas")
    Pelicula.geometry("1100x600")
    Pelicula.resizable(False,False)
    Pelicula.config(bg="chartreuse2")

    Label(Pelicula,text="Pelicula",font=("Arial",16,"bold"),fg="black",bg="white").place(x=5,y=5)
    Peli=Entry(Pelicula,font=("time new roman",15),bg="white")
    Peli.place(x=100,y=5,width=250,height=35) 

    Button(Pelicula,text="Pelicula1",font=("bold")).place(x=100,y=50)
    Button(Pelicula,text="Pelicula2",font=("bold")).place(x=100,y=100)
    Button(Pelicula,text="Pelicula3",font=("bold")).place(x=100,y=150)

    Label(Pelicula,text="Butaca",font=("Arial",16,"bold"),fg="black",bg="white").place(x=5,y=232)
    Buta=Entry(Pelicula,font=("time new roman",15),bg="white")
    Buta.place(x=100,y=230,width=250,height=35)

#def CambiarColorBoton(boton):
   # boton.config(bg= "Red")

#def boton(boton):

 #   if G1.config(bg="Red")==G1.config(bg="Green"):
 #      G1eli.config(bg="Gray")
        


    G1=Button(Pelicula,text="G1",bg="Green",font=("time new roman",10,"bold"))
    G1.place(x=100,y=300)

    G2=Button(Pelicula,text="G2",bg="Green",font=("time new roman",10,"bold"))
    G2.place(x=140,y=300)

    G3=Button(Pelicula,text="G3",bg="Green",font=("time new roman",10,"bold"))
    G3.place(x=180,y=300)

    G4=Button(Pelicula,text="G4",bg="Green",font=("time new roman",10,"bold"))
    G4.place(x=220,y=300)

    G5=Button(Pelicula,text="G5",bg="Red",font=("time new roman",10,"bold"))
    G5.place(x=260,y=300)

    G6=Button(Pelicula,text="G6",bg="Green",font=("time new roman",10,"bold"))
    G6.place(x=300,y=300)

    J1=Button(Pelicula,text="J1",bg="Green",font=("time new roman",10,"bold"))
    J1.place(x=100,y=350)

    J2=Button(Pelicula,text="J2",bg="Red",font=("time new roman",10,"bold"))
    J2.place(x=140,y=350)

    J3=Button(Pelicula,text="J3",bg="Green",font=("time new roman",10,"bold"))
    J3.place(x=180,y=350)

    J4=Button(Pelicula,text="J4",bg="Green",font=("time new roman",10,"bold"))
    J4.place(x=220,y=350)

    J5=Button(Pelicula,text="J5",bg="Green",font=("time new roman",10,"bold"))
    J5.place(x=260,y=350)

    J6=Button(Pelicula,text="J6",bg="Red",font=("time new roman",10,"bold"))
    J6.place(x=300,y=350)

    Pelicula.mainloop()
#ventana para el producto
def Candy():
    global Candy
    Candy=Toplevel()
    Candy.title("Seleccione Su Pedido")
    Candy.geometry("850x550")
    Candy.resizable(False,False)
    
    #cargamos la imagen
    img2 = PhotoImage(file="ProyectoCinemar/imagenes/proyectoCANDY2.png")
    Label(Candy, image=img2).pack()
   #centramos la ventana
    widthtotal = Candy.winfo_screenwidth()
    heighttotal = Candy.winfo_screenheight()
    widthventana = 850
    heightventana = 550
    width = round(widthtotal/2-widthventana/2)
    height = round(heighttotal/2-heightventana/2)
    Candy.geometry(str(widthventana)+"x"+str(heightventana)+"+"+str(width)+"+"+str(height))
    
    Candy.mainloop()
#ventana que seria el menu donde de ahi podemos ir a diferente ventanas
def ventana0():
    global ventana0
    ventana0=Toplevel()
    ventana0.title("Bienvenido a Cinemar")
    ventana0.geometry("1269x639")
    ventana0.resizable(False,False)
    

    #Ponemos Imagen de fondo
    fondo=PhotoImage(file="ProyectoCinemar/imagenes/test1.png")
    label=Label(ventana0,image=fondo)
    label.place(x=0,y=0,relheight=1,relwidth=1)

    #imagen de boton
    photo = PhotoImage(file ="ProyectoCinemar/imagenes/logintes.png") #imagen botono
    photoimage = photo.subsample(30,30)

    #botones!!
    Button(ventana0,command=ventana1,image= photoimage,bd=0,font=("time new roman",7,"bold")).place(x=1090,y=9)#icono de crear cuenta
    Button(ventana0,command=Pelicula,text="Peliculas",bd=0,font=("time new roman",8,"bold")).place(x=550,y=10)
    Button(ventana0,command=Candy,text="Candy",bd=0,font=("time new roman",8,"bold")).place(x=650,y=10)
    Label(ventana0,text="Cine Fan",bd=0,font=("time new roman",8,"bold")).place(x=750,y=10)#boton fantasma
    Label(ventana0,text="Regala Cine",bd=0,font=("time new roman",8,"bold")).place(x=850,y=10)#boton fantasma
    if (ventana0):
        ventana_principal.withdraw() #Este metodo permite ocultar una ventana; la forma que podemos usar para restaurarla es con 'deiconify()' o 'iconify()', o a traves del metodo 'state' que nos puede resultar mas comodo de usar. No se requiere de ningun argumento para funcionar como sucede tanto con 'deiconify' e 'iconify'.
    #Con Esto Centramos La Pantalla
    widthtotal = ventana0.winfo_screenwidth()
    heighttotal = ventana0.winfo_screenheight()
    widthventana = 1269
    heightventana = 639
    width = round(widthtotal/2-widthventana/2)
    height = round(heighttotal/2-heightventana/2)
    ventana0.geometry(str(widthventana)+"x"+str(heightventana)+"+"+str(width)+"+"+str(height))

    ventana0.mainloop()
#cargamos imagen del super boton 
fondoboton= PhotoImage(file ="ProyectoCinemar/imagenes/Iron-Man-3TP!1.png") #imagen boton
label=Label(ventana_principal,image=fondoboton)
titulo=Label(text="Bienvenidos A Cinemar Click Para Iniciar!!!",font=("cambria",12),bg="#FFFFFF",fg="Black")
titulo.pack()
#centramos el boton 
widthtotal = ventana_principal.winfo_screenwidth()
heighttotal = ventana_principal.winfo_screenheight()
widthventana = 700
heightventana = 900
width = round(widthtotal/2-widthventana/2)
height = round(heighttotal/2-heightventana/2)
ventana_principal.geometry(str(widthventana)+"x"+str(heightventana)+"+"+str(width)+"+"+str(height))
#al darle click al super boton nos abre la ventana que seria del menu 
boton_principal=Button(ventana_principal,command=ventana0,image=fondoboton,bd=0,font=("time new roman",10,"bold"))#boton fantasma
boton_principal.place(x=1,y=20)
    
ventana_principal.mainloop()
