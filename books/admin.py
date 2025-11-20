from django.contrib import admin
from .models import Book, Author, Category, Publisher

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title','isbn','price','stock','reorder_level','publisher')
    search_fields = ('title','isbn')
    list_filter = ('publisher','categories')
    filter_horizontal = ('authors','categories')

admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Publisher)
