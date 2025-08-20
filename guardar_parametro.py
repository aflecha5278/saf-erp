import os
import django

# Configurar entorno Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "saf.settings")
django.setup()

from articulos.models import ParametroSistema

# Crear o actualizar el parámetro
clave = "CODART_AUTO"
valor = "SÍ"
descripcion = "Automatización de código de artículo"

parametro, creado = ParametroSistema.objects.update_or_create(
    clave=clave,
    defaults={"valor": valor, "descripcion": descripcion}
)

if creado:
    print(f"? Parámetro '{clave}' creado con valor '{valor}'")
else:
    print(f"?? Parámetro '{clave}' actualizado a '{valor}'")
