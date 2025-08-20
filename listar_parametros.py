import os
import django

# Configurar entorno Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "saf.settings")
django.setup()

from articulos.models import ParametroSistema

# Obtener todos los parámetros
parametros = ParametroSistema.objects.all()

if parametros:
    print("📋 Parámetros encontrados:")
    for p in parametros:
        print(f"🔹 Clave: {p.clave} | Valor: {p.valor} | Descripción: {p.descripcion}")
else:
    print("⚠️ No se encontraron parámetros en la base de datos.")
