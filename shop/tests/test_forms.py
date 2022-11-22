from django.test import TestCase

from shop.forms import NewUserForm


class FormTests(TestCase):
    def test_user_creation_form(self):
        form_data = {
            "username": "testuser",
            "password1": "testqaz123",
            "password2": "testqaz123",
            "email": "testemail@email.com"
        }
        form = NewUserForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
        self.assertEqual(form.fields.keys(), form_data.keys())
