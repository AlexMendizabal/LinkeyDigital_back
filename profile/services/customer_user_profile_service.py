from rest_framework.generics import get_object_or_404

from profile.models import CustomerUserProfile


class ProfileService:
    def create_profile(self, dto):
        customer_user_profile, created = CustomerUserProfile.objects.update_or_create(
            customer_user=dto.customer_user)
        customer_user_profile.public_id = dto.public_id
        customer_user_profile.career = dto.career
        customer_user_profile.public_name = dto.public_name
        customer_user_profile.description = dto.description
        customer_user_profile.save()
        return customer_user_profile

    def get_profile(self, pk=None, customer_user=None):
        if pk and customer_user:
            customer_user_profile = get_object_or_404(CustomerUserProfile, pk=pk, customer_user=customer_user)
        elif customer_user:
            customer_user_profile = get_object_or_404(CustomerUserProfile, customer_user=customer_user)
        else:
            customer_user_profile = CustomerUserProfile.objects.all()
        return customer_user_profile
