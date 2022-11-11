from django.urls import path
from django.contrib.auth.views import LoginView
from shop.views import index, LogoutView, SignUpView


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
]

app_name = "shop"
