# from django.shortcuts import render, get_object_or_404, redirect
# from .models import Ordenes, Estados, Destinos
# from django.utils.timezone import now

from django.views.generic import ListView
from django.utils.timezone import now
from .models import Ordenes, Estados, Destinos
from django.views.generic.edit import UpdateView
from django.utils.timezone import now
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from .forms import EquipoForm, OrdenForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models


''' # vista anterior en funcion 
# Create your views here.
def ordenes_pendientes(request):
    ordenes = Ordenes.objects.select_related(
        'equipo_id__producto_id', 'estado_id'
    ).filter(
        estado_id__nombre_estado='Pendiente'
    )

    datos_ordenes = []
    for orden in ordenes:
        producto_modelo = orden.equipo_id.producto_id.modelo
        fecha_creacion = orden.fecha_creacion
        tiempo_transcurrido = now() - fecha_creacion
        datos_ordenes.append({
            'id': orden.id,
            'modelo': producto_modelo,
            'fecha_creacion': fecha_creacion,
            'tiempo_transcurrido': tiempo_transcurrido,
            'estado': orden.estado_id.nombre_estado,
        })

    return render(request, 'ordenes/ordenes_pendientes.html', {
        'ordenes': datos_ordenes
    })


def revisar_orden(request, orden_id):
    orden = get_object_or_404(Ordenes, id=orden_id)

    if request.method == 'POST':
        orden.falla_detectada = request.POST.get('falla_detectada')
        orden.reparacion = request.POST.get('reparacion')
        
        # Se actualiza el destino si se seleccionó uno
        destino_id = request.POST.get('destino')
        if destino_id:
            orden.destino_id = destino_id

        # Actualizar estado a "Revisado"
        estado_revisado = Estados.objects.get_or_create(nombre_estado='Revisado')[0]
        orden.estado_id = estado_revisado

        # Guardar fecha de revisión como ahora
        orden.fecha_revision = now()

        # Guardar cambios
        orden.save()

        # Redirigir a la lista de órdenes pendientes (o a otra vista de confirmación)
        return redirect('ordenes_pendientes')

    # GET: mostrar datos actuales
    estados = Estados.objects.all()
    destinos = Destinos.objects.all()

    return render(request, 'ordenes/revisar_orden.html', {
        'orden': orden,
        'estados': estados,
        'destinos': destinos,
    })
     
    
'''

class OrdenesPendientesListView(LoginRequiredMixin, ListView):
    model = Ordenes
    template_name = 'ordenes/ordenes_pendientes.html'
    context_object_name = 'ordenes'
    paginate_by = 10    # ✅ Paginación: 12 por página

    def get_queryset(self):
        queryset = Ordenes.objects.select_related(
            'equipo_id__producto_id', 'estado_id'
        ).filter(estado_id__nombre_estado='Pendiente')

        buscar = self.request.GET.get('buscar', '').strip()
        if buscar:
            queryset = queryset.filter(
                models.Q(equipo_id__producto_id__modelo__icontains=buscar) |
                models.Q(equipo_id__producto_id__marca__icontains=buscar)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        datos_ordenes = []

        for orden in context['ordenes']:
            datos_ordenes.append({
                'id': orden.id,
                'modelo': orden.equipo_id.producto_id.modelo,
                'fecha_creacion': orden.fecha_creacion,
                'tiempo_transcurrido': now() - orden.fecha_creacion,
                'estado': orden.estado_id.nombre_estado,
            })

        context['ordenes'] = datos_ordenes
        context['total_ordenes'] = Ordenes.objects.filter(estado_id__nombre_estado='Pendiente').count()  
        # ✅ Total de órdenes pendientes
        context['buscar'] = self.request.GET.get('buscar', '')
        return context


# class RevisarOrdenUpdateView(UpdateView):
#     model = Ordenes
#     fields = ['falla_detectada', 'reparacion', 'destino']  # Campos editables
#     template_name = 'ordenes/revisar_orden.html'
#     success_url = reverse_lazy('ordenes_pendientes')

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['estados'] = Estados.objects.all()
#         context['destinos'] = Destinos.objects.all()
#         return context

#     def form_valid(self, form):
#         orden = form.instance

#         # Asignar usuario desde request
#         orden._request = self.request

#         # Actualizar estado y fecha
#         estado_revisado, _ = Estados.objects.get_or_create(nombre_estado='Revisado')
#         orden.estado_id = estado_revisado
#         orden.fecha_revision = now()
        
#         return super().form_valid(form)


'''
class RevisarOrdenUpdateView(LoginRequiredMixin, UpdateView):
    model = Ordenes
    fields = ['falla_detectada', 'reparacion', 'destino']
    template_name = 'ordenes/revisar_orden.html'
    success_url = reverse_lazy('ordenes_pendientes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orden = self.object
        equipo_form = kwargs.get('equipo_form') or EquipoForm(instance=orden.equipo_id)
        context.update({
            'estados': Estados.objects.all(),
            'destinos': Destinos.objects.all(),
            'equipo_form': equipo_form
        })
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        equipo_form = EquipoForm(request.POST, instance=self.object.equipo_id)

        if form.is_valid() and equipo_form.is_valid():
            orden = form.save(commit=False)
            orden._request = self.request
            orden.estado_id, _ = Estados.objects.get_or_create(nombre_estado='Revisado')
            orden.fecha_revision = now()
            orden.save()
            equipo_form.save()
            return self.form_valid(form)
        else:
            # 👇 importante: pasar `form` explícitamente al contexto
            return self.render_to_response(
                self.get_context_data(form=form, equipo_form=equipo_form)
            )
'''

class RevisarOrdenUpdateView(LoginRequiredMixin, UpdateView):
    model = Ordenes
    form_class = OrdenForm  # <-- Usamos nuestro form personalizado
    template_name = 'ordenes/revisar_orden.html'
    success_url = reverse_lazy('ordenes_pendientes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orden = self.object
        equipo_form = kwargs.get('equipo_form') or EquipoForm(instance=orden.equipo_id)
        context.update({
            'estados': Estados.objects.all(),
            'destinos': Destinos.objects.all(),
            'equipo_form': equipo_form
        })
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        equipo_form = EquipoForm(request.POST, instance=self.object.equipo_id)

        if form.is_valid() and equipo_form.is_valid():
            orden = form.save(commit=False)
            orden._request = self.request
            orden.estado_id, _ = Estados.objects.get_or_create(nombre_estado='Revisado')
            orden.fecha_revision = now()
            orden.save()
            equipo_form.save()
            return self.form_valid(form)
        else:
            return self.render_to_response(
                self.get_context_data(form=form, equipo_form=equipo_form)
            )



# creando solo ordenes activas de prueba
class OrdenesActivasListView(LoginRequiredMixin, ListView):
    model = Ordenes
    template_name = 'ordenes/ordenes_activas.html'
    context_object_name = 'ordenes'
    paginate_by = 10  # 🔹 Paginación: 10 por página

    # def get_queryset(self):
    #     return Ordenes.objects.select_related(
    #         'equipo_id__producto_id', 'estado_id'
    #     ).filter(
    #         orden_activa=True
    #     ).order_by('-fecha_creacion')
    
    def get_queryset(self):
        if not self.request.GET:
            return Ordenes.objects.none()
        
        # queryset = Ordenes.objects.select_related(
        #     'equipo_id__producto_id', 'estado_id', 'destino'
        # ).filter(orden_activa=True)
        
        queryset = Ordenes.objects.select_related(
            'equipo_id__producto_id', 'estado_id', 'destino'
        ).all()


        # Filtros por GET
        estados = self.request.GET.getlist('estado')
        destinos = self.request.GET.getlist('destino')
        palletizado = self.request.GET.getlist('palletizado')
        buscar = self.request.GET.get('buscar', '').strip()

        if estados:
            queryset = queryset.filter(estado_id__in=estados)

        if destinos:
            queryset = queryset.filter(destino__in=destinos)

        if palletizado:
            queryset = queryset.filter(equipo_palletizado=True)
            
        
        if buscar:
            queryset = queryset.filter(
                models.Q(equipo_id__numero_serie__icontains=buscar) |
                models.Q(equipo_id__producto_id__modelo__icontains=buscar)
            )

        return queryset.order_by('-fecha_creacion')
    
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        datos_ordenes = []

        for orden in context['ordenes']:
            datos_ordenes.append({
                'id': orden.id,
                'modelo': orden.equipo_id.producto_id.modelo,
                'fecha_creacion': orden.fecha_creacion,
                'tiempo_transcurrido': now() - orden.fecha_creacion,
                'estado': orden.estado_id.nombre_estado,
            })

        context['ordenes'] = datos_ordenes
        context['total_ordenes'] = self.get_queryset().count()
        context['estados'] = Estados.objects.all()
        context['destinos'] = Destinos.objects.all()

        # 👇 Pasamos los filtros seleccionados
        context['filtro_estados'] = self.request.GET.getlist('estado')
        context['filtro_destinos'] = self.request.GET.getlist('destino')
        context['filtro_palletizado'] = self.request.GET.getlist('palletizado')

        return context
