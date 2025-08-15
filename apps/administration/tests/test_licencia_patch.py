from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.utils import timezone

from apps.authentication.models import CustomerUser
from apps.administration.models import Licencia


class LicenciaPatchTests(APITestCase):
    def setUp(self):
        self.superuser = CustomerUser.objects.create_superuser(
            username='admin', email='admin@example.com', password='adminpass', uid='uid-admin'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.superuser)
        self.user = CustomerUser.objects.create_user(
            username='user1', email='user1@example.com', password='userpass', uid='uid-user1'
        )
        self.licencia = Licencia.objects.create(
            customer_user_admin=None,
            tipo_de_plan='basic',
            fecha_inicio=timezone.now(),
            cobro=10,
            duracion=30,
            status=1,
        )

    def test_patch_update_customer_user_admin(self):
        url = reverse('patch_licenses', kwargs={'pk': self.licencia.id})
        payload = {
            'custom_user_admin': self.user.id,  # alias accepted
            'tipo_de_plan': 'pro'
        }
        resp = self.client.patch(url, data=payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.licencia.refresh_from_db()
        self.user.refresh_from_db()
        self.assertEqual(self.licencia.customer_user_admin_id, self.user.id)
        self.assertTrue(self.user.is_admin)

    def test_patch_bad_request_invalid_user(self):
        url = reverse('patch_licenses', kwargs={'pk': self.licencia.id})
        payload = {'customer_user_admin': 999999}
        resp = self.client.patch(url, data=payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
