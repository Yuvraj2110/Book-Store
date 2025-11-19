from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from books.models import Book
from inventory.models import StockMovement
from accounts.models import CustomerProfile
from .models import Sale, SaleItem


# -----------------------------
# MAIN SALES PAGE (POS)
# -----------------------------
def sales(request):
    cart = request.session.get("cart", {})
    cart_items = []
    total = 0

    for book_id, qty in cart.items():
        book = Book.objects.get(id=book_id)
        subtotal = book.price * qty
        total += subtotal
        cart_items.append({
            "book": book,
            "qty": qty,
            "subtotal": subtotal
        })

    books = Book.objects.all()

    return render(request, "sales/sales.html", {
        "cart": cart_items,
        "total": total,
        "books": books,
    })


# -----------------------------
# ADD BOOK TO CART
# -----------------------------
def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if book.stock <= 0:
        messages.error(request, f"'{book.title}' is OUT OF STOCK!")
        return redirect("sales")

    cart = request.session.get("cart", {})
    current_qty = cart.get(str(book_id), 0)
    new_qty = current_qty + 1

    if new_qty > book.stock:
        messages.error(request, f"Only {book.stock} left in stock!")
        return redirect("sales")

    cart[str(book_id)] = new_qty
    request.session["cart"] = cart

    messages.success(request, f"Added '{book.title}' to cart (x{new_qty})")
    return redirect("sales")


# -----------------------------
# REMOVE FROM CART
# -----------------------------
def remove_from_cart(request, book_id):
    cart = request.session.get("cart", {})
    if str(book_id) in cart:
        del cart[str(book_id)]
    request.session["cart"] = cart
    return redirect("sales")


# -----------------------------
# CHECKOUT
# -----------------------------
def checkout(request):
    cart = request.session.get("cart", {})

    if not cart:
        return redirect("sales")

    customers = CustomerProfile.objects.all()

    if request.method == "POST":
        customer_id = request.POST.get("customer_id")
        customer_name = request.POST.get("customer_name").strip()
        customer_phone = request.POST.get("customer_phone").strip()

        # Existing Customer
        if customer_id:
            customer = CustomerProfile.objects.get(id=customer_id)

        # New Customer
        else:
            customer = CustomerProfile.objects.create(
                name=customer_name,
                phone=customer_phone,
                loyalty_points=0
            )

        # Create sale
        sale = Sale.objects.create(
            customer_name=customer.name,
            customer_phone=customer.phone
        )

        total = 0

        for book_id, qty in cart.items():
            book = Book.objects.get(id=book_id)

            # Prevent overselling
            if qty > book.stock:
                messages.error(request, f"Only {book.stock} available for '{book.title}'.")
                return redirect("sales")

            SaleItem.objects.create(
                sale=sale,
                book=book,
                qty=qty,
                price=book.price,
            )

            total += book.price * qty

            StockMovement.objects.create(
                book=book,
                quantity=-qty,
                reason="sale",
                source=f"Sale #{sale.id}",
                created_by=request.user
            )

        sale.total_amount = total
        sale.save()

        request.session["cart"] = {}
        return redirect("sale_detail", sale.id)

    return render(request, "sales/checkout.html", {
        "customers": customers
    })


# -----------------------------
# SALES HISTORY
# -----------------------------
def sales_list(request):
    sales = Sale.objects.all().order_by("-created_at")
    return render(request, "sales/sales_list.html", {"sales": sales})


# -----------------------------
# SALE DETAIL
# -----------------------------
def sale_detail(request, sale_id):
    sale = get_object_or_404(Sale, id=sale_id)
    return render(request, "sales/sale_detail.html", {"sale": sale})
