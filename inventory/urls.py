from django.urls import path
from . import views

urlpatterns = [
    path("", views.stock_summary, name="stock_summary"),     
    path("movements/", views.stock_movements, name="stock_movements"),
    path("add/", views.add_stock_movement, name="add_stock_movement"),
]
