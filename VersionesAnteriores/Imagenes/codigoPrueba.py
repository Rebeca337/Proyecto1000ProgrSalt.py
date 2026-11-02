from tkinter import *

#Creamos la ventana Principal 
global ventana_principal
ventana_principal=Tk()
ventana_principal.geometry("700x900")
ventana_principal.title("C  I  N  E  M  A  R")
ventana_principal.resizable(False,False)

 #Ventan Inicio De Sesion
def ventana1():
    global ventana1

    ventana1=Toplevel(ventana_principal)
    ventana1.title("Inicio Sesion")
    ventana1.geometry("1100x600")
    ventana1.resizable(False,False)

    
    img = PhotoImage(file="ProyectoCinemar/imagenes/proyecto01-1.png")
    fondo1 = Label(ventana1, image=img).pack()

    ventana1_registro=Frame(ventana1,bg="white")
    ventana1_registro.place(x=350,y=150,height=330,width=370)
    titulo=Label(ventana1_registro,text="Iniciar Sesion",font=("Arial",30,"bold"),fg="#f50743",bg="white").place(x=70,y=30)
    
    usuario=Label(ventana1_registro,text="Nombre de Usuario",font=("Arial",13,"bold"),fg="#f50743",bg="white").place(x=100,y=100)
    texto_usuario=Entry(ventana1_registro,font=("time new roman",15),bg="lightgray")
    texto_usuario.place(x=90,y=130,width=250,height=35)
    

    usuario_contraseña=Label(ventana1_registro,text="Contraseña",font=("Arial",13,"bold"),fg="#f50743",bg="white").place(x=100,y=170)
    texto_contraseña=Entry(ventana1_registro,font=("time new roman",15),bg="lightgray",show="*")
    texto_contraseña.place(x=90,y=190,width=250,height=35) 

    boton=Button(ventana1_registro,text="Recuperar Contraseña",bd=0,font=("time new roman",8,"bold")).place(x=90,y=240)

    boton1=Button(ventana1_registro,text="Crear Cuenta",command=CrearCuenta,bd=0,font=("time new roman",8,"bold")).place(x=90,y=270)

    Enviar_btb=Button(ventana1,text="Iniciar Sesion",command=ventana1_registro,width="20",height="1",bg="#ABB2B9")
    Enviar_btb.place(x=435,y=450)

    widthtotal = ventana1.winfo_screenwidth()
    heighttotal = ventana1.winfo_screenheight()
    widthventana = 1269
    heightventana = 639
    width = round(widthtotal/2-widthventana/2)
    height = round(heighttotal/2-heightventana/2)
    ventana1.geometry(str(widthventana)+"x"+str(heightventana)+"+"+str(width)+"+"+str(height))

    ventana1.mainloop()

def ventanas():
    ventana1.iconify()
    ventana1.deiconify()
    CrearCuenta.destroy()
    
   
    #Ventana De Registro
def CrearCuenta():
    global CrearCuenta
    CrearCuenta=Toplevel()
    CrearCuenta.title("Registro De Usuario")
    CrearCuenta.geometry("1100x600")
    CrearCuenta.resizable(False,False)

    img1 = PhotoImage(file="ProyectoCinemar/imagenes/CINE.Proyecto1.png")
    fondo2 = Label(CrearCuenta, image=img1).pack()
    nombre=Label(CrearCuenta,text="Nombre",font=("Arial",12,"bold"),fg="#f50743",bg="white").place(x=100,y=80)
    texto_usuario=Entry(CrearCuenta,font=("time new roman",12),bg="lightgray")
    texto_usuario.place(x=100,y=110,width=250,height=35)

    apellido=Label(CrearCuenta,text="Apellido",font=("Arial",12,"bold"),fg="#f50743",bg="white").place(x=100,y=150)
    texto_usuario=Entry(CrearCuenta,font=("time new roman",12),bg="lightgray")
    texto_usuario.place(x=100,y=180,width=250,height=35)

    contraseña=Label(CrearCuenta,text="Contraseña",font=("Arial",12,"bold"),fg="#f50743",bg="white").place(x=100,y=220)
    texto_usuario=Entry(CrearCuenta,font=("time new roman",12),bg="lightgray")
    texto_usuario.place(x=100,y=250,width=250,height=35)

    repetir_contraseña=Label(CrearCuenta,text="Repetir Contraseña",font=("Arial",12,"bold"),fg="#f50743",bg="white").place(x=100,y=297)
    texto_usuario=Entry(CrearCuenta,font=("time new roman",12),bg="lightgray")
    texto_usuario.place(x=100,y=330,width=250,height=35)

    correo=Label(CrearCuenta,text="Correo",font=("Arial",12,"bold"),fg="#f50743",bg="white").place(x=100,y=370)
    texto_usuario=Entry(CrearCuenta,font=("time new roman",12),bg="lightgray")
    texto_usuario.place(x=100,y=400,width=250,height=35)

    fecha_de_nacimiento=Label(CrearCuenta,text="Fecha De Nacimiento",font=("Arial",12,"bold"),fg="#f50743",bg="white").place(x=100,y=440)
    texto_usuario=Entry(CrearCuenta,font=("time new roman",12),bg="lightgray")
    texto_usuario.place(x=100,y=470,width=250,height=35)

    Enviar_btb=Button(CrearCuenta,text="Inicio De Sesion",command=ventanas,width="25",height="0",bg="#ABB2B9")
    Enviar_btb.place(x=100,y=540)
    Registro_btb=Button(CrearCuenta,text="Registro",width="25",height="0",bg="#ABB2B9")
    Registro_btb.place(x=100,y=510)
    if(CrearCuenta):
        ventana1.withdraw()

    widthtotal = CrearCuenta.winfo_screenwidth()
    heighttotal = CrearCuenta.winfo_screenheight()
    widthventana = 1100
    heightventana = 600
    width = round(widthtotal/2-widthventana/2)
    height = round(heighttotal/2-heightventana/2)
    CrearCuenta.geometry(str(widthventana)+"x"+str(heightventana)+"+"+str(width)+"+"+str(height))
    
    CrearCuenta.mainloop()


    #Ventana De Peliculas    
def Pelicula():
    global Pelicula
    Peliculas=Toplevel()
    Peliculas.title("Lista De Peliculas")
    Peliculas.geometry("1100x600")
    Peliculas.resizable(False,False)

    #Ventana De Productos
def Candy():
    global Candy
    Candy=Toplevel()
    Candy.title("Seleccione Su Pedido")
    Candy.geometry("850x550")
    Candy.resizable(False,False)

    img2 = PhotoImage(file="ProyectoCinemar/imagenes/proyectoCANDY2.png")
    fondo3 = Label(Candy, image=img2).pack()

    widthtotal = Candy.winfo_screenwidth()
    heighttotal = Candy.winfo_screenheight()
    widthventana = 850
    heightventana = 550
    width = round(widthtotal/2-widthventana/2)
    height = round(heighttotal/2-heightventana/2)
    Candy.geometry(str(widthventana)+"x"+str(heightventana)+"+"+str(width)+"+"+str(height))

    Candy.mainloop()

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
    boton1=Button(ventana0,command=ventana1,image= photoimage,bd=0,font=("time new roman",7,"bold")).place(x=1090,y=9)#icono de crear cuenta
    boton2=Button(ventana0,command=Pelicula,text="Peliculas",bd=0,font=("time new roman",8,"bold")).place(x=550,y=10)#boton fantasma
    boton3=Button(ventana0,command=Candy,text="Candy",bd=0,font=("time new roman",8,"bold")).place(x=650,y=10)#boton fantasma
    boton4=Button(ventana0,text="Cine Fan",bd=0,font=("time new roman",8,"bold")).place(x=750,y=10)#boton fantasma
    boton5=Button(ventana0,text="Regala Cine",bd=0,font=("time new roman",8,"bold")).place(x=850,y=10)#boton fantasma
    if (ventana0):
        ventana_principal.withdraw()
    #Con Esto Centramos La Pantalla
    widthtotal = ventana0.winfo_screenwidth()
    heighttotal = ventana0.winfo_screenheight()
    widthventana = 1269
    heightventana = 639
    width = round(widthtotal/2-widthventana/2)
    height = round(heighttotal/2-heightventana/2)
    ventana0.geometry(str(widthventana)+"x"+str(heightventana)+"+"+str(width)+"+"+str(height))

    ventana0.mainloop()

fondoboton= PhotoImage(file ="ProyectoCinemar/imagenes/Iron-Man-3TP!1.png") #imagen botono
label=Label(ventana_principal,image=fondoboton)
titulo=Label(text="Bienvenidos A Cinemar Click Para Iniciar!!!",font=("cambria",12),bg="#FFFFFF",fg="Black")
titulo.pack()

widthtotal = ventana_principal.winfo_screenwidth()
heighttotal = ventana_principal.winfo_screenheight()
widthventana = 700
heightventana = 900
width = round(widthtotal/2-widthventana/2)
height = round(heighttotal/2-heightventana/2)
ventana_principal.geometry(str(widthventana)+"x"+str(heightventana)+"+"+str(width)+"+"+str(height))

boton_principal=Button(ventana_principal,command=ventana0,image=fondoboton,bd=0,font=("time new roman",10,"bold"))#boton fantasma
boton_principal.place(x=1,y=20)
    
ventana_principal.mainloop()