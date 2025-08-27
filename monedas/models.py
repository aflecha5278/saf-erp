from django.db import models

class Moneda(models.Model):
    codmoneda = models.CharField(max_length=3, primary_key=True)
    descrip = models.CharField(max_length=30)
    cotiz = models.DecimalField(max_digits=15, decimal_places=5)
    signoc = models.CharField(max_length=3)

    def __str__(self):
        return f"{self.codmoneda} - {self.descrip}"


