from django.db import models
from django.core.exceptions import ValidationError

TOPPINGS_VALIDOS = ['queso_extra', 'papas_al_hilo', 'salchicha_extra']

class PedidoCono(models.Model):
    VARIANTES = [
        ('Carnívoro', 'Carnívoro'),
        ('Vegetariano', 'Vegetariano'),
        ('Saludable', 'Saludable'),
    ]
    cliente = models.CharField(max_length=100)
    variante = models.CharField(max_length=20, choices=VARIANTES)
    toppings = models.JSONField(default=list)
    tamanio_cono = models.CharField(max_length=10)
    fecha_pedido = models.DateField(auto_now_add=True)

    def clean(self):
        if any(t not in TOPPINGS_VALIDOS for t in self.toppings):
            raise ValidationError("Toppings no válidos.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.cliente} - {self.variante}"
