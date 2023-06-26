import os

from rest_framework.generics import get_object_or_404

from profile.models import ViewProfile
from profile.models import CustomerUserProfile


class ViewsServices:
    def get_views(self, profile_id, month, year):
        userP = get_object_or_404(CustomerUserProfile, id=profile_id )
        view = ViewProfile.objects.filter(custom_user=userP.id, 
                                          timestamp__date__year=year, 
                                          timestamp__date__month=month)
        return view