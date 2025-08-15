from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .form import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomerUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomerUser
    list_display = ["email", "username", "is_superuser", "is_admin", "is_staff", "is_sales_manager"]
    fieldsets = UserAdmin.fieldsets + (
        ("Permisos adicionales", {"fields": ("is_admin", "is_sales_manager", "is_sponsor", 
                                         "is_booking", "is_ecommerce")}),
    )
    list_filter = ["is_superuser", "is_admin", "is_staff", "is_sales_manager"]


admin.site.register(CustomerUser, CustomUserAdmin)
