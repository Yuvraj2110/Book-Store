from django.urls import path
from . import views

urlpatterns = [
    # Suppliers
    path("", views.supplier_list, name="supplier_list"),
    path("add/", views.supplier_add, name="supplier_add"),

    # Purchase Orders
    path("po/", views.po_list, name="po_list"),
    path("po/create/", views.po_create, name="po_create"),
    path("po/<int:po_id>/", views.po_detail, name="po_detail"),
    path("po/<int:po_id>/ordered/", views.po_mark_ordered, name="po_mark_ordered"),
    path("po/<int:po_id>/received/", views.po_mark_received, name="po_mark_received"),
]
