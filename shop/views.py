import sweetify
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View, generic

from shop.forms import NewUserForm, ManufacturerSearchForm, AutopartsSearchForm
from shop.models import Manufacturer, AutoPart, Customer, Order


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

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name", "")

        context["manufacturer_search_form"] = ManufacturerSearchForm(initial={
            "name": name
        })

        return context

    def get_queryset(self):
        form = ManufacturerSearchForm(self.request.GET)

        if form.is_valid():
            return self.queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )
        return self.queryset


class AutopartListView(generic.ListView):
    model = AutoPart
    context_object_name = "autoparts_list"
    template_name = "shop/autoparts_list.html"
    queryset = AutoPart.objects.all()
    paginate_by = 9

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        part_name = self.request.GET.get("part_name", "")

        context["autoparts_search_form"] = AutopartsSearchForm(initial={
            "part_name": part_name
        })

        return context

    def get_queryset(self):
        form = AutopartsSearchForm(self.request.GET)

        if form.is_valid():
            return self.queryset.filter(
                part_name__icontains=form.cleaned_data["part_name"]
            )
        return self.queryset


def add_item_to_order(request, pk):
    if request.user.is_authenticated:
        customer = Customer.objects.get(id=request.user.id)
        part = AutoPart.objects.get(id=pk)

        order, created = Order.objects.get_or_create(owner_id=customer.id)
        order.auto_parts.add(part)
    else:
        sweetify.warning(
            request,
            "Sorry",
            text="You must be signed in",
            persistent="Ok"
        )
        return redirect(reverse_lazy("shop:autopart-list"))

    return redirect(reverse_lazy("shop:autopart-list"))

