# inventory/signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import StockMovement

@receiver(post_save, sender=StockMovement)
def apply_stock_movement(sender, instance, created, **kwargs):
    """
    Stock is calculated from StockMovement records (Book.stock property).
    No need to update Book.stock field — do NOT call any adjust_stock here.
    Keep this handler for future side-effects (notifications / caching / logs).
    """
    # Example: future hook place (currently intentionally empty)
    # if created:
    #     do_something_async_or_log(instance)
    return None


@receiver(post_delete, sender=StockMovement)
def remove_stock_movement(sender, instance, **kwargs):
    """
    If a movement is deleted we don't need to mutate Book state;
    Book.stock is calculated live. Keep handler for future cleanup if needed.
    """
    return None
