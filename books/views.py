from django.shortcuts import render, get_object_or_404
from .models import Book

def index(request):
    q = request.GET.get("q", "")
    books = Book.objects.all()

    if q:
        books = books.filter(title__icontains=q)

    return render(request, "books/index.html", {"books": books, "q": q})


def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, "books/detail.html", {"book": book})
