class Butaca:
    def __init__(self, fila, numero, reservada=False):
        self.fila = fila          # letra de la fila: "A", "B", ...
        self.numero = numero      # 1, 2, 3, ...
        self.reservada = reservada

    @property
    def codigo(self):
        return f"{self.fila}{self.numero}"   # por ejemplo "B4"

    def __str__(self):
        return self.codigo
