# apps/reportes/urls.py
from django.urls import path
from . import views

app_name = "reportes"

urlpatterns = [
    path('', views.ReporteDashboardView.as_view(), name='dashboard'),
    path('ingresos/', views.ReporteIngresosView.as_view(), name='ingresos'),
    path('ordenes/', views.ReporteOrdenesView.as_view(), name='ordenes'),
    path('exportar/', views.ExportIngresosView.as_view(), name='export_ingresos'),
    path('exportar-excel/', views.ExportIngresosExcelView.as_view(), name='export_ingresos_excel'),  # NUEVA
]
