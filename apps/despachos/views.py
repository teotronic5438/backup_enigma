# apps/despachos/views.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.timezone import now
from django.views import View
from apps.ordenes.models import Ordenes, Estados, Destinos
from apps.despachos.models import Pallet, DetallePallet
from django.db.models import Q, Count
from django.urls import reverse
from collections import defaultdict
from django.db import transaction

# para actulizar stock
from collections import defaultdict
from apps.stock.models import StockProductos

# --- CLASE-BASADA EN VISTA BASE (Para reutilizar lógica común de filtrado y búsqueda en vistas de visualización de pallets) ---
class BaseOrdenesDespachoView(LoginRequiredMixin, View):
    template_name = 'despachos/ordenes_despacho_base.html'
    destino_base_nombre = None
    titulo_pagina = "Órdenes Palletizadas"

    def get_queryset(self):
        estado_palletizado_obj = Estados.objects.filter(nombre_estado__iexact='palletizado').first()
        estado_despachado_pallet_obj = Estados.objects.filter(nombre_estado__iexact='despachado').first()
        destino_obj = Destinos.objects.filter(nombre_destino__iexact=self.destino_base_nombre).first()

        if not estado_palletizado_obj:
            messages.error(self.request, "El estado 'Palletizado' no está configurado en la base de datos (modelo Estados). Por favor, créalo en el panel de administración.")
            return Ordenes.objects.none()

        if not destino_obj:
            messages.error(self.request, f"El destino '{self.destino_base_nombre}' no está configurado en la base de datos (modelo Destinos). Por favor, créalo en el panel de administración.")
            return Ordenes.objects.none()

        queryset = Ordenes.objects.filter(
            estado_id=estado_palletizado_obj,
            destino=destino_obj,
            detalle_pallet_asociado__pallet__isnull=False
        )

        if estado_despachado_pallet_obj:
            queryset = queryset.exclude(detalle_pallet_asociado__pallet__estado_pallet=estado_despachado_pallet_obj)

        queryset = queryset.select_related(
            'destino', 'equipo_id', 'equipo_id__producto_id', 'estado_id',
            'detalle_pallet_asociado__pallet__estado_pallet', 'detalle_pallet_asociado__pallet__destino', 
            'usuario', 'editado_por', 'palletizado_por'
        ).order_by('detalle_pallet_asociado__pallet__nro_pallet', 'fecha_creacion')

        return queryset

    def get_context_data(self, request, queryset, mensaje_busqueda=None):
        pallets_agrupados = defaultdict(lambda: {
            'id': None,
            'nro_pallet': 'N/A',
            'destino': 'N/A',
            'fecha_creacion': None,
            'estado_pallet': 'N/A',
            'ordenes': [],
            'usuario_creacion_pallet': 'N/A' 
        })

        for orden in queryset:
            equipo_obj = orden.equipo_id
            
            producto_obj = getattr(equipo_obj, 'producto_id', None)
            producto_modelo = getattr(producto_obj, 'modelo', 'N/A')
            producto_marca = getattr(producto_obj, 'marca', 'N/A')

            nombre_destino = getattr(orden.destino, 'nombre_destino', 'Sin asignar')
            nombre_estado = getattr(orden.estado_id, 'nombre_estado', 'Sin estado')

            if hasattr(orden, 'detalle_pallet_asociado') and orden.detalle_pallet_asociado and orden.detalle_pallet_asociado.pallet:
                pallet_obj = orden.detalle_pallet_asociado.pallet
                pallet_id = pallet_obj.id
                pallet_info = {
                    'id': pallet_obj.id,
                    'nro_pallet': pallet_obj.nro_pallet,
                    'destino': getattr(pallet_obj.destino, 'nombre_destino', 'N/A'),
                    'fecha_creacion': pallet_obj.fecha_creacion,
                    'estado_pallet': getattr(pallet_obj.estado_pallet, 'nombre_estado', 'N/A'),
                    'usuario_creacion_pallet': getattr(pallet_obj.usuario, 'username', 'N/A')
                }

                if pallets_agrupados[pallet_id]['id'] is None:
                    pallets_agrupados[pallet_id].update(pallet_info)

                pallets_agrupados[pallet_id]['ordenes'].append({
                    'id': orden.id,
                    'numero_serie': getattr(equipo_obj, 'numero_serie', 'N/A'),
                    'modelo': producto_modelo,
                    'marca': producto_marca,
                    'fecha_creacion': orden.fecha_creacion,
                    'estado': nombre_estado,
                    'destino': nombre_destino,
                    'falla_detectada': orden.falla_detectada,
                    'reparacion': orden.reparacion,
                    'fecha_revision': orden.fecha_revision,
                })

        lista_pallets = sorted(list(pallets_agrupados.values()), key=lambda p: p['nro_pallet'] if p['nro_pallet'] != 'N/A' else '')

        context = {
            'pallets_activos': lista_pallets,
            'mensaje_busqueda': mensaje_busqueda,
            'query_actual': request.GET.get('q', ''),
            'titulo_pagina': self.titulo_pagina,
            'destinos_disponibles': Destinos.objects.all().order_by('nombre_destino'),
            'estados_disponibles': Estados.objects.all().order_by('nombre_estado'),
            'mostrar_boton_armar_pallet': False,
            'max_items_pallet': 15,
            'despachar_pallet_url': reverse('despachos:despachar_pallet'),
        }
        return context

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        query = request.GET.get('q', '')
        mensaje_busqueda = None

        if query:
            q_objects = Q(id__icontains=query) | Q(equipo_id__numero_serie__icontains=query)
            queryset = queryset.filter(q_objects)

            if not queryset.exists():
                mensaje_busqueda = f"No se encontraron órdenes con el ID/Número de Serie '{query}'."

        context = self.get_context_data(request, queryset, mensaje_busqueda)
        return render(request, self.template_name, context)


# --- VISTA PARA ÓRDENES REVISADAS (PUNTO DE PARTIDA PARA LA ASIGNACIÓN DE DESTINO Y PALLETIZADO) ---
class OrdenesRevisadasView(LoginRequiredMixin,View):
    template_name = 'despachos/revisadas.html'

    def get(self, request, *args, **kwargs):
        estado_revisado_obj = Estados.objects.filter(nombre_estado__iexact='revisado').first()

        if not estado_revisado_obj:
            messages.error(request, "El estado 'Revisado' no está configurado en la base de datos (modelo Estados). Por favor, créalo en el panel de administración.")
            return render(request, self.template_name, {
                'ordenes': [],
                'error_estado': "Estado 'Revisado' no encontrado.",
                'query_actual': request.GET.get('q', ''),
                'filtro_destino_seleccionado': request.GET.get('filtro_destino', 'todos'),
                'destinos_para_filtro': Destinos.objects.all().order_by('nombre_destino'),
                'destinos_para_despacho': Destinos.objects.all().order_by('nombre_destino'),
                'mostrar_boton_despacho': False,
                'titulo_pagina': 'Órdenes Revisadas',
            })

        ordenes_queryset = Ordenes.objects.filter(
            estado_id=estado_revisado_obj,
            equipo_palletizado=False
        ).select_related(
            'destino', 'equipo_id', 'equipo_id__producto_id', 'estado_id'
        ).order_by('-fecha_creacion')

        query = request.GET.get('q', '')
        filtro_destino_param = request.GET.get('filtro_destino', 'todos')

        if filtro_destino_param and filtro_destino_param != 'todos':
            destino_obj_filtro = Destinos.objects.filter(nombre_destino__iexact=filtro_destino_param).first()
            if destino_obj_filtro:
                ordenes_queryset = ordenes_queryset.filter(destino=destino_obj_filtro)
            else:
                messages.warning(request, f"El destino '{filtro_destino_param}' no es un filtro válido o no existe en la base de datos.")

        mensaje_busqueda = None
        if query:
            q_objects = Q(id__icontains=query) | Q(equipo_id__numero_serie__icontains=query)
            ordenes_queryset = ordenes_queryset.filter(q_objects)

            if not ordenes_queryset.exists():
                mensaje_busqueda = f"No se encontraron órdenes con el ID/Número de Serie '{query}'."

        datos_ordenes = []
        if ordenes_queryset.exists():
            for orden in ordenes_queryset:
                equipo_obj = orden.equipo_id
                producto_obj = getattr(equipo_obj, 'producto_id', None)

                producto_modelo = getattr(producto_obj, 'modelo', 'N/A')
                producto_marca = getattr(producto_obj, 'marca', 'N/A')

                nombre_destino = getattr(orden.destino, 'nombre_destino', 'Sin asignar')
                nombre_estado = getattr(orden.estado_id, 'nombre_estado', 'Sin estado')

                datos_ordenes.append({
                    'id': orden.id,
                    'equipo_id': orden.equipo_id.id if orden.equipo_id else None,
                    'numero_serie': getattr(equipo_obj, 'numero_serie', 'N/A'),
                    'modelo': producto_modelo,
                    'marca': producto_marca,
                    'fecha_creacion': orden.fecha_creacion,
                    'estado': nombre_estado,
                    'destino': nombre_destino,
                    'falla_detectada': orden.falla_detectada,
                    'reparacion': orden.reparacion,
                    'fecha_revision': orden.fecha_revision,
                })

        destinos_para_despacho = Destinos.objects.all().order_by('nombre_destino')

        context = {
            'ordenes': datos_ordenes,
            'mensaje_busqueda': mensaje_busqueda,
            'query_actual': query,
            'filtro_destino_seleccionado': filtro_destino_param,
            'destinos_para_filtro': Destinos.objects.all().order_by('nombre_destino'),
            'destinos_para_despacho': destinos_para_despacho,
            'mostrar_boton_despacho': bool(datos_ordenes), 
            'titulo_pagina': 'Órdenes Revisadas',
            'max_items_pallet': 15,
        }
        return render(request, self.template_name, context)


class ProcesarDespachoOrdenesView(LoginRequiredMixin,View):
    def post(self, request, *args, **kwargs):
        ordenes_ids = request.POST.getlist('orden_ids')
        destino_id = request.POST.get('destino_id_despacho')
        MAX_ITEMS_PER_PALLET = 15

        if not ordenes_ids:
            messages.error(request, "No se seleccionó ninguna orden para palletizar.")
            return redirect('despachos:ordenes_revisadas')

        if not destino_id:
            messages.error(request, "No se seleccionó ningún destino para el pallet.")
            return redirect('despachos:ordenes_revisadas')

        with transaction.atomic():
            try:
                destino_obj = get_object_or_404(Destinos, id=destino_id)
                estado_palletizado_obj = get_object_or_404(Estados, nombre_estado__iexact='palletizado')
                estado_revisado_obj = get_object_or_404(Estados, nombre_estado__iexact='revisado')
                estado_despachado_obj = Estados.objects.filter(nombre_estado__iexact='despachado').first()

                current_pallet = None
                updated_count = 0
                pallets_creados_o_actualizados = set()

                for orden_id in ordenes_ids:
                    try:
                        orden = Ordenes.objects.get(id=orden_id)

                        if orden.estado_id != estado_revisado_obj:
                            messages.warning(request, f"La orden con ID {orden_id} no está en estado 'Revisado' y no pudo ser procesada.")
                            continue

                        detalle_pallet_exists = DetallePallet.objects.filter(orden_id=orden).exists()

                        if detalle_pallet_exists:
                            if not orden.equipo_palletizado:
                                orden.equipo_palletizado = True
                                orden._request = request
                                orden.save()
                                messages.info(request, f"Se corrigió la orden {orden_id}: Marcada como palletizada ya que se encontró asociada a un pallet.")
                            messages.warning(request, f"La orden con ID {orden_id} ya está asociada a un pallet y no pudo ser re-procesada.")
                            continue

                        # Validar que el destino asignado coincida con el seleccionado
                        if orden.destino and orden.destino != destino_obj:
                            messages.warning(request, f"La orden con ID {orden_id} no se cargó al pallet porque el destino seleccionado ('{destino_obj}') no coincide con el asignado ('{orden.destino}').")
                            continue

                        active_pallets_for_destination_qs = Pallet.objects.filter(
                            destino=destino_obj
                        ).annotate(
                            item_count=Count('detalles')
                        ).filter(
                            item_count__lt=MAX_ITEMS_PER_PALLET
                        ).order_by('fecha_creacion')

                        if estado_despachado_obj:
                            active_pallets_for_destination_qs = active_pallets_for_destination_qs.exclude(
                                estado_pallet=estado_despachado_obj
                            )

                        active_pallet_with_space = active_pallets_for_destination_qs.first()

                        if not current_pallet or current_pallet.detalles.count() >= MAX_ITEMS_PER_PALLET:
                            if active_pallet_with_space:
                                current_pallet = active_pallet_with_space
                            else:
                                last_pallet = Pallet.objects.order_by('-id').first()
                                next_pallet_number = 1
                                if last_pallet and last_pallet.nro_pallet and last_pallet.nro_pallet.isdigit():
                                    next_pallet_number = int(last_pallet.nro_pallet) + 1
                                generated_nro_pallet = str(next_pallet_number).zfill(4)

                                current_pallet = Pallet.objects.create(
                                    nro_pallet=generated_nro_pallet,
                                    destino=destino_obj,
                                    estado_pallet=estado_palletizado_obj,
                                    usuario=request.user,
                                )
                                messages.info(request, f"Se ha creado un nuevo pallet: Nro. {current_pallet.nro_pallet} para el destino '{destino_obj.nombre_destino}'.")

                        DetallePallet.objects.create(
                            pallet=current_pallet,
                            orden_id=orden,
                        )

                        orden.estado_id = estado_palletizado_obj
                        orden.equipo_palletizado = True
                        orden._request = request
                        orden.save()
                        updated_count += 1
                        pallets_creados_o_actualizados.add(current_pallet.id)

                    except Ordenes.DoesNotExist:
                        messages.warning(request, f"La orden con ID {orden_id} no existe y no pudo ser procesada.")
                    except Exception as e:
                        messages.error(request, f"Error al procesar orden {orden_id} para pallet: {e}")

                if updated_count > 0:
                    messages.success(request, f"{updated_count} órdenes fueron distribuidas en {len(pallets_creados_o_actualizados)} pallet(s) para destino '{destino_obj.nombre_destino}'.")
                else:
                    messages.info(request, "No se procesó ninguna orden para palletizar. Asegúrate de que estén en estado 'Revisado', no palletizadas y con el destino correcto.")

                return redirect('despachos:ordenes_revisadas')

            except Destinos.DoesNotExist:
                messages.error(request, "El destino de pallet seleccionado no es válido. Asegúrate de que exista en tu base de datos.")
                return redirect('despachos:ordenes_revisadas')
            except Estados.DoesNotExist as e:
                messages.error(request, f"Uno de los estados requeridos no está configurado en la base de datos: {e}. Por favor, créalos en el panel de administración de Django.")
                return redirect('despachos:ordenes_revisadas')
            except Exception as e:
                messages.error(request, f"Ocurrió un error general al procesar el pallet: {e}")
                return redirect('despachos:ordenes_revisadas')


class ProcesarDespachoPalletView(LoginRequiredMixin,View):
    def post(self, request, *args, **kwargs):
        pallet_id = request.POST.get('pallet_id_a_despachar')
        if not pallet_id:
            messages.error(request, "No se recibió el ID del pallet a despachar.")
            return redirect(request.META.get('HTTP_REFERER', '/'))

        with transaction.atomic():
            try:
                pallet = get_object_or_404(Pallet, id=pallet_id)

                estado_despachado_pallet_obj = Estados.objects.filter(nombre_estado__iexact='despachado').first()



                if not estado_despachado_pallet_obj:
                    messages.error(request, "El estado 'Despachado' para pallets no está configurado en la base de datos (modelo Estados). Por favor, créalo.")
                    return redirect(request.META.get('HTTP_REFERER', '/'))

                estado_despachado_orden_obj = Estados.objects.filter(nombre_estado__iexact='despachado').first()
                if not estado_despachado_orden_obj:
                    messages.warning(request, "El estado 'Despachado' para órdenes no está configurado. Las órdenes no cambiarán de estado a 'Despachado'.")

                pallet.estado_pallet = estado_despachado_pallet_obj
                pallet.fecha_despacho = now()
                pallet.usuario_despacho = request.user if request.user.is_authenticated else None
                pallet._request = request
                pallet.save()
                
                # Agrupar productos por producto_id y contar cuántos hay de cada uno
                productos_despachados = defaultdict(int)

                for detalle_pallet in pallet.detalles.all():
                    orden = detalle_pallet.orden_id
                    if orden and orden.equipo_id and orden.equipo_id.producto_id:
                        producto_id = orden.equipo_id.producto_id.id
                        productos_despachados[producto_id] += 1
                # para agrupar y controlar stock
                

                # Descontar del stock según los productos agrupados
                for producto_id, cantidad_despachada in productos_despachados.items():
                    # Si manejás un depósito específico, filtralo por depósito_id también
                    stock_entry = StockProductos.objects.filter(producto_id=producto_id).first()
                    if stock_entry:
                        if stock_entry.cantidad_total >= cantidad_despachada:
                            stock_entry.cantidad_total -= cantidad_despachada
                            stock_entry.save()
                        else:
                            messages.warning(request, f"Stock insuficiente para el producto {stock_entry.producto_id}. Se necesitaban {cantidad_despachada}, pero hay {stock_entry.cantidad_total}.")
                    else:
                        messages.warning(request, f"No se encontró stock para el producto con ID {producto_id}.")


                ordenes_actualizadas_count = 0
                for detalle_pallet in pallet.detalles.all():
                    orden = detalle_pallet.orden_id
                    if orden:
                        if estado_despachado_orden_obj:
                            orden.estado_id = estado_despachado_orden_obj
                        orden.orden_activa = False
                        orden._request = request
                        orden.save()
                        ordenes_actualizadas_count += 1

                messages.success(request, f"Pallet {pallet.nro_pallet} despachado exitosamente. Se actualizaron {ordenes_actualizadas_count} órdenes.")

            except Pallet.DoesNotExist:
                messages.error(request, f"El pallet con ID {pallet_id} no existe.")
            except Estados.DoesNotExist:
                messages.error(request, "Error: Uno o ambos estados ('Despachado' para pallet u orden) no encontrados en la base de datos.")
            except Exception as e:
                messages.error(request, f"Ocurrió un error al despachar el pallet: {e}")

            return redirect(request.META.get('HTTP_REFERER', '/'))


# --- VISTAS PARA ÓRDENES CON ESTADO REVISADO Y UN DESTINO ESPECÍFICO (CON HISTORIAL) ---
class OrdenesNuevasView(BaseOrdenesDespachoView):
    destino_base_nombre = 'nuevo'
    titulo_pagina = 'Órdenes Nuevas Palletizadas'

    def get_context_data(self, request, queryset, mensaje_busqueda=None):
        context = super().get_context_data(request, queryset, mensaje_busqueda)

        estado_despachado_obj = Estados.objects.filter(nombre_estado__iexact='despachado').first()
        destino_obj = Destinos.objects.filter(nombre_destino__iexact=self.destino_base_nombre).first()

        pallets_despachados = []
        if estado_despachado_obj and destino_obj:
            despachados_queryset = Pallet.objects.filter(
                estado_pallet=estado_despachado_obj,
                destino=destino_obj
            ).select_related(
                'destino', 'estado_pallet', 'usuario', 'usuario_despacho', 'remito_salida'
            ).prefetch_related(
                'detalles__orden_id__equipo_id__producto_id',
                'detalles__orden_id__estado_id',
                'detalles__orden_id__destino'
            ).order_by('-fecha_despacho')

            for pallet in despachados_queryset:
                ordenes_en_pallet = []
                for detalle_pallet in pallet.detalles.all():
                    orden = detalle_pallet.orden_id
                    if orden:
                        equipo_obj = getattr(orden, 'equipo_id', None)
                        producto_obj = getattr(equipo_obj, 'producto_id', None)

                        modelo_nombre = getattr(producto_obj, 'modelo', 'N/A')
                        marca_nombre = getattr(producto_obj, 'marca', 'N/A')

                        ordenes_en_pallet.append({
                            'id': orden.id,
                            'numero_serie': getattr(equipo_obj, 'numero_serie', 'N/A'),
                            'modelo': modelo_nombre,
                            'marca': marca_nombre,
                            'estado': getattr(orden.estado_id, 'nombre_estado', 'N/A'),
                        })

                pallets_despachados.append({
                    'id': pallet.id,
                    'nro_pallet': pallet.nro_pallet,
                    'destino': getattr(pallet.destino, 'nombre_destino', 'N/A'),
                    'fecha_creacion': pallet.fecha_creacion,
                    'fecha_despacho': pallet.fecha_despacho,
                    'estado_pallet': getattr(pallet.estado_pallet, 'nombre_estado', 'N/A'),
                    'usuario_creacion': getattr(pallet.usuario, 'username', 'N/A'),
                    'usuario_despacho': getattr(pallet.usuario_despacho, 'username', 'N/A'),
                    'remito_salida': getattr(pallet.remito_salida, 'nro_remito', 'N/A'),
                    'cantidad_ordenes': len(ordenes_en_pallet),
                    'ordenes': ordenes_en_pallet,
                })

        context['pallets_despachados'] = pallets_despachados
        context['titulo_historial'] = f"Historial de Pallets Despachados a {self.destino_base_nombre.capitalize()}"

        return context

class OrdenesAveriadasView(OrdenesNuevasView):
    destino_base_nombre = 'averia'
    titulo_pagina = 'Órdenes Averiadas Palletizadas'

class OrdenesDestruidasView(OrdenesNuevasView):
    destino_base_nombre = 'destruccion'
    titulo_pagina = 'Órdenes de Destrucción Palletizadas'