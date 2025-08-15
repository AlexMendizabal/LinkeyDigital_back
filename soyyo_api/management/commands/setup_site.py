from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site

class Command(BaseCommand):
    help = 'Crea o actualiza el objeto Site para Allauth (localhost:8000)'

    def handle(self, *args, **options):
        site, created = Site.objects.update_or_create(
            domain='localhost:8000',
            defaults={
                'name': 'localhost',
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Site creado: localhost:8000'))
        else:
            self.stdout.write(self.style.SUCCESS('Site actualizado: localhost:8000'))
