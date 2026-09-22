from django.db import models

from django.core.validators import MinValueValidator


# Opciones para el campo 'tipo'
TIPO_CHOICES = [
        ('selecione', 'selecione'),
        ('cuerda', 'Cuerda'),
        ('viento', 'Viento'),
        ('percusion', 'Percusion'),
        ('teclado', 'Teclado'),
    ]
# Opciones para el campo 'marca'
MARCA_CHOICES = [
        ('selecione', 'selecione'),
        ('yamaha', 'Yamaha'),
        ('fender', 'Fender'),
        ('gibson', 'Gibson'),
        ('roland', 'Roland'),
        ('otra', 'Otra'),
    ]

class Instrumentos(models.Model):
    nombre=models.CharField(max_length=100)
    tipo=models.CharField(max_length=50, 
                          choices=TIPO_CHOICES, 
                          default='selecione')
    cantidad=models.IntegerField(validators=[MinValueValidator(0)])
    precio=models.PositiveIntegerField()
    marca=models.CharField( max_length=50, 
                           choices=MARCA_CHOICES, 
                           default='selecione')

