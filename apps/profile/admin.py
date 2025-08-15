from django.contrib import admin
from .models.customer_user_custom_image import CustomerUserCustomImage
from .models.customer_user_custom_social_media import CustomerUserCustomSocialMedia
from .models.customer_user_email import CustomerUserEmail
from .models.customer_user_map import CustomerUserMap
from .models.customer_user_phonenumber import CustomerUserPhone
from .models.customer_user_profile import CustomerUserProfile
from .models.customer_user_reserva import CustomerUserReserva
from .models.customer_user_social_media import CustomerUserSocialMedia
from .models.customer_user_whatsapp import CustomerUserWhatsapp
from .models.design_profile import DesignProfile
from .models.social_media import SocialMedia
from .models.view_profile import ViewProfile

admin.site.register(CustomerUserCustomImage)
admin.site.register(CustomerUserCustomSocialMedia)
admin.site.register(CustomerUserEmail)
admin.site.register(CustomerUserMap)
admin.site.register(CustomerUserPhone)
admin.site.register(CustomerUserProfile)
admin.site.register(CustomerUserReserva)
admin.site.register(CustomerUserSocialMedia)
admin.site.register(CustomerUserWhatsapp)
admin.site.register(DesignProfile)
admin.site.register(SocialMedia)
admin.site.register(ViewProfile)
