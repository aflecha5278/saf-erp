from django.contrib import admin
from .models import Articulo

@admin.register(Articulo)
class ArticuloAdmin(admin.ModelAdmin):
    list_display = ('codart', 'descrip', 'precosto')
    search_fields = ('codart', 'descrip')
