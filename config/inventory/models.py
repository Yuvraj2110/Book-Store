
from django.db import models
from django.utils import timezone
from django.conf import settings

from books.models import Book

class StockMovement(models.Model):
    REASON_CHOICES = [
        ('purchase', 'Purchase (in)'),
        ('sale', 'Sale (out)'),
        ('return', 'Customer return'),
        ('adjustment', 'Manual adjustment'),
        ('transfer', 'Transfer'),
    ]

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='stock_movements')
    quantity = models.IntegerField(help_text="Positive for incoming, negative for outgoing")
    reason = models.CharField(max_length=30, choices=REASON_CHOICES)
    source = models.CharField(max_length=200, blank=True, help_text="e.g. PO#123 or Order#456")
    note = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        sign = '+' if self.quantity >= 0 else ''
        return f"{self.book.title} {sign}{self.quantity} ({self.reason})"
