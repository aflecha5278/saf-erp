from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),  # Cambia esto por la vista que tengas
]

