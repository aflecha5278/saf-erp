from django.urls import path
from . import views
from .views import agregar_parametro, listar_parametros 
from articulos import views  

urlpatterns = [
    path('', views.login_view, name='login'),  # Página inicial es el login
    path('menu/', views.menu_principal, name='menu'),
    path('lista/', views.lista_articulos, name='lista_articulos'),
    path('agregar/', views.agregar_articulo, name='agregar_articulo'),
    path('modificar/<int:pk>/', views.modificar_articulo, name='modificar_articulo'),
    path('eliminar/<int:pk>/', views.eliminar_articulo, name='eliminar_articulo'),
    path('logout/', views.logout_view, name='logout'),
    path('parametros/', views.listar_parametros, name='listar_parametros'),
    path('parametros/nuevo/', views.agregar_parametro, name='agregar_parametro'),
    path('parametros/<int:pk>/editar/', views.editar_parametro, name='editar_parametro'),
    path('parametros/<int:pk>/eliminar/', views.eliminar_parametro, name='eliminar_parametro'),
    path('page2/<str:codart>/', views.page2_moneda_ext, name='page2_moneda_ext'),
]


