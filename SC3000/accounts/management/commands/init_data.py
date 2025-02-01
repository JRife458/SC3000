from django.core.management import BaseCommand, call_command
from django.contrib.auth.models import User
# from yourapp.models import User # if you have a custom user


class Command(BaseCommand):
    help = "DEV COMMAND: Fill database with a set of data for testing purposes"

    def handle(self, *args, **options):
        call_command('loaddata','demo_user_data.json')
        # Fix the passwords of fixtures
        for user in User.objects.all():
            user.set_password(user.password)
            user.save()
