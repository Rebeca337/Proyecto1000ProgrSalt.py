class CrearCuenta:
    def __init__(self,nombre,apellido,contrasenia,repetir_contrasenia,correo,repetir_correo,genero,fecha_de_nacimiento,dni):
        self.nombre=nombre
        self.apellido=apellido
        self.contrasenia=contrasenia
        self.repetir_contrasenia=repetir_contrasenia
        self.correo=correo
        self.repetir_correo=repetir_correo
        self.genero=genero
        self.fecha_de_nacimiento=fecha_de_nacimiento
        self.dni=dni
       #self.contrasenia_tipo=contrasenia_tipo=123


    def validar_contrasenia(self):
        if self.contrasenia==self.repetir_contrasenia:
            return True
        else:
            return False


    def validar_correo(self):
        if self.correo==self.repetir_correo:
            return True
        else:
            return False  


    def __str__(self):
        cadena=self.nombre+"\n"
        cadena+=self.apellido+"\n"
        cadena+=self.contrasenia+"\n"
        cadena+=self.repetir_contrasenia+"\n"
        cadena+=self.correo+"\n"
        cadena+=self.repetir_correo+"\n"
        cadena+=self.genero+"\n"
        cadena+=str(self.fecha_de_nacimiento)+"\n"
        cadena+=str(self.dni)+"\n"
        return cadena
       #cadena+=str(self.contrasenia_tipo)+"\n"   


class fecha_de_nacimiento:
    def __init__(self,dia,mes,anio):
        self.dia=dia
        self.mes=mes
        self.anio=anio


    def __str__(self):
        return str(self.dia)+ "/" + str(self.mes)+ "/" + str(self.anio)


fecha1=fecha_de_nacimiento(10,5,1995)

juan=CrearCuenta("juan","lopez","123abc","123abc","mauri@gmail.com","mauri@gmail.com","masculino",fecha1,39581808)
print(juan)
print(juan.validar_contrasenia)
print(juan.validar_correo)
    
                            

