from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from books.models import Book
from .models import StockMovement
from django.utils import timezone


# ------------------------------
# STOCK SUMMARY (NEW MAIN PAGE)
# ------------------------------
def stock_summary(request):
    books = Book.objects.all()
    summary = []

    for book in books:
        current = book.stock
        if current < 0:
            current = 0  # clamp negative → 0

        summary.append({
            "book": book,
            "stock": current,
            "reorder": book.reorder_level,
            "low": current <= book.reorder_level,
        })

    return render(request, "inventory/stock_summary.html", {"summary": summary})



# ------------------------------
# STOCK MOVEMENTS (LOG PAGE)
# ------------------------------
def stock_movements(request):
    movements = StockMovement.objects.all().order_by("-created_at")

    return render(request, "inventory/stock_movements.html", {
        "movements": movements
    })


# ------------------------------
# ADD STOCK MOVEMENT (FORM)
# ------------------------------
def add_stock_movement(request):
    books = Book.objects.all()

    if request.method == "POST":
        book_id = request.POST.get("book")
        qty = int(request.POST.get("quantity"))
        reason = request.POST.get("reason")
        source = request.POST.get("source")

        book = get_object_or_404(Book, id=book_id)

        StockMovement.objects.create(
            book=book,
            quantity=qty,
            reason=reason,
            source=source,
            created_by=request.user,
        )

        return redirect("stock_movements")

    return render(request, "inventory/add_stock_movement.html", {
        "books": books
    })
