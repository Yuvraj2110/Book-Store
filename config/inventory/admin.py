from django.contrib import admin
from .models import StockMovement

@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ('book','quantity','reason','source','created_at','created_by')
    list_filter = ('reason',)
    search_fields = ('book__title','source')
