
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Product

User = get_user_model()


class SignupForm(UserCreationForm):
    email = forms.EmailField()
    organization_name = forms.CharField(max_length=150)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "organization_name",
            "password1",
            "password2",
        ]


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "name",
            "sku",
            "description",
            "quantity",
            "cost_price",
            "selling_price",
            "low_stock_threshold",
        ]
        widgets = {
        "name": forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Enter product name",
        }),
        "sku": forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Enter unique SKU",
        }),
        "description": forms.Textarea(attrs={
            "class": "form-control",
            "rows": 3,
            "placeholder": "Enter product description",
        }),
        "quantity": forms.NumberInput(attrs={
            "class": "form-control",
            "min": 0,
        }),
        "cost_price": forms.NumberInput(attrs={
            "class": "form-control",
            "min": 0,
            "step": "0.01",
        }),
        "selling_price": forms.NumberInput(attrs={
            "class": "form-control",
            "min": 0,
            "step": "0.01",
        }),
        "low_stock_threshold": forms.NumberInput(attrs={
            "class": "form-control",
            "min": 0,
        }),
    }