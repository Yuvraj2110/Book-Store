# books/models.py
from django.db import models
from django.db.models import Sum

class Author(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Publisher(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    website = models.URLField(blank=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=400, db_index=True)
    authors = models.ManyToManyField(Author, related_name='books')
    publisher = models.ForeignKey(Publisher, on_delete=models.SET_NULL, null=True, blank=True, related_name='books')
    categories = models.ManyToManyField(Category, blank=True, related_name='books')
    isbn = models.CharField(max_length=20, unique=True, db_index=True)
    sku = models.CharField(max_length=64, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    reorder_level = models.IntegerField(default=5)
    cover = models.ImageField(upload_to='covers/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def stock(self):
        """Calculate live stock from StockMovement."""
        from inventory.models import StockMovement
        total = StockMovement.objects.filter(book=self).aggregate(
            Sum("quantity")
        )["quantity__sum"]
        return total or 0

    def is_low_stock(self):
        return self.stock <= (self.reorder_level or 0)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']
        indexes = [
            models.Index(fields=['isbn']),
            models.Index(fields=['title']),
        ]
