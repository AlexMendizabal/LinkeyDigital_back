from apps.authentication.serializers import CustomerUserserializers
from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.authentication.models import CustomerUser
from rest_framework import status
from django.db import transaction
from apps.administration.UtilitiesAdministration import UtilitiesAdm
from apps.booking.services import Bookingservices
from django.core.paginator import Paginator
#from firebase_admin import auth


class CustomerUserserializersWithBooking(CustomerUserserializers):
    class Meta:
        model = CustomerUser
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        bookservices = Bookingservices()
        booking_data = {}
        for status in range(5):
            booking_data[status] = bookservices.get_bookings_count(customer_user=instance.id, status=status)
        representation['booking'] = booking_data

        return representation


class CustomerUserViewSet(APIView):
    def get(self, request):
        customer_user_serializers = CustomerUserserializersWithBooking(request.user)
        return Response(customer_user_serializers.data, status=status.HTTP_200_OK)

    def post(self, request):
        if request.user.is_superuser == 0:
            return Response({"status": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        serializers = CustomerUserserializers(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response({"status": "success", "data": serializers.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializers.errors}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        # si no se manda user por params... se usara el del user que lo solicite 
        customer_user = request.GET.get('user_id', request.user)
        try:
            with transaction.atomic():
                if isinstance(customer_user, int) or isinstance(customer_user, str):
                    customer_user = get_object_or_404(CustomerUser, id=customer_user)

                utilitiesAdm = UtilitiesAdm()
                if not utilitiesAdm.hasPermision(request.user, customer_user):
                    return Response({"success": False}, status=status.HTTP_401_UNAUTHORIZED)

                customer_user_serializers = CustomerUserserializers(instance=customer_user, data=request.data, partial=True)
                customer_user_serializers.is_valid(raise_exception=True)
                customer_user_serializers.save()

        except Exception as e:
            return Response({"status": False, "error" : str(e)}, status=status.HTTP_503_service_unavailable)

        return Response(customer_user_serializers.data, status=status.HTTP_200_OK)

    def delete(self, request):
        if not request.user.is_superuser:
            return Response({"status": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            customer_user_id = request.GET.get('user_id')
            userProfile = get_object_or_404(CustomerUser, id=customer_user_id)
            userProfile.delete()
        except Exception as e:
            return Response({'msg': 'error al borrar de db', 'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        return Response({'msg': 'done'}, status=status.HTTP_204_NO_CONTENT)

class CustomerUserListViewSet(APIView):
    def get(self, request):

        # Busca la licencia, si no existe regresa todos
        licencia_id = request.GET.get('licencia_id', None)
        # se pregunta si se quiere users con licencia o no... si no existe regresara todos 
        sin_licencia = request.GET.get('sin_licencia', None) 
        if isinstance(sin_licencia, str):
            sin_licencia = sin_licencia.lower() == 'true'
        # users que fueron "eliminados"
        is_active = request.GET.get('is_active', None)

        authservicess = Authservicess()
        users = authservicess.getUsers(is_active=is_active, sin_licencia = sin_licencia, licencia_id = licencia_id)

        # Paginacion
        page_number = request.GET.get('page', 1)
        items_per_page = 100
        paginator = Paginator(users, items_per_page)
        try:
            page = paginator.page(page_number)
        except Exception as e:
            print(e)
            return Response({"success": False, "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)        

        customer_user_serializers = CustomerUserserializersWithBooking(page, many=True)
        return Response( {"success": True, "data": customer_user_serializers.data, "pages": paginator.num_pages}, status=status.HTTP_200_OK)

class CustomerAdminViewSet(APIView):
    def put(self, request, customer_id):

        customer_user = get_object_or_404(CustomerUser, id=customer_id)

        utilitiesAdm = UtilitiesAdm()
        if not utilitiesAdm.hasPermision(request.user, customer_user ):
            return Response({"success": False}, status=status.HTTP_401_UNAUTHORIZED)
        
        customer_user_serializers = CustomerUserserializers(instance=customer_user, data=request.data, partial=True)
        customer_user_serializers.is_valid(raise_exception=True)
        customer_user_serializers.save()
        return Response(customer_user_serializers.data, status=status.HTTP_200_OK)


class CustomerUserPutRubroViewSet(APIView):
    
    """ WAITING: ID Se debe poner la funcion de filtrar ids """
    def put(self, request):
        if not request.user.is_superuser and not request.user.is_admin:
            return Response({"status": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        
        if not "ids" in request.data and len(request.data["ids"]) > 0:
            return Response({"status": False}, status=status.HTTP_400_BAD_REQUEST)
        ids_get = request.data["ids"]
        with transaction.atomic():
            ids = list( set(ids_get) )
            for reg in ids:
                try:
                    customer_user = get_object_or_404(CustomerUser, id=reg)
                    utilitiesAdm = UtilitiesAdm()
                    if not request.user.is_superuser:
                        if not utilitiesAdm.is_from_same_license(request.user, customer_user ):
                                return Response({"success": False,"mensaje": "uno de los ids no pertenece a la licencia "}, status=status.HTTP_401_UNAUTHORIZED)
                    
                    customer_user.rubro = request.data["rubro"]
                    customer_user_serializers = CustomerUserserializers(instance=customer_user, data=request.data, partial=True)
                    customer_user_serializers.is_valid(raise_exception=True)
                    customer_user_serializers.save()
                except Exception as e:
                    return Response({"success": False}, status=status.HTTP_503_services_UNAVAILABLE)
        return Response({"success": True}, status=status.HTTP_200_OK)

        

        


