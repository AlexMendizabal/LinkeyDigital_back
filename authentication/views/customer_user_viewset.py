from rest_framework import viewsets, serializers
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.models import CustomerUser
from rest_framework import status
from django.db import transaction
from administration.UtilitiesAdministration import UtilitiesAdm
from booking.services import BookingService
from firebase_admin import auth

class CustomerUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerUser
        fields = '__all__'

class CustomerUserSerializerWithBooking(CustomerUserSerializer):
    class Meta:
        model = CustomerUser
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        bookservice = BookingService()
        booking_data = {}
        for status in range(5):
            booking_data[status] = bookservice.get_bookings_count(customer_user=instance.id, status=status)
        representation['booking'] = booking_data

        return representation


class CustomerUserViewSet(APIView):
    def get(self, request):
        customer_user_serializer = CustomerUserSerializerWithBooking(request.user)
        return Response(customer_user_serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if request.user.is_superuser == 0:
            return Response({"status": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = CustomerUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        customer_user = request.GET.get('user_id', request.user)
        #pregunta user es numerico, si lo es busca al user, si no lo es significa que ya lo tiene
        try:
            if isinstance(customer_user, int) or isinstance(customer_user, str):
                customer_user = get_object_or_404(CustomerUser, id=customer_user)

            utilitiesAdm = UtilitiesAdm()
            if not utilitiesAdm.hasPermision(request.user, customer_user):
                return Response({"success": False}, status=status.HTTP_401_UNAUTHORIZED)
            
            customer_user_serializers = CustomerUserSerializer(instance=customer_user, data=request.data, partial=True)
            customer_user_serializers.is_valid(raise_exception=True)
            customer_user_serializers.save()
        except Exception as e:
            return Response({"status": False, "error" : str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        
        return Response(customer_user_serializers.data, status=status.HTTP_200_OK)

    def delete(self, request):
        #return Response({"status": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        if not request.user.is_superuser:
            return Response({"status": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            customer_user = request.GET.get('user_id')
            userProfile = get_object_or_404(CustomerUser, id=customer_user)
            uid = userProfile.uid
            userProfile.delete()
        except:
            return Response({'msg': 'error al borrar de db'}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            auth.delete_user(uid)
        except:
            return Response({'msg': 'error al borrar de firebase'}, status=status.HTTP_404_NOT_FOUND)
        
        return Response({'msg': 'done'}, status=status.HTTP_204_NO_CONTENT)

class CustomerAdminViewSet(APIView):
    def put(self, request, customer_id):

        customer_user = get_object_or_404(CustomerUser, id=customer_id)

        utilitiesAdm = UtilitiesAdm()
        if not utilitiesAdm.hasPermision(request.user, customer_user ):
            return Response({"success": False}, status=status.HTTP_401_UNAUTHORIZED)
        
        customer_user_serializers = CustomerUserSerializer(instance=customer_user, data=request.data, partial=True)
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
                    customer_user_serializers = CustomerUserSerializer(instance=customer_user, data=request.data, partial=True)
                    customer_user_serializers.is_valid(raise_exception=True)
                    customer_user_serializers.save()
                except Exception as e:
                    return Response({"success": False}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        return Response({"success": True}, status=status.HTTP_200_OK)

        

        


