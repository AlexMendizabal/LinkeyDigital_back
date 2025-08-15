from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.utils import timezone

from apps.authentication.models import CustomerUser
from apps.administration.models import Licencia

class LicenciaPostAndPatchListingTests(APITestCase):
    def setUp(self):
        self.superuser = CustomerUser.objects.create_superuser(
            username='super', email='super@example.com', password='superpass', uid='uid-super'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.superuser)
        self.user_a = CustomerUser.objects.create_user(username='a', email='a@example.com', password='pass', uid='uid-a')
        self.user_b = CustomerUser.objects.create_user(username='b', email='b@example.com', password='pass', uid='uid-b')

    def test_post_licenciasup_with_user_id_links_license(self):
        url = reverse('get_or_create_all_licenses')
        payload = {
            'user_id': self.user_a.id,
            'tipo_de_plan': 'basic',
            'duracion': 15,
            'cobro': 50,
            'status': 1,
            'fecha_inicio': timezone.now(),
        }
        resp = self.client.post(url, data=payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.user_a.refresh_from_db()
        self.assertIsNotNone(self.user_a.licencia_id_id)

    def test_patch_change_admin_reflects_in_listing(self):
        # Create license for user_a
        lic = Licencia.objects.create(customer_user_admin=self.user_a, tipo_de_plan='basic', fecha_inicio=timezone.now(), cobro=10, duracion=10, status=1)
        self.user_a.licencia_id_id = lic.id
        self.user_a.is_admin = True
        self.user_a.save()
        # Change admin to user_b
        url_patch = reverse('patch_licenses', kwargs={'pk': lic.id})
        resp = self.client.patch(url_patch, data={'custom_user_admin': self.user_b.id}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        # List empresas
        url_list = reverse('get_all_users')
        resp_list = self.client.get(url_list)
        self.assertEqual(resp_list.status_code, status.HTTP_200_OK)
