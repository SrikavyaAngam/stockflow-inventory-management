
from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("products/", views.product_list, name="product_list"),
    path("products/add/", views.product_create, name="product_create"),
    path("products/<int:pk>/edit/", views.product_edit, name="product_edit"),
    path("products/<int:pk>/delete/", views.product_delete, name="product_delete"),
    path("settings/", views.settings_view, name="settings"),
    path('add-product/', views.add_product, name='add_product'),
]
