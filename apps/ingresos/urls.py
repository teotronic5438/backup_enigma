# apps/usuarios/urls.py
# from django.urls import path
# from .views import test_view

# urlpatterns = [
    # path('test/', test_view),
# ]

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import crear_remito, editar_remito, eliminar_remito, aprobar_remito, ver_remito

#Clases
from .views import ListarRemitosView, ListarRemitosHistorialView

#apis
from .views import remito_list, remito_create
from django.contrib.auth.decorators import login_required

urlpatterns = [
    # path('ingresos/', listar_remitos, name='ingresos'),
    # path('history/', listar_remitos_historial, name='ingresos_historial'),
    path('ingresos/', login_required(ListarRemitosView.as_view()), name='ingresos'),
    path('history/', login_required(ListarRemitosHistorialView.as_view()), name='ingresos_historial'),
    path('nuevo/', crear_remito, name='crear_remito'),
    path('editar/<int:pk>/', editar_remito, name='editar_remito'),
    path('eliminar/<int:pk>/', eliminar_remito, name='eliminar_remito'),
    path('aprobar/<int:pk>/', aprobar_remito, name='aprobar_remito'),
    path('remitos/', remito_list, name='remitos-list'),
    path('remitos/crear/', remito_create, name='remito-create'),
    path('ver/<int:pk>/', ver_remito, name='ver_remito'),
    
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])