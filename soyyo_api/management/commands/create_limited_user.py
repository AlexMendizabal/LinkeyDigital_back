#Esto fue  creado para dar el comando de usuarios limitados, sin embargo no se implementa por tiempo

# from django.core.management.base import BaseCommand
# from django.contrib.auth.models import User

# class Command(BaseCommand):
#     help = 'Create a limited user'

#     def handle(self, *args, **options):
#         username = input("Enter username: ")
#         password = input("Enter password: ")
        
#         user = User.objects.create_user(username=username, password=password)
        
#         self.stdout.write(self.style.SUCCESS(f'Successfully created user {username}'))
