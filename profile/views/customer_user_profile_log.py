from django.shortcuts import render
from django.http import JsonResponse
from profile.models import ViewProfile

def view_profile_log(request, custom_user_id):
    # Obtener todos los registros de ViewProfile para un custom_user dado
    profiles = ViewProfile.objects.filter(custom_user_id=custom_user_id)

    # Serializar los datos si es necesario
    serialized_profiles = [{'timestamp': profile.timestamp, 'counter': profile.counter} for profile in profiles]

    # Devolver los datos como una respuesta JSON
    return JsonResponse(serialized_profiles, safe=False)
