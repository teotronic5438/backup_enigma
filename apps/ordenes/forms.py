# forms.py
from .models import Equipos
from django import forms
from .models import Ordenes

class EquipoForm(forms.ModelForm):
    class Meta:
        model = Equipos
        fields = ['numero_serie', 'observaciones']


class OrdenForm(forms.ModelForm):
    FALLAS_CHOICES = [
        ("Falla Panel - Sin Imagen", "Falla Panel - Sin Imagen"),
        ("Falla Panel - Problema de Imagen", "Falla Panel - Problema de Imagen"),
        ("Panel Roto", "Panel Roto"),
        ("Falla SSB - No Enciende", "Falla SSB - No Enciende"),
        ("Falla SSB - TV Bloqueado", "Falla SSB - TV Bloqueado"),
        ("Falla SSB - Sonido", "Falla SSB - Sonido"),
        ("Falla SSB - Sin Imagen", "Falla SSB - Sin Imagen"),
        ("Falla PSU - No Enciende", "Falla PSU - No Enciende"),
        ("Falla PSU - Problema Backlight", "Falla PSU - Problema Backlight"),
        ("Actualizacion SW - Por Falla", "Actualizacion SW - Por Falla"),
        ("Falla IR", "Falla IR"),
        ("Falla Modulo WiFi (PLACA)", "Falla Modulo WiFi (PLACA)"),
        ("Falla Teclado", "Falla Teclado"),
        ("Falla Cable LVDS - Se Bloquea", "Falla Cable LVDS - Se Bloquea"),
        ("Falla Cable LVDS - Sin Imagen", "Falla Cable LVDS - Sin Imagen"),
        ("No Presenta Defecto", "No Presenta Defecto"),
        ("Cable SSB - Modulo WiFi", "Cable SSB - Modulo WiFi"),
        ("Falla Panel - Tiras de Led sin Lente", "Falla Panel - Tiras de Led sin Lente"),
    ]

    REPARACIONES_CHOICES = [
        ("Irreparable", "Irreparable"),
        ("Cambio de SSB", "Cambio de SSB"),
        ("Cambio de PSU", "Cambio de PSU"),
        ("Upgrade Software", "Upgrade Software"),
        ("Cambio Ir Board", "Cambio Ir Board"),
        ("Cambio NetBoard", "Cambio NetBoard"),
        ("Cambio Keyboard", "Cambio Keyboard"),
        ("Cambio LVDS", "Cambio LVDS"),
        ("No verifica Falla", "No verifica Falla"),
        ("Cambio cables flat", "Cambio cables flat"),
    ]

    falla_detectada = forms.ChoiceField(
        choices=FALLAS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False
    )

    reparacion = forms.ChoiceField(
        choices=REPARACIONES_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False
    )

    class Meta:
        model = Ordenes
        fields = ['falla_detectada', 'reparacion', 'destino']