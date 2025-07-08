class Cono:
    def __init__(self):
        self.ingredientes = []
        self.precio = 0

class ConoCarnivoro(Cono):
    def __init__(self):
        super().__init__()
        self.ingredientes = ['carne', 'queso']
        self.precio = 20

class ConoVegetariano(Cono):
    def __init__(self):
        super().__init__()
        self.ingredientes = ['verduras', 'queso']
        self.precio = 15

class ConoSaludable(Cono):
    def __init__(self):
        super().__init__()
        self.ingredientes = ['ensalada']
        self.precio = 10

class ConoFactory:
    @staticmethod
    def crear_cono(variante):
        if variante == 'Carnívoro':
            return ConoCarnivoro()
        elif variante == 'Vegetariano':
            return ConoVegetariano()
        elif variante == 'Saludable':
            return ConoSaludable()
        raise ValueError("Variante inválida")

class ConoBuilder:
    PRECIO_TOPPING = {
        'queso_extra': 2,
        'papas_al_hilo': 3,
        'salchicha_extra': 4
    }

    def __init__(self, cono):
        self.cono = cono

    def agregar_toppings(self, toppings):
        for topping in toppings:
            if topping in self.PRECIO_TOPPING:
                self.cono.ingredientes.append(topping)
                self.cono.precio += self.PRECIO_TOPPING[topping]

    def obtener_precio(self):
        return self.cono.precio

    def obtener_ingredientes(self):
        return self.cono.ingredientes


class LoggerSingleton:
    _instancia = None
    logs = []

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
        return cls._instancia

    def log(self, mensaje):
        self.logs.append(mensaje)
        print(mensaje)
