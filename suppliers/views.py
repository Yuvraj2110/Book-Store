from django.shortcuts import render, redirect, get_object_or_404
from .models import Supplier, PurchaseOrder, PurchaseOrderItem
from .forms import SupplierForm, PurchaseOrderForm, PurchaseOrderItemForm
from inventory.models import StockMovement


# ---------------------------
#       SUPPLIERS
# ---------------------------
def supplier_list(request):
    suppliers = Supplier.objects.all()
    return render(request, "suppliers/supplier_list.html", {"suppliers": suppliers})


def supplier_add(request):
    if request.method == "POST":
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("supplier_list")
    else:
        form = SupplierForm()

    return render(request, "suppliers/supplier_add.html", {"form": form})


# ---------------------------
#   PURCHASE ORDERS (PO)
# ---------------------------
def po_list(request):
    pos = PurchaseOrder.objects.all().order_by("-created_at")
    return render(request, "suppliers/po_list.html", {"pos": pos})


def po_create(request):
    if request.method == "POST":
        form = PurchaseOrderForm(request.POST)
        if form.is_valid():
            po = form.save(commit=False)
            po.status = "draft"
            po.save()
            return redirect("po_detail", po.id)
    else:
        form = PurchaseOrderForm()

    return render(request, "suppliers/po_create.html", {"form": form})


def po_detail(request, po_id):
    po = get_object_or_404(PurchaseOrder, id=po_id)
    items = po.items.all()
    item_form = PurchaseOrderItemForm()

    if request.method == "POST":
        item_form = PurchaseOrderItemForm(request.POST)
        if item_form.is_valid():
            item = item_form.save(commit=False)
            item.po = po
            item.save()
            return redirect("po_detail", po.id)

    return render(request, "suppliers/po_detail.html", {
        "po": po,
        "items": items,
        "item_form": item_form
    })


def po_mark_ordered(request, po_id):
    po = get_object_or_404(PurchaseOrder, id=po_id)
    po.status = "ordered"
    po.save()
    return redirect("po_detail", po.id)


def po_mark_received(request, po_id):
    po = get_object_or_404(PurchaseOrder, id=po_id)
    po.status = "received"
    po.save()

    # ADD STOCK for each item
    for item in po.items.all():
        StockMovement.objects.create(
            book=item.book,
            quantity=item.qty,
            reason="purchase",
            source=f"PO#{po.id}",
            created_by=request.user,
        )

    return redirect("po_detail", po.id)

