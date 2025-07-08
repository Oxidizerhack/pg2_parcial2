# pg2_parcial2
# Parcial 2 - API REST con Patrones de Diseño

## Información del Estudiante

- **Nombre:** [Jhonny Antoni Quispe Mamani]
- **Curso:** [Segundo año de Sistemas Informáticos]
- **Materia:** Programación 2
- **Fecha:** 7 de Julio, 2025

## Descripción del Proyecto

Este proyecto implementa una API REST para la gestión de pedidos de conos utilizando Django REST Framework, aplicando patrones de diseño Factory Method, Builder y Singleton para el cálculo de precios e ingredientes.

## Patrones de Diseño Implementados

### 1. Factory Method Pattern

**Ubicación:** `api_conos/services/patrones.py` - Clase `ConoFactory`

**Propósito:** Crear instancias específicas de conos basándose en la variante seleccionada.

**Implementación:**
```python
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
```

**Aplicación:** Se utiliza en el método `get_precio_final()` del serializador para crear el tipo de cono base según la variante del pedido, encapsulando la lógica de creación y permitiendo agregar nuevas variantes fácilmente.

### 2. Builder Pattern

**Ubicación:** `api_conos/services/patrones.py` - Clase `ConoBuilder`

**Propósito:** Construir paso a paso un cono personalizado agregando toppings y calculando precios incrementales.

**Implementación:**
```python
class ConoBuilder:
    def __init__(self, cono):
        self.cono = cono

    def agregar_toppings(self, toppings):
        for topping in toppings:
            if topping in self.PRECIO_TOPPING:
                self.cono.ingredientes.append(topping)
                self.cono.precio += self.PRECIO_TOPPING[topping]
```

**Aplicación:** Se utiliza en los métodos `get_precio_final()` e `get_ingredientes_finales()` del serializador para construir el cono final agregando toppings sobre el objeto base creado por la fábrica, permitiendo una construcción flexible y modular.

### 3. Singleton Pattern

**Ubicación:** `api_conos/services/patrones.py` - Clase `LoggerSingleton`

**Propósito:** Mantener una única instancia de logger para registrar todas las operaciones de cálculo realizadas.

**Implementación:**
```python
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
```

**Aplicación:** Se utiliza en el serializador para registrar cada operación de cálculo de precio e ingredientes, garantizando que existe una única instancia del logger en toda la aplicación y manteniendo un registro centralizado de operaciones.

## Estructura del Proyecto
...
api_patrones/
├── api_conos/
│   ├── models.py           # Modelo PedidoCono con validaciones
│   ├── serializers.py      # Serializador con atributos calculados
│   ├── views.py           # ViewSet para la API REST
│   ├── admin.py           # Configuración del administrador
│   ├── services/
│   │   └── patrones.py    # Implementación de patrones de diseño
│   └── urls.py            # Rutas de la API
├── manage.py
└── README.md


## Endpoints de la API

### Pedidos de Conos
- `GET /api/pedidos_conos/` - Listar todos los pedidos
- `POST /api/pedidos_conos/` - Crear un nuevo pedido
- `GET /api/pedidos_conos/{id}/` - Obtener un pedido específico
- `PUT /api/pedidos_conos/{id}/` - Actualizar un pedido
- `DELETE /api/pedidos_conos/{id}/` - Eliminar un pedido

### Opciones Disponibles
- `GET /api/pedidos_conos/opciones/` - Obtener todas las opciones disponibles (variantes, toppings, tamaños)

## Modelo de Datos

### PedidoCono
- **cliente** (CharField): Nombre del cliente
- **variante** (CharField): Tipo de cono ('Carnívoro', 'Vegetariano', 'Saludable')
- **toppings** (JSONField): Lista de toppings adicionales
- **tamanio_cono** (CharField): Tamaño del cono ('Pequeño', 'Mediano', 'Grande')
- **fecha_pedido** (DateField): Fecha de creación automática

### Atributos Calculados
- **precio_final**: Calculado usando Factory + Builder patterns
- **ingredientes_finales**: Lista completa de ingredientes usando Builder pattern

## Validaciones

- Los toppings deben estar en la lista predefinida: `['queso_extra', 'papas_al_hilo', 'salchicha_extra']`
- Las variantes están limitadas a las opciones definidas
- Los tamaños están limitados a las opciones definidas

## Ejemplo de Uso

### Crear un pedido:
```json
POST /api/pedidos_conos/
{
  "cliente": "Juan Pérez",
  "variante": "Carnívoro",
  "toppings": ["queso_extra", "papas_al_hilo"],
  "tamanio_cono": "Grande"
}
```

### Respuesta:
```json
{
  "id": 1,
  "cliente": "Juan Pérez",
  "variante": "Carnívoro",
  "toppings": ["queso_extra", "papas_al_hilo"],
  "tamanio_cono": "Grande",
  "fecha_pedido": "2025-07-07",
  "precio_final": 25,
  "ingredientes_finales": ["carne", "queso", "queso_extra", "papas_al_hilo"],
  "toppings_display": ["Queso Extra", "Papas Al Hilo"]
}
```

## Instalación y Ejecución

1. Clonar el repositorio
2. Instalar dependencias: `pip install -r requirements.txt`
3. Ejecutar migraciones: `python manage.py migrate`
4. Crear superusuario: `python manage.py createsuperuser`
5. Ejecutar servidor: `python manage.py runserver`

## Capturas de Pantalla

### Administrador de Django
![Admin Interface](![alt text](image-1.png))

*Interfaz de administración mostrando el formulario de creación de pedidos con campos personalizados y validación de toppings*

### API REST Endpoint
![API Endpoint](![alt text](image.png))

*Endpoint de la API REST mostrando la lista de pedidos con atributos calculados (precio_final e ingredientes_finales)*

### Formulario de Creación en API
![API Form](![alt text](image-2.png))
*Formulario de creación en la interfaz de Django REST Framework mostrando las opciones disponibles para cada campo*

## Tecnologías Utilizadas

- Django 5.2.4
- Django REST Framework 3.16.0
- Python 3.x
- SQLite (base de datos por defecto)

## Patrones de Diseño - Beneficios

1. **Factory Method**: Permite agregar nuevas variantes de conos sin modificar código existente
2. **Builder**: Facilita la construcción paso a paso de conos personalizados
3. **Singleton**: Garantiza un registro centralizado de operaciones de cálculo

## Autor

[Jhonny] - [jhonny.antoni.quispe@gmail.com] - [https://github.com/Oxidizerhack]