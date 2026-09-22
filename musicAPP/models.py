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
    nombre=models.CharField(max_length=50)
    tipo=models.CharField(max_length=50, 
                          choices=TIPO_CHOICES)
    cantidad=models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(2000)])
    precio=models.PositiveIntegerField(validators=[MaxValueValidator(1000000)])
    marca=models.CharField( max_length=50, 
                           choices=MARCA_CHOICES)

