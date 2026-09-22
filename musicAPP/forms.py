from django import forms
from .models import Instrumentos

# validacion de formuulario

class InstrumentoForm(forms.ModelForm):
    class Meta:
        model = Instrumentos
        fields = ['nombre', 'tipo', 'marca', 'cantidad', 'precio']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '50', 'placeholder': 'Ej. Guitarra Electrica'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'marca': forms.Select(attrs={'class': 'form-select'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '1000'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '1000000'}),
        }

    def clean_tipo(self):
        tipo = self.cleaned_data.get('tipo')
        if tipo == 'selecione':
            raise forms.ValidationError('Debes seleccionar un tipo de instrumento.')
        return tipo

    def clean_marca(self):
        marca = self.cleaned_data.get('marca')
        if marca == 'selecione':
            raise forms.ValidationError('Debes seleccionar una marca.')
        return marca

    # Validacion personalizada: Precio mayor a 0
    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio is not None and precio <= 0:
            raise forms.ValidationError("El precio debe ser un numero mayor a cero.")
        return precio

    # Validacion personalizada: Cantidad no negativa
    def clean_cantidad(self):
        cantidad = self.cleaned_data.get('cantidad')
        if cantidad is not None and cantidad < 0:
            raise forms.ValidationError("La cantidad en stock no puede ser negativa.")
        if cantidad is not None and cantidad > 1000:
            raise forms.ValidationError("La cantidad no puede ser mayor que 1000.")
        return cantidad