from django import forms
from .models import Articulo, Alicuota

class ArticuloForm(forms.ModelForm):
    class Meta:
        model = Articulo
        fields = ['codart', 'descrip', 'precosto', 'ncodalic', 'margen']
        widgets = {
            'codart': forms.TextInput(attrs={'maxlength': 14, 'style': 'text-transform: uppercase;'}),
            'descrip': forms.TextInput(attrs={'maxlength': 80, 'style': 'text-transform: uppercase;'}),
            'precosto': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
            'margen': forms.NumberInput(attrs={'step': '0.01'}),
            'ncodalic': forms.Select(attrs={'style': 'width: 250px;'}),
        }
        
