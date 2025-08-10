from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),  # Página inicial es el login
    path('menu/', views.menu_principal, name='menu'),
    path('lista/', views.lista_articulos, name='lista_articulos'),
    path('agregar/', views.agregar_articulo, name='agregar_articulo'),
    path('modificar/<int:pk>/', views.modificar_articulo, name='modificar_articulo'),
    path('eliminar/<int:pk>/', views.eliminar_articulo, name='eliminar_articulo'),
    path('logout/', views.logout_view, name='logout'),
]
