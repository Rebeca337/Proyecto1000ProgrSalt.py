from tkinter import *
import tkinter as tk
import sqlite3
from tkinter import messagebox as mb


ventana1=Tk()
ventana1.title("Inicio Sesion")
ventana1.geometry("1100x600")
ventana1.resizable(False,False)

db=sqlite3.connect('BaseDeDatosLogin.db')
c=db.cursor()
def vali():#validar usuario y contrasenia sin mensaje
    return len (NombreUsuario.get())!=0 and len (Contrasenia.get())!=0
def Login():
    if vali():
        usu=NombreUsuario.get()
        contr=Contrasenia.get()
        c.execute('SELECT * FROM registro WHERE nombre =? AND contrasenia =?',(usu,contr))
        if c.fetchall():
            mb.showinfo(title="Login Correcto",message="Usuario y contraseña correctos")

        else:
            mb.showerror(title="Login incorrecto",message="Usuario o contraseña incorrecto")
    


def CrearCuenta():
    CrearCuenta=Toplevel()
    CrearCuenta.title("Registro De Usuario")
    CrearCuenta.geometry("1100x600")
    CrearCuenta.resizable(False,False)

    img1 = PhotoImage(file="ProyectoCinemar/imagenes/CINE.Proyecto1.png")
    fondo2 = Label(CrearCuenta, image=img1).pack()
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

    #Enviar_btb=Button(CrearCuenta,text="Inicio De Sesion",width="25",height="0",bg="#ABB2B9")
    #Enviar_btb.place(x=100,y=540)

    def validacion():#validar datos para que no cree una cuenta en blanco
        return len (Nombre.get())!=0 and len (Apellido.get())!=0 and len (Contrasenia.get())!=0 and len(Repetir_Contrasenia.get())!=0 and len(Correo.get())!=0 and len(Fecha_De_Nacimiento.get())!=0
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
                CrearCuenta.destroy()		#Cerramos la ventana de registro
            else:	#Se ejecutara si las contraseñas no coinciden
                mb.showerror(title="Contraseña Incorrecta",message="Error \nLas contraseñas no coinciden.")	#Mostramos un mensaje
		#c.close()
		#db.close()
    Registro1_btb=Button(CrearCuenta,text="Registro",command=registro_boton,width="25",height="0",bg="#ABB2B9")
    Registro1_btb.place(x=100,y=510)

    widthtotal = CrearCuenta.winfo_screenwidth()
    heighttotal = CrearCuenta.winfo_screenheight()
    widthventana = 1100
    heightventana = 600
    width = round(widthtotal/2-widthventana/2)
    height = round(heighttotal/2-heightventana/2)
    CrearCuenta.geometry(str(widthventana)+"x"+str(heightventana)+"+"+str(width)+"+"+str(height))
    
    CrearCuenta.mainloop()

    
img = PhotoImage(file="ProyectoCinemar/imagenes/proyecto01-1.png")
fondo1 = Label(ventana1, image=img).pack()

ventana1_registro=Frame(ventana1,bg="white")
ventana1_registro.place(x=350,y=150,height=330,width=370)
titulo=Label(ventana1_registro,text="Iniciar Sesion",font=("Arial",30,"bold"),fg="#f50743",bg="white").place(x=70,y=30)
    
usuario=Label(ventana1_registro,text="Nombre",font=("Arial",13,"bold"),fg="#f50743",bg="white").place(x=100,y=100)
NombreUsuario=Entry(ventana1_registro,font=("time new roman",15),bg="lightgray")
NombreUsuario.place(x=90,y=130,width=250,height=35)
    

usuario_contraseña=Label(ventana1_registro,text="Contraseña",font=("Arial",13,"bold"),fg="#f50743",bg="white").place(x=100,y=170)
Contrasenia=Entry(ventana1_registro,font=("time new roman",15),bg="lightgray",show="*")
Contrasenia.place(x=90,y=190,width=250,height=35) 

Label(ventana1_registro,text="Recuperar Contraseña",bd=0,font=("time new roman",10,"bold")).place(x=90,y=240)

boton1=Button(ventana1_registro,text="Crear Cuenta",command=CrearCuenta,bd=0,font=("time new roman",10,"bold")).place(x=90,y=270)

Enviar_btb=Button(ventana1,text="Iniciar Sesion",command=Login,width="20",height="1",bg="#ABB2B9")
Enviar_btb.place(x=435,y=450)

widthtotal = ventana1.winfo_screenwidth()
heighttotal = ventana1.winfo_screenheight()
widthventana = 1269
heightventana = 639
width = round(widthtotal/2-widthventana/2)
height = round(heighttotal/2-heightventana/2)
ventana1.geometry(str(widthventana)+"x"+str(heightventana)+"+"+str(width)+"+"+str(height))

ventana1.mainloop()
