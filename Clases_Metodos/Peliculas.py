from BaseDeDatos.conexion import consultar


class Pelicula:
    def __init__(self, id_pelicula, nombre, sinopsis, clasificacion, genero, duracion, director, actores):
        self.id_pelicula = id_pelicula
        self.nombre = nombre
        self.sinopsis = sinopsis
        self.clasificacion = clasificacion
        self.genero = genero
        self.duracion = duracion
        self.director = director
        self.actores = actores

    @classmethod
    def buscar(cls, id_pelicula):
        filas = consultar("SELECT * FROM peliculas WHERE id = ?", (id_pelicula,))
        if not filas:
            return None
        f = filas[0]
        return cls(f["id"], f["nombre"], f["sinopsis"], f["clasificacion"], f["genero"],
                   f["duracion"], f["director"], f["actores"])

    def ficha(self):
        """Texto con los datos de la película para mostrar en pantalla."""
        return (f"{self.nombre}  ({self.clasificacion} · {self.genero} · {self.duracion} min)\n"
                f"Director: {self.director}   Actores: {self.actores}\n"
                f"{self.sinopsis}")

    def __str__(self):
        return self.nombre
