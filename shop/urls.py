from django.urls import path
from django.contrib.auth.views import LoginView
from shop.views import (
    index,
    LogoutView,
    SignUpView,
    ManufacturerListView,
    AutopartListView,
    add_item_to_order,
    remove_part_from_order,
    basket,
    CustomerDetailView,
    CustomerUpdateView,
    manufacturer_detail_parts,
)

urlpatterns = [
    path("", index, name="index"),
    path("login/home/", index, name="index"),
    path(
        "login/",
        LoginView.as_view(
            template_name='registration/login.html',
            redirect_authenticated_user=True
        ),
        name="login"
    ),
    path("logout/", LogoutView.as_view(), name='logout'),
    path("register/", SignUpView.as_view(), name="register"),
    path(
        "manufacturers/",
        ManufacturerListView.as_view(),
        name="manufacturer-list",
    ),
    path(
        "auto-parts/",
        AutopartListView.as_view(),
        name="autopart-list",
    ),
    path("auto-parts/<int:pk>/buy/", add_item_to_order, name="buy"),
    path("basket/", basket, name="basket"),
    path(
        "customer/<int:pk>/",
        CustomerDetailView.as_view(),
        name="customer-detail"
    ),
    path(
        "customer/<int:pk>/update",
        CustomerUpdateView.as_view(),
        name="customer-update"
    ),
    path(
        "basket/<int:pk>/remove/",
        remove_part_from_order,
        name="remove"
    ),
    path(
        "manufacturer/<int:pk>/",
        manufacturer_detail_parts,
        name="manufacturer-detail"
    )
]

app_name = "shop"
