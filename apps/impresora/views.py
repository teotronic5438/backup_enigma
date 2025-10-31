from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import ConfiguracionImpresora
import win32print

@login_required(login_url='usuarios:login')
def configuracion_impresora(request):
    impresoras = [p[2] for p in win32print.EnumPrinters(2)]
    actual = ConfiguracionImpresora.objects.first()

    if request.method == "POST":
        seleccion = request.POST.get("impresora")
        verificar = request.POST.get("verificar")

        if verificar and seleccion:
            # Intentar abrir la impresora seleccionada
            try:
                hPrinter = win32print.OpenPrinter(seleccion)
                win32print.ClosePrinter(hPrinter)
                messages.success(request, f"✅ La impresora '{seleccion}' está accesible.")
            except Exception as e:
                messages.error(request, f"❌ Error de conexión con '{seleccion}': {str(e)}")
            return redirect("impresora:configuracion")

        if seleccion:
            if actual:
                actual.nombre = seleccion
                actual.save()
            else:
                ConfiguracionImpresora.objects.create(nombre=seleccion)
            messages.success(request, f"💾 Impresora '{seleccion}' configurada correctamente.")
            return redirect("impresora:configuracion")

    return render(
        request,
        "impresora/configuracion.html",
        {"impresoras": impresoras, "actual": actual.nombre if actual else None}
    )


from django.shortcuts import redirect
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

@login_required
@require_POST
def imprimir_etiqueta(request):
    modelo = request.POST.get("modelo")
    marca = request.POST.get("marca")
    serial = request.POST.get("serial")

    # Aquí iría tu lógica para generar la etiqueta ZPL
    # Por ahora solo mostramos un mensaje de prueba
    messages.success(request, f"Etiqueta para {marca} {modelo} ({serial}) enviada a la impresora.")
    return redirect(request.META.get('HTTP_REFERER', '/'))