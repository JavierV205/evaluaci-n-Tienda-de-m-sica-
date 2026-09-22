from django import forms
from .models import Instrumentos

# validacion de formuulario

class InstrumentoForm(forms.ModelForm):
    class Meta:
        model = Instrumentos
        fields = ['nombre', 'tipo', 'marca', 'cantidad', 'precio']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Guitarra Electrica'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'marca': forms.Select(attrs={'class': 'form-select'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
        }

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
        return cantidad