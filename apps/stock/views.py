# from django.shortcuts import render,HttpResponse
# from .models import StockProductos

# def stock(request):
#     productos = StockProductos.objects.select_related('producto_id', 'deposito_id').all()

#     busqueda = request.GET.get('busqueda')
#     filtro = request.GET.get('filtro')

#     if busqueda and filtro:
#         if filtro == "marca":
#             productos = productos.filter(producto_id__marca__icontains=busqueda)
#         elif filtro == "modelo":
#             productos = productos.filter(producto_id__modelo__icontains=busqueda)
#         elif filtro == "deposito":
#             productos = productos.filter(deposito_id__nombre__icontains=busqueda)
#         elif filtro == "ubicacion":
#             productos = productos.filter(ubicacion__icontains=busqueda)
#         elif filtro == "cantidad":
#             try:
#                 cantidad = int(busqueda)
#                 productos = productos.filter(cantidad_total=cantidad)
#             except ValueError:
#                 productos = productos.none() 

#     return render(request, 'stock.html', {
#         'productos': productos,
#         'show_navbar': True
#     })

from django.shortcuts import render, HttpResponse
from django.views import View
from .models import StockProductos
from django.contrib.auth.mixins import LoginRequiredMixin

class StockView(LoginRequiredMixin, View):
    def get(self, request):
        productos = StockProductos.objects.select_related('producto_id', 'deposito_id').all()

        busqueda = request.GET.get('busqueda')
        filtro = request.GET.get('filtro')

        if busqueda and filtro:
            if filtro == "marca":
                productos = productos.filter(producto_id__marca__icontains=busqueda)
            elif filtro == "modelo":
                productos = productos.filter(producto_id__modelo__icontains=busqueda)
            elif filtro == "deposito":
                productos = productos.filter(deposito_id__nombre__icontains=busqueda)
            elif filtro == "ubicacion":
                productos = productos.filter(ubicacion__icontains=busqueda)
            elif filtro == "cantidad":
                try:
                    cantidad = int(busqueda)
                    productos = productos.filter(cantidad_total=cantidad)
                except ValueError:
                    productos = productos.none()

        return render(request, 'stock.html', {
            'productos': productos,
            'show_navbar': True
        })