from django.contrib import admin
from .models import Sale, SaleItem

class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 0

class SaleAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "total_amount")
    inlines = [SaleItemInline]

admin.site.register(Sale, SaleAdmin)
