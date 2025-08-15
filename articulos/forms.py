from django import forms
from .models import Articulo, Marca, Rubro, UpperCaseMixin  

class LoginForm(forms.Form):
    username = forms.CharField(
        label="Usuario",
        max_length=14,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'autofocus': True,
            'style': 'text-transform: uppercase; width:200px;',
            'oninput': 'this.value = this.value.toUpperCase()'
        })
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={
            'style': 'width:200px;',
            'class': 'form-control'
        })
    )

    def clean_username(self):
        username = self.cleaned_data.get('username', '').strip().upper()
        return username    


class UpperCaseMixin:
    """Mixin para convertir automáticamente todos los campos de texto a mayúsculas"""
    def clean(self):
        cleaned_data = super().clean()
        for field_name, value in cleaned_data.items():
            if isinstance(value, str):
                cleaned_data[field_name] = value.strip().upper()
        return cleaned_data

class MarcaForm(UpperCaseMixin, forms.ModelForm):
    class Meta:
        model = Marca
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'style': 'text-transform: uppercase;'})
        }


class RubroForm(UpperCaseMixin, forms.ModelForm):
    class Meta:
        model = Rubro
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'style': 'text-transform: uppercase;'})
        }        
        

class ArticuloForm(UpperCaseMixin, forms.ModelForm):

    marca_nombre = forms.CharField(
        label="Marca",
        max_length=14,
        required=False,
        widget=forms.TextInput(attrs={'style': 'text-transform: uppercase;'})
    )
    rubro_nombre = forms.CharField(
        label="Rubro",
        max_length=14,
        required=False,
        widget=forms.TextInput(attrs={'style': 'text-transform: uppercase;'})
    )

    class Meta:
        model = Articulo
        fields = ['codart', 'descrip', 'marca', 'rubro', 'precosto', 'margen', 'ncodalic']
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
            'preventa': forms.TextInput(attrs={'readonly': 'readonly'}),
            'ncodalic': forms.Select(attrs={
                'style': 'width: 250px;',
                'class': 'form-control'
            })
        }

    def clean_codart(self):
        codart = self.cleaned_data.get('codart', '').strip().upper()
        # Rellenar siempre con ceros a la izquierda hasta 14 caracteres
        codart = codart.rjust(14, '0')
        # Validar que no sea todo ceros
        if codart == "0" * 14:
            raise forms.ValidationError("El código no puede ser todo ceros.")
        return codart
    
    def save(self, commit=True):
        # Autocrear Marca
        marca_nombre = self.cleaned_data.get('marca_nombre', '').upper()
        if marca_nombre:
            marca, _ = Marca.objects.get_or_create(nombre=marca_nombre)
            self.instance.marca = marca

        # Autocrear Rubro
        rubro_nombre = self.cleaned_data.get('rubro_nombre', '').upper()
        if rubro_nombre:
            rubro, _ = Rubro.objects.get_or_create(nombre=rubro_nombre)
            self.instance.rubro = rubro

        return super().save(commit=commit)    

    
