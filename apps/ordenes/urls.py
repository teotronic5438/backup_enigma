from django.urls import path
# from . import views
from .views import OrdenesPendientesListView, RevisarOrdenUpdateView, OrdenesActivasListView, actualizar_serial
from django.contrib.auth.decorators import login_required

urlpatterns = [
    # path('pendientes/', views.ordenes_pendientes, name='ordenes_pendientes'),
    # path('revisar/<int:orden_id>/', views.revisar_orden, name='revisar_orden'),
    path('pendientes/', login_required(OrdenesPendientesListView.as_view()), name='ordenes_pendientes'),
    path('revisar/<int:pk>/', login_required(RevisarOrdenUpdateView.as_view()), name='revisar_orden'),
    path('ordenes/activas/', login_required(OrdenesActivasListView.as_view()), name='ordenes_activas'),
    path('orden/<int:pk>/actualizar_serial/', actualizar_serial, name='actualizar_serial'),
]
