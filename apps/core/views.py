from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
""" 
def login(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Usuario y contraseña hardcodeados (solo para probar)
        if username == 'admin' and password == '1234':
            request.session['usuario'] = username  # guardamos el usuario en sesión
            return redirect('Dashboard')
        else:
            error = 'Usuario o contraseña incorrectos'

    return render(request, 'core/login.html', {'show_navbar': False, 'error': error})
""" 
@login_required
def dashboard(request):
    if 'usuario' not in request.session:
        return redirect('Login')  # si no hay usuario en sesión, lo redirigimos al login

    return render(request, 'dashboard.html', {'show_navbar': True})


#def logout(request):  ESTO SE HAcE DESDE USUARIOS 
 #   request.session.flush()  # eliminamos todos los datos de la sesión
  #  return redirect('Login')

# def home(request):
#     return render(request, 'core/home.html')



# myapp/views.py (o donde tengas tus vistas de órdenes) jose

from django.views.generic import TemplateView # Importamos TemplateView
from django.db.models import Q
import json # Necesario para json.dumps

from apps.ordenes.models import Ordenes, Estados, Destinos # Asegúrate de importar todos los modelos necesarios

class DashboardOrdenesView(LoginRequiredMixin, TemplateView):
    template_name = 'core/dashboard.html' # El nombre de tu plantilla HTML para el dashboard

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # --- Obtener los objetos de Estado y Destino para los filtros ---
        # Es crucial que estos nombres y IDs coincidan con tu base de datos.
        # Manejamos el caso donde un estado/destino no exista para evitar errores.

        # Estados
        estados = {}
        try:
            estados['pendiente'] = Estados.objects.get(nombre_estado="Pendiente")
            estados['revisado'] = Estados.objects.get(nombre_estado="Revisado")
            estados['palletizado'] = Estados.objects.get(nombre_estado="Palletizado")
        except Estados.DoesNotExist as e:
            print(f"Advertencia: Estado no encontrado para gráficos de tipo: {e}")

        # Destinos
        destinos = {}
        try:
            destinos['nuevo'] = Destinos.objects.get(nombre_destino="Nuevo")
            destinos['averia'] = Destinos.objects.get(nombre_destino="Averia")
            destinos['destruccion'] = Destinos.objects.get(nombre_destino="Destruccion")
        except Destinos.DoesNotExist as e:
            print(f"Advertencia: Destino no encontrado para gráficos de estado específico: {e}")

        # --- Cálculos para los 3 primeros gráficos (Órdenes por Tipo/Estado General) ---

        # Órdenes Totales Activas
        ordenes_totales_activas = Ordenes.objects.filter(orden_activa=True).count()

        # Órdenes Pendientes de Revisión (Estado="Pendiente" y activa)
        ordenes_pendientes_revision_activas = 0
        if 'pendiente' in estados:
            ordenes_pendientes_revision_activas = Ordenes.objects.filter(
                orden_activa=True,
                estado_id=estados['pendiente'].id
            ).count()

        # Órdenes Revisadas (Estado="Revisado" O "Palletizado" y activa)
        ordenes_revisadas_activas = 0
        q_revisadas_o_palletizadas = Q()   #definir Q
        if 'revisado' in estados:
            q_revisadas_o_palletizadas |= Q(estado_id=estados['revisado'].id)
        if 'palletizado' in estados:
            q_revisadas_o_palletizadas |= Q(estado_id=estados['palletizado'].id)

        if q_revisadas_o_palletizadas: # Solo si hay condiciones, aplicamos el filtro
            ordenes_revisadas_activas = Ordenes.objects.filter(
                orden_activa=True
            ).filter(q_revisadas_o_palletizadas).count()

        # Preparamos los datos para el primer grupo de gráficos
        datos_grafico_tipo = {
            'total_activas': ordenes_totales_activas,
            'pendientes_revision_activas': ordenes_pendientes_revision_activas,
            'revisadas_activas': ordenes_revisadas_activas,
        }
        context['datos_grafico_tipo_json'] = json.dumps(datos_grafico_tipo)


        # --- Cálculos para los 3 gráficos siguientes (Órdenes por Destino) ---

        # Órdenes para Destino "Nuevo" activas
        ordenes_destino_nuevo_activas = 0
        if 'nuevo' in destinos:
            ordenes_destino_nuevo_activas = Ordenes.objects.filter(
                orden_activa=True,
                destino=destinos['nuevo']
            ).count()

        # Órdenes para Destino "Averia" activas
        ordenes_destino_averia_activas = 0
        if 'averia' in destinos:
            ordenes_destino_averia_activas = Ordenes.objects.filter(
                orden_activa=True,
                destino=destinos['averia']
            ).count()

        # Órdenes para Destino "Destruccion" activas
        ordenes_destino_destruccion_activas = 0
        if 'destruccion' in destinos:
            ordenes_destino_destruccion_activas = Ordenes.objects.filter(
                orden_activa=True,
                destino=destinos['destruccion']
            ).count()

        # Preparamos los datos para el segundo grupo de gráficos
        datos_grafico_destino = {
            'destino_nuevo_activas': ordenes_destino_nuevo_activas,
            'destino_averia_activas': ordenes_destino_averia_activas,
            'destino_destruccion_activas': ordenes_destino_destruccion_activas,
        }
        context['datos_grafico_destino_json'] = json.dumps(datos_grafico_destino)

        return context
 