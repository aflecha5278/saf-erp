from django.db import models

class Moneda(models.Model):
    codmoneda = models.CharField(max_length=3, primary_key=True)
    descrip = models.CharField(max_length=30)
    cotiz = models.DecimalField(max_digits=15, decimal_places=5)
    signoc = models.CharField(max_length=3)
    
    def save(self, *args, **kwargs):
        if self.codmoneda:
            self.codmoneda = self.codmoneda.upper()
        if self.descrip:
            self.descrip = self.descrip.upper()
        if self.signoc:
            self.signoc = self.signoc.upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.codmoneda} - {self.descrip}"




