from django.db import models

# Create your models here.

from django.conf import settings
from django.db import models
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction

from .models import Organization, Product
from .forms import ProductForm


@login_required
def add_product(request):
    organization, created = Organization.objects.get_or_create(
        owner=request.user,
        defaults={
            "name": f"{request.user.username}'s Organization"
        },
    )

    if request.method == "POST":
        form = ProductForm(request.POST)

        if form.is_valid():
            try:
                with transaction.atomic():
                    product = form.save(commit=False)
                    product.organization = organization
                    product.save()

                messages.success(request, "Product added successfully!")
                return redirect("dashboard")

            except IntegrityError:
                form.add_error(
                    "sku",
                    "This SKU already exists in your organization."
                )
    else:
        form = ProductForm()

    return render(
        request,
        "inventory/add_product.html",
        {"form": form},
    )
@login_required
def add_product(request):
    organization, created = Organization.objects.get_or_create(
        owner=request.user,
        defaults={
            "name": f"{request.user.username}'s Organization"
        },
    )

    if request.method == "POST":
        form = ProductForm(request.POST)

        if form.is_valid():
            try:
                with transaction.atomic():
                    product = form.save(commit=False)
                    product.organization = organization
                    product.save()

                messages.success(request, "Product added successfully!")
                return redirect("dashboard")

            except IntegrityError:
                form.add_error(
                    "sku",
                    "This SKU already exists in your organization."
                )
    else:
        form = ProductForm()

    return render(
        request,
        "inventory/add_product.html",
        {"form": form},
    )

from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render
from .models import Organization, Product


@login_required
def dashboard(request):
    organization = Organization.objects.filter(
        owner=request.user
    ).first()

    products = Product.objects.filter(
        organization=organization
    ) if organization else Product.objects.none()

    total_stock = products.aggregate(
        total=Sum("quantity")
    )["total"] or 0

    context = {
        "products": products,
        "total_stock": total_stock,
    }

    return render(request, "inventory/dashboard.html", context)

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully. Please log in.")
            return redirect("login")
    else:
        form = UserCreationForm()

    return render(request, "inventory/signup.html", {"form": form})

from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(
                request,
                "Invalid username or password. Please try again."
            )

    return render(request, "inventory/login.html")

from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect("login")

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Organization, Product

@login_required
def product_list(request):
    organization = Organization.objects.filter(
        owner=request.user
    ).first()

    if organization:
        products = Product.objects.filter(
            organization=organization
        ).order_by("-created_at")
    else:
        products = Product.objects.none()

    return render(
        request,
        "inventory/product_list.html",
        {"products": products},
    )

@login_required
def product_create(request):
    organization, created = Organization.objects.get_or_create(
        owner=request.user,
        defaults={
            "name": f"{request.user.username}'s Organization"
        },
    )

    if request.method == "POST":
        form = ProductForm(request.POST)

        if form.is_valid():
            try:
                with transaction.atomic():
                    product = form.save(commit=False)
                    product.organization = organization
                    product.save()

                messages.success(request, "Product added successfully!")
                return redirect("product_list")

            except IntegrityError:
                form.add_error(
                    "sku",
                    "This SKU already exists in your organization."
                )
    else:
        form = ProductForm()

    return render(
        request,
        "inventory/add_product.html",
        {"form": form},
    )

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Organization, Product
from .forms import ProductForm


@login_required
def product_edit(request, product_id):
    organization = get_object_or_404(
        Organization,
        owner=request.user
    )

    product = get_object_or_404(
        Product,
        id=product_id,
        organization=organization
    )

    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)

        if form.is_valid():
            form.save()
            return redirect("product_list")
    else:
        form = ProductForm(instance=product)

    return render(
        request,
        "inventory/product_edit.html",
        {"form": form, "product": product}
    )

@login_required
def product_delete(request, product_id):
    organization = get_object_or_404(
        Organization,
        owner=request.user
    )

    product = get_object_or_404(
        Product,
        id=product_id,
        organization=organization
    )

    if request.method == "POST":
        product.delete()
        return redirect("product_list")

    return render(
        request,
        "inventory/product_confirm_delete.html",
        {"product": product}
    )

@login_required
def settings_view(request):
    organization = get_object_or_404(
        Organization,
        owner=request.user
    )

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        threshold = request.POST.get("default_low_stock_threshold", "").strip()

        if not name:
            messages.error(request, "Organization name is required.")
        elif not threshold.isdigit():
            messages.error(request, "Enter a valid stock threshold.")
        else:
            organization.name = name
            organization.default_low_stock_threshold = int(threshold)
            organization.save()
            messages.success(request, "Settings updated successfully.")
            return redirect("settings")

    return render(
        request,
        "inventory/settings.html",
        {"organization": organization}
    )