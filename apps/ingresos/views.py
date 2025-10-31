# Create your views here.
# get_object_or_404: busca un objeto por clave primaria (PK); si no lo encuentra, devuelve error 404.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Remitos, RemitoProducto
from apps.ordenes.models import Equipos, Ordenes, Estados
from .forms import RemitoForm, RemitoProductoFormSet
from django.views.generic import ListView
from apps.stock.models import StockProductos, Depositos
from django.contrib.auth.mixins import LoginRequiredMixin   # para proteger las vistas CBV
from django.contrib.auth.decorators import login_required   # para proteger las vistas FBV


# listado con clase
class ListarRemitosView(LoginRequiredMixin, ListView):
    model = Remitos
    template_name = 'remitos/listar.html'
    context_object_name = 'remitos'

    def get_queryset(self):
        return Remitos.objects.filter(aprobado=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['show_navbar'] = True
        return context

# listado con función    
# def listar_remitos(request):
#     remitos = Remitos.objects.filter(aprobado=False)
#     return render(request, 'remitos/listar.html', {'remitos': remitos, 'show_navbar': True})

# listado aprobado con clase
class ListarRemitosHistorialView(LoginRequiredMixin, ListView):
    model = Remitos
    template_name = 'remitos/listar_historial.html'
    context_object_name = 'remitos'

    def get_queryset(self):
        return Remitos.objects.filter(aprobado=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['show_navbar'] = True
        return context

# listado aprobado con función
# def listar_remitos_hitorial(request):
#     remitos = Remitos.objects.filter(aprobado=True)
#     return render(request, 'remitos/listar_historial.html', {'remitos': remitos, 'show_navbar': True})


@login_required     # SOLO EL DECORADOR, LA REDIRECCION ESTA DEFINIDA EN EL SETTING
def crear_remito(request):
    if request.method == 'POST':
        form = RemitoForm(request.POST)
        formset = RemitoProductoFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            remito = form.save(commit=False)
            remito._request = request  # inyectamos el request para que setee el usuario
            remito.save()
            formset.instance = remito
            formset.save()
            return redirect('ingresos')
    else:
        form = RemitoForm()
        formset = RemitoProductoFormSet()
    return render(request, 'remitos/formulario.html', {'form': form, 'formset': formset})


@login_required     # SOLO EL DECORADOR, LA REDIRECCION ESTA DEFINIDA EN EL SETTING
def editar_remito(request, pk):
    remito = get_object_or_404(Remitos, pk=pk)

    if request.method == 'POST':
        print("POST recibido")
        form = RemitoForm(request.POST, instance=remito)
        formset = RemitoProductoFormSet(request.POST, instance=remito)

        if form.is_valid() and formset.is_valid():
            print("Formularios válidos. Guardando...")
            form.save()
            formset.save()
            return redirect('ingresos')
        else:
            print("Formularios inválidos")
            print("Errores form:", form.errors)
            print("Errores formset:", formset.errors)
    else:
        form = RemitoForm(instance=remito)
        formset = RemitoProductoFormSet(instance=remito)

    return render(request, 'remitos/formulario.html', {'form': form, 'formset': formset})


@login_required     # SOLO EL DECORADOR, LA REDIRECCION ESTA DEFINIDA EN EL SETTING
def ver_remito(request, pk):
    remito = get_object_or_404(Remitos, pk=pk)
    productos_relacionados = RemitoProducto.objects.filter(remito_id=remito)

    return render(request, 'remitos/ver_formulario.html', {'remito': remito, 
                                                           'productos_relacionados': productos_relacionados,
                                                           })


# Aplica las mismas líneas de depuración a la función editar_remito

# def crear_remito(request):
#     if request.method == 'POST':
#         form = RemitoForm(request.POST)
#         # Inicializamos el formset con los datos POST y una instancia vacía de Remitos
#         formset = RemitoProductoFormSet(request.POST, instance=Remitos())

#         if form.is_valid() and formset.is_valid():
#             remito = form.save(commit=False) # No guardar aún, para asignar campos adicionales

#             # # Asignar el usuario actual si está logueado
#             # # Es crucial que el usuario esté autenticado para que request.user sea válido
#             # if request.user.is_authenticated:
#             #     remito.usuario_id = request.user
#             # else:
#             #     # Manejar caso de usuario no autenticado, quizás redirigir a login o asignar un usuario por defecto
#             #     # Por ahora, lanzar un error o redirigir si el campo es obligatorio
#             #     # raise Exception("Usuario no autenticado, no se puede crear el remito.")
#             #     return redirect('login') # O tu URL de login

#             remito.aprobado = False # Por defecto, un remito nuevo no está aprobado
#             remito.save() # Ahora sí guardamos el Remito

#             formset.instance = remito # Asociar el formset con el remito recién creado
#             formset.save() # Guardar los productos asociados al remito
            

#             return redirect('ingresos') # Redirigir a la lista de remitos no aprobados
#     else:
#         form = RemitoForm()
#         formset = RemitoProductoFormSet(instance=Remitos()) # Instancia vacía para el formset inicial
    
#     # Asegúrate de que el template formulario.html esté preparado para renderizar el formset
#     return render(request, 'remitos/formulario.html', {'form': form, 'formset': formset, 'show_navbar': True})

''' reemplazando modelo de funcion para agregar ordenes
def aprobar_remito(request, pk):
    remito = get_object_or_404(Remitos, pk=pk)
    
    if remito.aprobado == False:
        remito.aprobado = True
        remito.save()
        return redirect('ingresos')
    else:
        return redirect('ingresos')
'''
from apps.ordenes.models import get_estado_pendiente
from django.db import transaction

# la pk es la clave del remito
def aprobar_remito(request, pk):
    remito = get_object_or_404(Remitos, pk=pk)  # obtenemos el remito con la clave pk

    if remito.aprobado:
        return redirect('ingresos')     # si la aprobo redirige a ingresos

    with transaction.atomic():      # que los cambios se hagan juntos
        remito.aprobado = True      # actualiza el campo aprobado del objeto remito
        remito.save()

        estado_pendiente = Estados.objects.get(pk=get_estado_pendiente())
        
        remito_productos = RemitoProducto.objects.filter(remito_id=remito)  # trae todos los productos que coincidam con el id remito

        for rp in remito_productos:     # recorres con for in
            producto = rp.producto_id       # por cada itearcion obtiene el id
            cantidad = rp.cantidad
            ## nota
            deposito = remito.deposito_id

            # ACTUALIZAR STOCK
            stock_producto, creado = StockProductos.objects.get_or_create(
                producto_id=producto,
                deposito_id=deposito,
                defaults={'cantidad_total': 0}
            )
            stock_producto.cantidad_total += cantidad
            stock_producto.save()

            # Crear equipos y órdenes
            for _ in range(cantidad):
                equipo = Equipos.objects.create(
                    producto_id=producto,
                    observaciones=f"Generado por remito {remito.numero_remito}"
                )

                orden = Ordenes(
                    remito_id=remito,
                    equipo_id=equipo,
                    estado_id=estado_pendiente,
                    orden_activa=True,
                )
                orden._request = request  # Para que setee los usuarios en el `save()`
                orden.save()

    return redirect('ingresos')



def eliminar_remito(request, pk):
    remito = get_object_or_404(Remitos, pk=pk)
    if request.method == 'POST':
        remito.delete()
        return redirect('ingresos')
    return render(request, 'remitos/confirmar_eliminar.html', {'remito': remito, 'show_navbar': True})



# vistas para apis
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializers import RemitoSerializer

@api_view(['GET'])
@permission_classes([AllowAny])  # <--- esta línea es clave
def remito_list(request):
    remitos = Remitos.objects.all()
    serializer = RemitoSerializer(remitos, many=True)
    return Response(serializer.data)


from rest_framework import status

@api_view(['POST'])
@permission_classes([AllowAny])  # Cambiar a IsAuthenticated si tenés autenticación activa
def remito_create(request):
    """
    Crea un nuevo remito con los datos básicos.
    """
    serializer = RemitoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"mensaje": "Remito creado correctamente", "remito": serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)