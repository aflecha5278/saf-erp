from django import forms
from decimal import Decimal, ROUND_HALF_UP
from .models import Articulo, Marca, Rubro, Subrubro, UpperCaseMixin, ParametroSistema 
from .choices import UNIDADES  

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
    
    deposito = forms.ChoiceField(
        label="Depósito",
        choices=[('INTERNO', 'INTERNO')],
        initial='INTERNO',
        required=False,
        widget=forms.Select(attrs={
            'style': 'width: 200px;',
            'class': 'form-control'
        })
    )
    marca_nueva = forms.CharField(
        label='Marca nueva (opcional)',
        max_length=14,
        required=False,
        widget=forms.TextInput(attrs={
            'style': 'width: 200px ; text-transform: uppercase;',
            'class': 'form-control'
        })
    )
    rubro_nueva = forms.CharField(
        label='Rubro nuevo (opcional)',
        max_length=14,
        required=False,
        widget=forms.TextInput(attrs={
            'style': 'width: 200px ; text-transform: uppercase;',
            'class': 'form-control'
        })    
    )
    subrubro_nueva = forms.CharField(
        label='Sub-rubro nuevo (opcional)',
        max_length=14,
        required=False,
        widget=forms.TextInput(attrs={
            'style': 'width: 200px ; text-transform: uppercase;',
            'class': 'form-control'
        })  
    )
    
    def __init__(self, *args, codart_auto_activo=False, **kwargs):
        super().__init__(*args, **kwargs)
        if codart_auto_activo:
            self.fields['codart'].widget.attrs.update({
                'readonly': True,
                'class': 'form-control readonly-codart',
                'title': 'Generado automáticamente por el Cianova 360'
            })

        if 'rubro' in self.data and self.data['rubro']:
            self.fields['subrubro'].queryset = Subrubro.objects.filter(rubro_id=self.data['rubro'])
        elif self.instance.pk and self.instance.rubro_id:
            self.fields['subrubro'].queryset = Subrubro.objects.filter(rubro_id=self.instance.rubro_id)
        else:
            self.fields['subrubro'].queryset = Subrubro.objects.none()

    unimed = forms.ChoiceField(
        label="Unidad de medida",
        choices=UNIDADES,
        initial='UN',
        required=False,
        widget=forms.Select(attrs={
            'style': 'width: 50px;',
            'class': 'form-control'
        })
    )
    
    class Meta:
        model = Articulo
        fields = ['codart', 'descrip', 'marca', 'rubro', 'subrubro', 'subrubro_nueva',
          'precosto', 'margen', 'prefinal', 'modo_calculo', 'ncodalic', 'cantidad', 'unimed', 'codprovee', 'bajostock']
        widgets = {
            'codart': forms.TextInput(attrs={
                'maxlength': 14,
                'style': 'width:200px; text-transform: uppercase;',
                'class': 'form-control input-codart'
            }),
            'descrip': forms.TextInput(attrs={
                'maxlength': 80,
                'style': 'width:600px; text-transform: uppercase;',
                'class': 'form-control input-descrip'
            }),
            'precosto': forms.NumberInput(attrs={
                'step': '0.01',
                'min': '0',
                'style': 'width:150px;',
                'class': 'form-control input-importe'
            }),
            'margen': forms.NumberInput(attrs={
                'step': '0.01',
                'style': 'width:150px;',
                'class': 'form-control input-importe'
            }),
            'ncodalic': forms.Select(attrs={
                'style': 'width: 150px;',
                'class': 'form-control'
            }),
            'subrubro': forms.Select(attrs={
                'style': 'width: 150px;',
                'class': 'form-control'
            }),
            'prefinal': forms.NumberInput(attrs={
                'step': '0.01',
                'min': '0',
                'style': 'width:150px;',
                'class': 'form-control',
                'pattern': '[0-9]+(\.[0-9]{0,2})?'
            }),
            'cantidad': forms.NumberInput(attrs={
                'step': '0.0001',
                'min': '0',
                'style': 'width:150px;',
                'class': 'form-control input-cantidad',
                'pattern': r'^\d{1,9}(\.\d{1,4})?$',
            }),
        }

    def clean_precosto(self):
        precosto = self.cleaned_data.get('precosto')
        if precosto is not None:
            precosto = Decimal(precosto).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        return precosto

    def clean_margen(self):
        margen = self.cleaned_data.get('margen')
        if margen is not None:
            return round(float(margen), 2)
        return margen

    def clean_prefinal(self):
        prefinal = self.cleaned_data.get('prefinal')
        if prefinal is None or prefinal == '':
            raise forms.ValidationError("Este campo no puede estar vacío.")
        try:
            prefinal = Decimal(prefinal).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        except:
            raise forms.ValidationError("Ingrese un número válido.")
        return prefinal

    def save(self, commit=True):
        marca_nueva = self.cleaned_data.get('marca_nueva', '').strip().upper()
        if marca_nueva:
            marca, _ = Marca.objects.get_or_create(nombre=marca_nueva)
            self.instance.marca = marca

        rubro_nueva = self.cleaned_data.get('rubro_nueva', '').strip().upper()
        if rubro_nueva:
            rubro, _ = Rubro.objects.get_or_create(nombre=rubro_nueva)
            self.instance.rubro = rubro

        subrubro_nueva = self.cleaned_data.get('subrubro_nueva', '').strip().upper()
        if subrubro_nueva and self.cleaned_data.get('rubro'):
            subrubro, _ = Subrubro.objects.get_or_create(
                rubro_id=self.cleaned_data['rubro'].id,
                nombre=subrubro_nueva
            )
            self.instance.subrubro = subrubro

        return super().save(commit=commit)

class ParametroSistemaForm(forms.ModelForm):
    class Meta:
        model = ParametroSistema
        fields = ['clave', 'descripcion', 'valor']
        widgets = {
            'valor': forms.Select(choices=[('S', 'Sí'), ('N', 'No')]),
            'clave': forms.TextInput(attrs={'style': 'text-transform:uppercase;'}),
            'descripcion': forms.TextInput(attrs={
                'style': 'text-transform:uppercase;',
                'class': 'form-control w-100',
                'placeholder': 'Ingrese descripción del parámetro'
            }),
        }
