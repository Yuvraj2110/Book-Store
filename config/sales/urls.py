from django.urls import path
from . import views

urlpatterns = [
    path("", views.sales, name="sales"),  # main sales/POS page
    path("add/<int:book_id>/", views.add_to_cart, name="add_to_cart"),
    path("remove/<int:book_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("sales_history/", views.sales_list, name="sales_list"),
    path("sales/<int:sale_id>/", views.sale_detail, name="sale_detail"),
]
