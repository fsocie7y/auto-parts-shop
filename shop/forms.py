from django import forms
from django.contrib.auth.forms import UserCreationForm
from shop.models import Customer


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=False)

    class Meta:
        model = Customer
        fields = ("username", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class ManufacturerSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by name..."
            }
        )
    )


class AutopartsSearchForm(forms.Form):
    part_name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by name..."
            }
        )
    )
