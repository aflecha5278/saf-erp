from django import forms
from .models import Articulo

class ArticuloForm(forms.ModelForm):
    class Meta:
        model = Articulo
        fields = ['codart', 'descrip', 'precosto', 'ncodalic', 'margen']
        widgets = {
            'codart': forms.TextInput(attrs={
                'maxlength': 14,
                'style': 'width:150px; text-transform: uppercase;',
                'class': 'form-control'
            }),
            'descrip': forms.TextInput(attrs={
                'maxlength': 80,
                'style': 'width:400px; text-transform: uppercase;',
                'class': 'form-control'
            }),
            'precosto': forms.NumberInput(attrs={
                'step': '0.01',
                'min': '0',
                'style': 'width:120px;',
                'class': 'form-control calc'
            }),
            'margen': forms.NumberInput(attrs={
                'step': '0.01',
                'style': 'width:120px;',
                'class': 'form-control calc'
            }),
            'ncodalic': forms.Select(attrs={
                'style': 'width: 250px;',
                'class': 'form-control calc'
            }),
        }


