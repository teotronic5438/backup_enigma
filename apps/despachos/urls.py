# apps/despachos/urls.py
from django.urls import path
from . import views

app_name = 'despachos'

urlpatterns = [

    path('nuevas/', views.OrdenesNuevasView.as_view(), name='ordenes_nuevas'),
    path('averiadas/', views.OrdenesAveriadasView.as_view(), name='ordenes_averiadas'),
    path('destruccion/', views.OrdenesDestruidasView.as_view(), name='ordenes_destruccion'),
    path('revisadas/', views.OrdenesRevisadasView.as_view(), name='ordenes_revisadas'),
    path('procesar-despacho-ordenes/', views.ProcesarDespachoOrdenesView.as_view(), name='procesar_despacho_ordenes'),
    path('despachar-pallet/', views.ProcesarDespachoPalletView.as_view(), name='despachar_pallet'),
]