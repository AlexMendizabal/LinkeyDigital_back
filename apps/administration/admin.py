from django.contrib import admin
from .models.currencies import Currencies
from .models.customer import Customer
from .models.customer_subscription import CustomerSubscription
from .models.customer_type import CustomerType
from .models.customer_user_devices import CustomerUserDevices
from .models.devices import Devices
from .models.discount import Discount
from .models.licencia import Licencia
from .models.subscription import Subscription

admin.site.register(Currencies)
admin.site.register(Customer)
admin.site.register(CustomerSubscription)
admin.site.register(CustomerType)
admin.site.register(CustomerUserDevices)
admin.site.register(Devices)
admin.site.register(Discount)
admin.site.register(Licencia)
admin.site.register(Subscription)
