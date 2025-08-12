from django import forms
from .models import Articulo

class ArticuloForm(forms.ModelForm):
    class Meta:
        model = Articulo
        fields = ['codart', 'descrip', 'precosto', 'margen', 'ncodalic']
        widgets = {
            'codart': forms.TextInput(attrs={
                'maxlength': 14,
                'style': 'width:150px; text-transform: uppercase;',
                'class': 'form-control input-codart'
            }),
            'descrip': forms.TextInput(attrs={
                'maxlength': 80,
                'style': 'width:400px; text-transform: uppercase;',
                'class': 'form-control input-descrip'
            }),
            'precosto': forms.NumberInput(attrs={
                'step': '0.01',
                'min': '0',
                'style': 'width:120px;',
                'class': 'form-control input-importe'
            }),
            'margen': forms.NumberInput(attrs={
                'step': '0.01',
                'style': 'width:120px;',
                'class': 'form-control input-importe'
            }),
            'ncodalic': forms.Select(attrs={
                'style': 'width: 250px;',
                'class': 'form-control'
            }),
        }

    def clean_codart(self):
        codart = self.cleaned_data.get('codart', '').strip().upper()

        # Rellenar siempre con ceros a la izquierda hasta 14 caracteres
        codart = codart.rjust(14, '0')

        # Validar que no sea todo ceros
        if codart == "0" * 14:
            raise forms.ValidationError("El código no puede ser todo ceros.")

        return codart
