
from django.contrib import admin
from .models.productos import Productos
from .models.transaction import Discount
from .models.transaction import Transaction
from .models.detalleTransaccion import DetalleTransaction

admin.site.register(Productos)
admin.site.register(Discount)
admin.site.register(Transaction)
admin.site.register(DetalleTransaction)
