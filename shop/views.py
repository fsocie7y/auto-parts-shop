import sweetify
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View, generic
from sweetify.views import SweetifySuccessMixin

from shop.forms import NewUserForm, ManufacturerSearchForm, AutopartsSearchForm
from shop.models import Manufacturer, AutoPart, Customer, Order


def index(request):
    """View function for the home page of the site."""
    manufacturer_count = Manufacturer.objects.all().count()
    autoparts_count = AutoPart.objects.all().count()
    users_count = Customer.objects.all().count()

    context = {
        "manufacturer_count": manufacturer_count,
        "autoparts_count": autoparts_count,
        "users_count": users_count,
    }
    return render(request, "shop/index.html", context=context)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return render(request, "registration/logged_out.html")


class SignUpView(SweetifySuccessMixin, generic.CreateView):
    template_name = "registration/register.html"
    success_url = reverse_lazy('shop:login')
    form_class = NewUserForm
    success_message = "Your profile was created successfully"


class CustomerDetailView(generic.DetailView):
    model = Customer


class CustomerUpdateView(SweetifySuccessMixin, generic.UpdateView):
    model = Customer
    fields = ["username", "first_name", "last_name", "email"]
    success_message = "Your profile was updated successfully"

    def get_success_url(self):
        return reverse_lazy(
            "shop:customer-detail", kwargs={"pk": self.object.pk}
        )


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


def manufacturer_detail_parts(request, pk):
    manufacturer = Manufacturer.objects.get(pk=pk)
    autoparts_list = manufacturer.autopart_set.all()

    context = {
        "autoparts_list": autoparts_list,
        "manufacturer": manufacturer,
    }

    return render(request, "shop/manufacturer_detail.html", context)


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
        sweetify.success(
            request,
            "Great",
            text="You successfully add part to order"
        )
    else:
        sweetify.warning(
            request,
            "Sorry",
            text="You must be signed in",
            persistent="Ok"
        )
        return redirect(reverse_lazy("shop:autopart-list"))

    return redirect(reverse_lazy("shop:autopart-list"))


def remove_part_from_order(request, pk):
    owner_id = request.user.id
    part = AutoPart.objects.get(pk=pk)
    order = Order.objects.get(owner_id=owner_id)
    order.auto_parts.remove(part)
    sweetify.success(
        request,
        "Great",
        text="You successfully remove part from order"
    )
    return redirect(reverse_lazy("shop:basket"))


def basket(request):
    if request.user.is_authenticated:
        owner_id = request.user.id
        order, created = Order.objects.get_or_create(owner_id=owner_id)
        summary_cost = sum([part.price for part in order.auto_parts.all()])
        context = {
            "order": order,
            "summary_cost": summary_cost
        }
        return render(request, "shop/basket.html", context=context)
    else:
        sweetify.warning(
            request,
            "Sorry",
            text="You must be signed in",
            persistent="Ok"
        )
        return redirect(reverse_lazy("shop:login"))
