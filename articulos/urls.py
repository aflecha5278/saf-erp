from django.urls import path
from .views import lista_articulos, agregar_articulo, modificar_articulo, login_view, logout_view, eliminar_articulo

urlpatterns = [
    path('', lista_articulos, name='lista_articulos'),
    path('agregar/', agregar_articulo, name='agregar_articulo'),
    path('modificar/<int:pk>/', modificar_articulo, name='modificar_articulo'),
    path('eliminar/<int:pk>/', eliminar_articulo, name='eliminar_articulo'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]











