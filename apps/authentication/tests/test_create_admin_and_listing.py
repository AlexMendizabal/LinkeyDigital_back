from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.utils import timezone

from apps.authentication.models import CustomerUser

class CreateAdminAndListingTests(APITestCase):
    def setUp(self):
        self.superuser = CustomerUser.objects.create_superuser(
            username='super', email='super@example.com', password='superpass', uid='uid-super'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.superuser)

    def test_create_admin_creates_license_and_lists_in_allEmpresas(self):
        # Create admin empresa
        url_create = reverse('register_user_admin')
        payload = {
            'correo': 'empresa1@example.com',
            'esEmpresa': True,
            'tipo_de_plan': 'pro',
            'duracion': 30,
            'cobro': 100,
            'status': 1,
            'fecha_inicio': timezone.now()
        }
        resp = self.client.post(url_create, data=payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        data = resp.json()
        self.assertIn('licencia_id', data)
        self.assertIn('licencia', data)
        # Now list empresas
        url_list = reverse('get_all_users')
        resp_list = self.client.get(url_list)
        self.assertEqual(resp_list.status_code, status.HTTP_200_OK)
        empresas = resp_list.json().get('data', [])
        self.assertTrue(any(e['custom_user']['email'] == 'empresa1@example.com' for e in empresas))
