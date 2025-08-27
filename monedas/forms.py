from django import forms
from .models import Moneda

class MonedaForm(forms.ModelForm):
    class Meta:
        model = Moneda
        fields = "__all__"
        widgets = {
            "codmoneda": forms.TextInput(attrs={
                "class": "form-control input-corto",
                "maxlength": 3,
                "placeholder": "Código"
            }),
            "descrip": forms.TextInput(attrs={
                "class": "form-control",
                "maxlength": 30,
                "placeholder": "Descripción"
            }),
            "cotiz": forms.NumberInput(attrs={
                "class": "form-control",
                "step": "0.00001",
                "placeholder": "Cotización"
            }),
            "signoc": forms.TextInput(attrs={
                "class": "form-control input-corto",
                "maxlength": 3,
                "placeholder": "Símbolo"
            }),
        }
        labels = {
            "codmoneda": "Código",
            "descrip": "Descripción",
            "cotiz": "Cotización",
            "signoc": "Símbolo",
        }
