from django.contrib.auth import logout
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View, generic

from shop.forms import NewUserForm
from shop.models import Manufacturer, AutoPart


def index(request):
    """View function for the home page of the site."""
    return render(request, "shop/index.html")


class LogoutView(View):
    def get(self, request):
        logout(request)
        return render(request, "registration/logged_out.html")


class SignUpView(SuccessMessageMixin, generic.CreateView):
    template_name = "registration/register.html"
    success_url = reverse_lazy('shop:login')
    form_class = NewUserForm
    success_message = "Your profile was created successfully"

    def get_context_data(self, **kwargs):
        context = super(SignUpView, self).get_context_data(**kwargs)
        context["success_message"] = self.success_message

        return context


class ManufacturerListView(generic.ListView):
    model = Manufacturer
    context_object_name = "manufacturer_list"
    template_name = "shop/manufacturer_list.html"
    queryset = Manufacturer.objects.all()
    paginate_by = 10


class AutopartListView(generic.ListView):
    model = AutoPart
    context_object_name = "autoparts_list"
    template_name = "shop/autoparts_list.html"
    queryset = AutoPart.objects.all()
    paginate_by = 10
