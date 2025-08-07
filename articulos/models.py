from django.db import models

class Articulo(models.Model):
    codart = models.CharField("Código", max_length=14, unique=True)
    descrip = models.CharField("Descripción", max_length=80)
    precosto = models.DecimalField("Precio Costo", max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.codart} - {self.descrip}"
