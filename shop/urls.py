from django.urls import path
from django.contrib.auth.views import LoginView
from shop.views import (
    index,
    LogoutView,
    SignUpView,
    ManufacturerListView,
    AutopartListView,
    add_item_to_order,
    basket,
)

urlpatterns = [
    path("", index, name="index"),
    path("login/home/", index, name="index"),
    path(
        "login/",
        LoginView.as_view(
           template_name='registration/login.html',
           redirect_authenticated_user=True),
        name='login'
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
]

app_name = "shop"
