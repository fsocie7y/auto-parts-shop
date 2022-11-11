from django.contrib.auth import logout
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView

from shop.forms import NewUserForm


def index(request):
    """View function for the home page of the site."""
    return render(request, "shop/index.html")


class LogoutView(View):
    def get(self, request):
        logout(request)
        return render(request, "registration/logged_out.html")


class SignUpView(SuccessMessageMixin, CreateView):
    template_name = "registration/register.html"
    success_url = reverse_lazy('shop:login')
    form_class = NewUserForm
    success_message = "Your profile was created successfully"

    def get_context_data(self, **kwargs):
        context = super(SignUpView, self).get_context_data(**kwargs)
        context["success_message"] = self.success_message

        return context
