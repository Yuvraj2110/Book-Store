from django.contrib import admin
from .models import Supplier, PurchaseOrder, PurchaseOrderItem

admin.site.register(Supplier)

@admin.register(PurchaseOrder)
class POAdmin(admin.ModelAdmin):
    list_display = ('id','supplier','status','created_at')
    list_filter = ('status','supplier')
    inlines = []

admin.site.register(PurchaseOrderItem)
