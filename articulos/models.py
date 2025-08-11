from django.db import models
from django.core.validators import MinValueValidator

class Alicuota(models.Model):
    ncodalic = models.IntegerField(primary_key=True)
    descrip = models.CharField("Descripción", max_length=50)
    nporc = models.DecimalField("Porcentaje", max_digits=5, decimal_places=2)

    class Meta:
        verbose_name = "Alícuota IVA"
        ordering = ['ncodalic']
    
    def __str__(self):
        return f"{self.descrip} ({self.nporc}%)"


class Articulo(models.Model):
    # Campos editables
    codart = models.CharField("Código", max_length=14, unique=True)
    descrip = models.CharField("Descripción", max_length=80)
    precosto = models.DecimalField(
        "Precio Costo", 
        max_digits=12, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    margen = models.DecimalField(
        "Margen %",
        max_digits=6,
        decimal_places=2,
        default=0
    )
    ncodalic = models.ForeignKey(
        'Alicuota',
        verbose_name="Código Alícuota",
        on_delete=models.PROTECT
    )

    # Campos calculados
    alic = models.DecimalField(
        "% Alícuota",
        max_digits=5,
        decimal_places=2,
        editable=False,
        null=True,
        default=0
    )
    costoiva = models.DecimalField(
        "Costo con IVA",
        max_digits=12,
        decimal_places=2,
        editable=False,
        null=True,
        default=0
    )
    preventa = models.DecimalField(
        "Precio Venta (sin IVA)",
        max_digits=12,
        decimal_places=2,
        editable=False,
        null=True,
        default=0
    )
    prefinal = models.DecimalField(
        "Precio Final (con IVA)",
        max_digits=12,
        decimal_places=2,
        editable=False,
        null=True,
        default=0
    )
    
    def save(self, *args, **kwargs):
        self.alic = self.ncodalic.nporc
        self.costoiva = self.precosto * (1 + self.alic / 100)
        self.preventa = self.precosto * (1 + self.margen / 100)
        self.prefinal = self.preventa * (1 + self.alic / 100)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.codart} - {self.descrip}"

    