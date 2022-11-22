from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from shop.models import Manufacturer, AutoPart, Customer

admin.site.register(Manufacturer)


@admin.register(AutoPart)
class AutoPartAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_filter = ("price",)


@admin.register(Customer)
class RedactorAdmin(UserAdmin):
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "first_name",
                        "last_name",
                    )
                },
            ),
        )
    )
