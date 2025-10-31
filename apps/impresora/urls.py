# apps/impresora/urls.py
from django.urls import path
from . import views

app_name = 'impresora'  # 🔹 importante: define el namespace

urlpatterns = [
    path('configuracion/', views.configuracion_impresora, name='configuracion'),
    path('imprimir-etiqueta/', views.imprimir_etiqueta, name='imprimir_etiqueta'),
]
