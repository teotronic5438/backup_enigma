# from django.urls import path
# from .views import stock

# urlpatterns=[
#     path('stock/', stock, name="stock"),
#     # path('deposito/',stock_deposito, name="deposito"),
# ]

from django.urls import path
from .views import StockView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('stock/', login_required(StockView.as_view()), name="stock"),
    # path('deposito/', stock_deposito, name="deposito"),
]