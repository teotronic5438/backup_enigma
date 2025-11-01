from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import ConfiguracionImpresora
import win32print
from django.views.decorators.http import require_POST

@login_required
@require_POST
def imprimir_etiqueta(request):
    """
    Función para imprimir etiquetas EPL en impresora Zebra TLP2844
    para etiquetas dobles de 2.5 x 5 cm
    """
    
    # 1. Obtener datos del POST
    modelo = request.POST.get("modelo", "").strip()
    marca = request.POST.get("marca", "").strip()
    serial = request.POST.get("serial", "").strip()

    print("=== FUNCIÓN imprimir_etiqueta ===")
    print(f"Modelo: {modelo}, Marca: {marca}, Serial: {serial}")

    # 2. Validar campos obligatorios
    if not serial:
        messages.error(request, "❌ No se puede imprimir: el campo SERIAL está vacío.")
        return redirect(request.META.get('HTTP_REFERER', '/'))

    # 3. Obtener configuración de impresora
    config = ConfiguracionImpresora.objects.first()
    if not config:
        messages.error(request, "❌ No hay una impresora configurada.")
        return redirect(request.META.get('HTTP_REFERER', '/'))

    nombre_impresora = config.nombre
    print(f"Impresora seleccionada: {nombre_impresora}")

    # 4. Construir contenido EPL optimizado para 2.5x5cm
    contenido_epl = generar_codigo_epl(marca, modelo, serial)
    
    print("Código EPL generado:")
    print(contenido_epl)

    # # 5. Enviar a la impresora
    # try:
    #     hPrinter = win32print.OpenPrinter(nombre_impresora)
        
    #     hJob = win32print.StartDocPrinter(hPrinter, 1, ("Etiqueta EPL", None, "RAW"))
    #     win32print.StartPagePrinter(hPrinter)

    #     # Enviar comando EPL
    #     win32print.WritePrinter(hPrinter, contenido_epl.encode('utf-8'))

    #     win32print.EndPagePrinter(hPrinter)
    #     win32print.EndDocPrinter(hPrinter)
    #     win32print.ClosePrinter(hPrinter)

    #     messages.success(request, f"🖨 Etiqueta enviada correctamente a {nombre_impresora}.")
        
    # except Exception as e:
    #     print(f"Error al imprimir: {e}")
    #     messages.error(request, f"❌ Error al imprimir: {str(e)}")


    # 5. Enviar a la impresora
    try:
        print(f"🔧 Intentando conectar con: {nombre_impresora}")
        hPrinter = win32print.OpenPrinter(nombre_impresora)
        print("✅ Conexión exitosa a la impresora")
        
        # Obtener información de la impresora
        printer_info = win32print.GetPrinter(hPrinter, 2)
        print(f"📋 Estado impresora: {printer_info['Status']}")
        print(f"📊 Tipo: {printer_info['pDriverName']}")
        
        # Iniciar trabajo de impresión
        hJob = win32print.StartDocPrinter(hPrinter, 1, ("Etiqueta EPL", None, "RAW"))
        win32print.StartPagePrinter(hPrinter)

        # Convertir a bytes y enviar
        epl_bytes = contenido_epl.encode('utf-8')
        print(f"📦 Enviando {len(epl_bytes)} bytes a la impresora...")
        
        bytes_written = win32print.WritePrinter(hPrinter, epl_bytes)
        print(f"✅ Bytes escritos: {bytes_written}")

        win32print.EndPagePrinter(hPrinter)
        win32print.EndDocPrinter(hPrinter)
        win32print.ClosePrinter(hPrinter)

        messages.success(request, f"🖨 Etiqueta enviada correctamente a {nombre_impresora}.")
        
    except Exception as e:
        print(f"❌ Error detallado al imprimir: {str(e)}")
        print(f"🔍 Tipo de error: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        messages.error(request, f"❌ Error al imprimir: {str(e)}")

    return redirect(request.META.get('HTTP_REFERER', '/'))


# def generar_codigo_epl(marca, modelo, serial):
#     """
#     Genera código EPL2 para impresora Zebra TLP2844
#     Etiqueta doble de 2.5cm x 5cm (aproximadamente 100x200 puntos)
#     """
    
#     # Limitar longitud de textos para que quepan en la etiqueta pequeña
#     marca = marca[:12]  # Máximo 12 caracteres
#     modelo = modelo[:10]  # Máximo 10 caracteres
#     serial = serial[:15]  # Máximo 15 caracteres para código de barras
    
#     # Configuración EPL2 para etiqueta doble
#     epl_commands = []
    
#     # Comando de inicialización
#     epl_commands.append("N")  # Limpiar buffer
    
#     # PRIMERA ETIQUETA (superior)
#     # Texto - Marca
#     epl_commands.append(f'A10,10,0,2,1,1,N,"{marca}"')
    
#     # Texto - Modelo  
#     epl_commands.append(f'A10,30,0,2,1,1,N,"{modelo}"')
    
#     # Texto - Serial
#     epl_commands.append(f'A10,50,0,2,1,1,N,"{serial}"')
    
#     # Código de barras Code 128 (más compacto)
#     epl_commands.append(f'B10,70,0,1,2,2,40,N,"{serial}"')
    
#     # SEGUNDA ETIQUETA (inferior) - A 100 puntos de distancia
#     # Texto - Marca
#     epl_commands.append(f'A10,110,0,2,1,1,N,"{marca}"')
    
#     # Texto - Modelo
#     epl_commands.append(f'A10,130,0,2,1,1,N,"{modelo}"')
    
#     # Texto - Serial
#     epl_commands.append(f'A10,150,0,2,1,1,N,"{serial}"')
    
#     # Código de barras Code 128
#     epl_commands.append(f'B10,170,0,1,2,2,40,N,"{serial}"')
    
#     # Comando de impresión (1 copia)
#     epl_commands.append("P1")
    
#     return "\n".join(epl_commands)


def generar_codigo_epl(marca, modelo, serial):
    """
    Genera código EPL2 para impresora Zebra TLP2844
    Versión más básica y compatible
    """
    
    # Limitar longitud de textos
    marca = marca[:12]
    modelo = modelo[:10] 
    serial = serial[:15]
    
    # Comandos EPL más básicos y estándar
    epl_commands = []
    
    # Reset e inicialización
    epl_commands.append("\n")  # Línea en blanco inicial
    epl_commands.append("N")   # Clear image buffer
    epl_commands.append("q812")  # Set width (2.5cm ≈ 98 dots, pero usamos 609 para TLP2844)
    epl_commands.append("Q203")  # Set length (5cm ≈ 203 dots) + 1 para gap
    epl_commands.append("S2")  # Set media sensing to gap
    
    # PRIMERA ETIQUETA
    # Texto - Marca (posición más conservadora)
    epl_commands.append(f'A20,20,0,3,1,1,N,"{marca}"')
    
    # Texto - Modelo  
    epl_commands.append(f'A20,45,0,3,1,1,N,"{modelo}"')
    
    # Texto - Serial
    epl_commands.append(f'A20,70,0,3,1,1,N,"S:{serial}"')
    
    # Código de barras Code 128 - más estándar
    epl_commands.append(f'B20,95,0,3,3,6,50,B,"{serial}"')
    
    # SEGUNDA ETIQUETA (offset de 150 puntos)
    epl_commands.append(f'A20,170,0,3,1,1,N,"{marca}"')
    epl_commands.append(f'A20,195,0,3,1,1,N,"{modelo}"')
    epl_commands.append(f'A20,220,0,3,1,1,N,"S:{serial}"')
    epl_commands.append(f'B20,245,0,3,3,6,50,B,"{serial}"')
    
    # Imprimir
    epl_commands.append("P1")  # Print 1 copy
    
    return "\n".join(epl_commands)


# Mantener tu vista de configuración existente
@login_required(login_url='usuarios:login')
def configuracion_impresora(request):
    impresoras = [p[2] for p in win32print.EnumPrinters(2)]
    actual = ConfiguracionImpresora.objects.first()

    if request.method == "POST":
        seleccion = request.POST.get("impresora")
        verificar = request.POST.get("verificar")

        if verificar and seleccion:
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