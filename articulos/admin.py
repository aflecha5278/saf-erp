from django.contrib import admin
from .models import Alicuota, Articulo, ParametroSistema  # 👈 Importás el modelo

@admin.register(Alicuota)
class AlicuotaAdmin(admin.ModelAdmin):
    list_display = ('ncodalic', 'descrip', 'nporc')
    ordering = ('ncodalic',)

@admin.register(Articulo)
class ArticuloAdmin(admin.ModelAdmin):
    list_display = ('codart', 'descrip', 'ncodalic', 'preventa')
    list_filter = ('ncodalic',)
    search_fields = ('codart', 'descrip')

@admin.register(ParametroSistema)
class ParametroSistemaAdmin(admin.ModelAdmin):
    list_display = ('clave', 'descripcion', 'valor')  # 👈 Columnas visibles
    search_fields = ('clave', 'descripcion')          # 👈 Búsqueda rápida
    ordering = ('clave',)                             # 👈 Orden por defecto

    
    
    
 
