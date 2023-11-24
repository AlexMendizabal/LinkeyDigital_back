from django.contrib import admin
from pay.models.transaction import Discount, SavedDiscounts

admin.site.register(Discount)
# Register your models here.

admin.site.register(SavedDiscounts)