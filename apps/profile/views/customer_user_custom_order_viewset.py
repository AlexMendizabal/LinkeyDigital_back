from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404

from rest_framework.response import Response
from rest_framework import status

from apps.profile.services import SocialMediaservices

from apps.administration.UtilitiesAdministration import UtilitiesAdm

class customer_user_custom_order_viewset(APIView):
    

# {
# 1:123,
# 2:124,
# 3:125,
# }

    def put(self, request):

        cusm_services = SocialMediaservices()
        ids = request.data.get('ids', {})

        if not ids or ids == {}:
            return Response({"success": False}, status=status.HTTP_400_BAD_REQUEST)
        
        first_id = next(iter(ids.values()))
        customer_user_custom_social_media = cusm_services.get_custom_social_media(pk=first_id)
        utilitiesAdm = UtilitiesAdm()

        if not utilitiesAdm.hasPermision(request.user, customer_user_custom_social_media.customer_user ):
            return Response({"success": False}, status=status.HTTP_401_UNAUTHORIZED)

        user = customer_user_custom_social_media.customer_user.id
        for key, value in ids.items():
            res = cusm_services.update_order_social_media(value, key, user)

        return Response({"success": True}, status=status.HTTP_200_OK)
            
            


            



