from django.db import models
from django.core.validators import MinValueValidator, RegexValidator
from django.utils import timezone
from decimal import Decimal, ROUND_HALF_UP
from .choices import UNIDADES, ACTIVO_CHOICES, PRODELA_CHOICES, TIPOPESO_CHOICES
from monedas.models import Moneda

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
        db_table = 'subrubro'
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
    deposito = models.CharField(max_length=14, blank=True, null=True, verbose_name="Depósito")
    precosto = models.DecimalField("Precio Costo", max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    margen = models.DecimalField("Margen %", max_digits=6, decimal_places=2, default=0)
    ncodalic = models.ForeignKey('Alicuota', verbose_name="Código Alícuota", on_delete=models.PROTECT)
    alic = models.DecimalField("% Alícuota", max_digits=5, decimal_places=2, editable=False, null=True, default=0)
    costoiva = models.DecimalField("Costo con IVA", max_digits=12, decimal_places=2, null=True, blank=True, default=0)
    preventa = models.DecimalField("Precio Venta (sin IVA)", max_digits=12, decimal_places=2, null=True, blank=True, default=0)
    prefinal = models.DecimalField(
        "Precio Final (con IVA)",
        max_digits=12,
        decimal_places=2,
        null=True,
        default=0,
        blank=True,
        validators=[MinValueValidator(0)]
    )
    fecultmod = models.DateField(null=True, blank=True)
    modo_calculo = models.CharField(
        max_length=1,
        choices=[('C', 'Costo → Final'), ('F', 'Final → Costo')],
        default='C',
        verbose_name="Modo de cálculo"
    )
    
    cantidad = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    unimed = models.CharField(max_length=2, choices=UNIDADES, default='UN')
    codprovee = models.CharField("Código de proveedor", max_length=14, blank=True, null=True)
    bajostock = models.DecimalField("Stock mínimo para alerta", max_digits=11, decimal_places=4, default=0)
    ubicacion = models.CharField("Ubicación", max_length=14, blank=True, null=True)
    obs = models.TextField("Observaciones", blank=True, null=True)
    activo = models.CharField(max_length=1, choices=ACTIVO_CHOICES, blank=False, default='S') 
    prodela = models.IntegerField(choices=PRODELA_CHOICES, null=True, blank=True)
    tipopeso = models.IntegerField(choices=TIPOPESO_CHOICES, null=True, blank=True)
    codmoneda = models.CharField(max_length=3, null=True, blank=True, verbose_name="Moneda")
    cotiz = models.DecimalField(max_digits=15, decimal_places=5, null=True, blank=True, verbose_name="Cotización:")
    ctome = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True, verbose_name="Prec. Costo de M.Ext.")
    vtame = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True, verbose_name="Prec. Venta de M.Ext.")
    finme = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True, verbose_name="Prec. Final de M.Ext.")

   
def save(self, *args, **kwargs):
    self.codart = self.codart.upper().zfill(14)

    alic = Decimal(str(self.ncodalic.nporc or "0"))
    margen = Decimal(str(self.margen or "0"))

    # --- costo en pesos ---
    precosto = Decimal(str(self.precosto or "0"))
    ctome = Decimal(str(self.ctome or "0"))
    cotiz = Decimal(str(self.cotiz or "0"))

    # Si hay costo en moneda extranjera y cotización, recalculo precosto en pesos
    if ctome > 0 and cotiz > 0:
        precosto = ctome * cotiz
        self.precosto = precosto

    # Alícuota guardada
    self.alic = alic

    # --- cálculo en pesos según modo_calculo ---
    if self.modo_calculo == 'C':  # Costo → Final
        self.preventa = precosto * (Decimal("1") + margen / Decimal("100"))
        self.prefinal = self.preventa * (Decimal("1") + alic / Decimal("100"))
    else:  # Final → Costo
        prefinal = Decimal(str(self.prefinal or "0"))
        self.preventa = prefinal / (Decimal("1") + alic / Decimal("100"))
        self.precosto = self.preventa / (Decimal("1") + margen / Decimal("100"))

    # Costo con IVA
    self.costoiva = self.precosto * (Decimal("1") + alic / Decimal("100"))

    # --- cálculo en moneda extranjera ---
    if ctome > 0:
        self.vtame = ctome * (Decimal("1") + margen / Decimal("100"))
        self.finme = self.vtame * (Decimal("1") + alic / Decimal("100"))
    else:
        self.vtame = Decimal("0")
        self.finme = Decimal("0")

    # --- redondeo a 2 decimales ---
    self.precosto = self.precosto.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    self.preventa = self.preventa.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    self.costoiva = self.costoiva.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    self.prefinal = self.prefinal.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    self.vtame = self.vtame.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    self.finme = self.finme.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    # --- fecha última modificación ---
    if self.pk:
        original = Articulo.objects.get(pk=self.pk)
        if (
            original.precosto != self.precosto or
            original.margen != self.margen or
            original.prefinal != self.prefinal or
            original.ctome != self.ctome or
            original.cotiz != self.cotiz
        ):
            self.fecultmod = timezone.now().date()
    else:
        self.fecultmod = timezone.now().date()

    super().save(*args, **kwargs)


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
        
class ParametroSistema(models.Model):
    clave = models.CharField(max_length=14, unique=True)
    descripcion = models.CharField(max_length=200)
    valor = models.CharField(max_length=1, choices=[('S', 'Sí'), ('N', 'No')])
    
    @property
    def activo(self):
        return self.valor == 'S'
    
    def __str__(self):
        return f"{self.descripcion} ({self.valor})"

    def save(self, *args, **kwargs):
        self.clave = self.clave.strip().upper()
        super().save(*args, **kwargs)
