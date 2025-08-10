from django.contrib import admin
from .models import Alicuota, Articulo

@admin.register(Alicuota)
class AlicuotaAdmin(admin.ModelAdmin):
    list_display = ('ncodalic', 'descrip', 'nporc')
    ordering = ('ncodalic',)

@admin.register(Articulo)
class ArticuloAdmin(admin.ModelAdmin):
    list_display = ('codart', 'descrip', 'ncodalic', 'preventa')
    list_filter = ('ncodalic',)  # Removido 'activo'
    search_fields = ('codart', 'descrip')    
    
 
