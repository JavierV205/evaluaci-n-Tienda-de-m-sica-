from django import forms
from .models import Instrumentos

# validacion de formuulario

class InstrumentoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Reemplaza la opcion vacia automatica por un mensaje claro para el usuario.
        tipo_choices = [choice for choice in self.fields['tipo'].choices if choice[0] != '']
        marca_choices = [choice for choice in self.fields['marca'].choices if choice[0] != '']
        self.fields['tipo'].choices = [('', 'Seleccione')] + tipo_choices
        self.fields['marca'].choices = [('', 'Seleccione')] + marca_choices
        self.fields['tipo'].error_messages['required'] = 'Debes seleccionar un tipo de instrumento.'
        self.fields['marca'].error_messages['required'] = 'Debes seleccionar una marca.'

    class Meta:
        model = Instrumentos
        fields = ['nombre', 'tipo', 'marca', 'cantidad', 'precio']
        # Estos atributos tambien bloquean valores invalidos desde el navegador.
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Guitarra Electrica', 'maxlength': '50'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'marca': forms.Select(attrs={'class': 'form-select'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '2000'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '1000000'}),
        }

    # Validacion personalizada: Precio mayor a 0
    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio is not None and precio <= 0:
            raise forms.ValidationError("El precio debe ser un numero mayor a cero.")
        return precio

    # Validacion personalizada: Cantidad positiva y no mayor que 2000
    def clean_cantidad(self):
        cantidad = self.cleaned_data.get('cantidad')
        if cantidad is not None and cantidad <= 0:
            raise forms.ValidationError("La cantidad en stock debe ser mayor que cero.")
        if cantidad is not None and cantidad > 2000:
            raise forms.ValidationError("La cantidad en stock no puede ser mayor que 2000.")
        return cantidad