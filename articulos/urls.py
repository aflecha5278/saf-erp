from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_articulos, name='lista_articulos'),
    path('agregar/', views.agregar_articulo, name='agregar_articulo'),
    path('modificar/<int:pk>/', views.modificar_articulo, name='modificar_articulo'),
    path('logout/', views.logout_view, name='logout'),
]






