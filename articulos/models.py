from django.db import models
from django.core.validators import MinValueValidator, RegexValidator 
from decimal import Decimal, ROUND_HALF_UP

class UpperCaseMixin:
    def save(self, *args, **kwargs):
        for field in self._meta.fields:
            if isinstance(field, models.CharField) and getattr(self, field.name):
                setattr(self, field.name, getattr(self, field.name).upper())
        super().save(*args, **kwargs)

class Alicuota(models.Model):
    ncodalic = models.IntegerField(primary_key=True)
    descrip = models.CharField("Descripción", max_length=50)
    nporc = models.DecimalField("Porcentaje", max_digits=5, decimal_places=2)

    class Meta:
        verbose_name = "Alícuota IVA"
        ordering = ['ncodalic']

    def __str__(self):
        return f"{self.descrip} ({self.nporc}%)"

class Subrubro(UpperCaseMixin, models.Model):
    rubro = models.ForeignKey('Rubro', on_delete=models.CASCADE, related_name='subrubros')
    nombre = models.CharField(max_length=14)

    class Meta:
        db_table = 'subrubro'          # ← nombre de tabla exacto
        unique_together = ('rubro', 'nombre')
        ordering = ['nombre']

    def __str__(self):
        return f"{self.rubro.nombre} - {self.nombre}"

class Articulo(UpperCaseMixin, models.Model):
    codart = models.CharField(
        "Código",
        max_length=14,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[A-Z0-9]+$',
                message='Solo se permiten letras mayúsculas y números.'
            )
        ],
        help_text='14 caracteres, se completa con ceros a la izquierda.'
    )
    descrip = models.CharField("Descripción", max_length=80)
    marca = models.ForeignKey('Marca', on_delete=models.PROTECT, blank=True, null=True)
    rubro = models.ForeignKey('Rubro', on_delete=models.PROTECT, blank=True, null=True)
    subrubro = models.ForeignKey('Subrubro', on_delete=models.PROTECT, blank=True, null=True)
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
        null=True,
        default=0
    )
    preventa = models.DecimalField(
        "Precio Venta (sin IVA)",
        max_digits=12,
        decimal_places=2,
        null=True,
        default=0
    )
    prefinal = models.DecimalField(
        "Precio Final (con IVA)",
        max_digits=12,
        decimal_places=2,
        null=True,
        default=0,
        blank=True,
        validators=[MinValueValidator(0)]
    )
    modo_calculo = models.CharField(
        max_length=1,
        choices=[('C', 'Costo → Final'), ('F', 'Final → Costo')],
        default='C'
    )
    from decimal import Decimal, ROUND_HALF_UP

    def save(self, *args, **kwargs):
        self.codart = self.codart.upper().zfill(14)

        # Usar Decimal siempre
        alic = Decimal(self.ncodalic.nporc or 0)
        margen = Decimal(self.margen or 0)
        precosto = Decimal(self.precosto or 0)

        self.alic = alic
        self.costoiva = precosto * (Decimal("1") + alic / Decimal("100"))

        if self.modo_calculo == 'C':  # Costo → Final
            self.preventa = precosto * (Decimal("1") + margen / Decimal("100"))
            self.prefinal = self.preventa * (Decimal("1") + alic / Decimal("100"))
        else:  # Final → Costo
            self.prefinal = Decimal(self.prefinal or 0)
            self.preventa = self.prefinal / (Decimal("1") + alic / Decimal("100"))
            self.precosto = self.preventa / (Decimal("1") + margen / Decimal("100"))

        # Redondear a 2 decimales
        self.precosto = Decimal(self.precosto).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        self.preventa = Decimal(self.preventa).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        self.costoiva = Decimal(self.costoiva).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        self.prefinal = Decimal(self.prefinal).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.codart} - {self.descrip}"

class Marca(UpperCaseMixin, models.Model):
    nombre = models.CharField(max_length=14, unique=True)

    class Meta:
        verbose_name_plural = "Marcas"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

class Rubro(UpperCaseMixin, models.Model):
    nombre = models.CharField(max_length=14, unique=True)

    class Meta:
        verbose_name_plural = "Rubros"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre