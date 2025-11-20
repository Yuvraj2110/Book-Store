from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import CustomerProfile
from django.contrib.auth.decorators import login_required
from .models import CustomerProfile


def index(request):
    return render(request, "accounts/index.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "accounts/login.html")


def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        name = request.POST.get("name")
        phone = request.POST.get("phone")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("register")

        user = User.objects.create_user(username=username, password=password)
        CustomerProfile.objects.create(
            user=user,
            name=name,
            phone=phone
        )

        messages.success(request, "Account created successfully")
        return redirect("login")

    return render(request, "accounts/register.html")


def logout_view(request):
    logout(request)
    return redirect("home")


def profile_view(request):
    if not request.user.is_authenticated:
        return redirect("login")

    profile = request.user.customer_profile
    return render(request, "accounts/profile.html", {"profile": profile})



@login_required
def profile_view(request):
    customer, created = CustomerProfile.objects.get_or_create(
        user=request.user,
        defaults={
            "name": request.user.username,
            "email": request.user.email,
            "phone": "",
        }
    )

    return render(request, "accounts/profile.html", {
        "customer": customer
    })
