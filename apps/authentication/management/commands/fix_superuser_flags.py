from django.core.management.base import BaseCommand
from apps.authentication.models.customer_user import CustomerUser

class Command(BaseCommand):
    help = 'Asegura que todos los superusuarios tengan todos los permisos y flags relevantes activos.'

    def handle(self, *args, **options):
        superusers = CustomerUser.objects.filter(is_superuser=True)
        updated = 0
        for user in superusers:
            changed = False
            if not user.is_admin:
                user.is_admin = True
                changed = True
            if not user.is_sales_manager:
                user.is_sales_manager = True
                changed = True
            if not user.is_staff:
                user.is_staff = True
                changed = True
            if not user.is_active:
                user.is_active = True
                changed = True
            if changed:
                user.save()
                updated += 1
        self.stdout.write(self.style.SUCCESS(f'Superusuarios actualizados: {updated}'))
