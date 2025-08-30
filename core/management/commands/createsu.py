from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
import os

username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
full_name = os.environ.get('DJANGO_SUPERUSER_FULL_NAME')

class Command(BaseCommand):
    help = 'Creates a superuser.'

    def handle(self, *args, **options):
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(
                username=username,
                password=password,
                email=email,
                full_name=full_name
            )
        print('Superuser has been created.')