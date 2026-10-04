from django.db import models

from django.core.validators import MaxValueValidator, MinValueValidator


# Opciones para el campo 'tipo'
TIPO_CHOICES = [
        ('cuerda', 'Cuerda'),
        ('viento', 'Viento'),
        ('percusion', 'Percusion'),
        ('teclado', 'Teclado'),
    ]
# Opciones para el campo 'marca'
MARCA_CHOICES = [
        ('yamaha', 'Yamaha'),
        ('fender', 'Fender'),
        ('gibson', 'Gibson'),
        ('roland', 'Roland'),
        ('otra', 'Otra'),
    ]

class Instrumentos(models.Model):
    # El modelo representa los instrumentos disponibles en el inventario.
    nombre=models.CharField(max_length=25)
    tipo=models.CharField(max_length=20, 
                          choices=TIPO_CHOICES)
    cantidad=models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
    precio=models.PositiveIntegerField(validators=[MaxValueValidator(60000)])
    marca=models.CharField( max_length=20, 
                           choices=MARCA_CHOICES)

