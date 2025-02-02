from django.core.management import BaseCommand, call_command
from django.contrib.auth.models import User
from accounts.models import Teams
import requests
# from yourapp.models import User # if you have a custom user


class Command(BaseCommand):
    help = "DEV COMMAND: Fill database with a set of data for testing purposes"

    def handle(self, *args, **options):
        call_command('loaddata','demo_user_data.json')
        # Fix the passwords of fixtures
        for user in User.objects.all():
            user.set_password(user.password)
            user.save()
        data = requests.get("https://statsapi.mlb.com/api/v1/teams")
        json_data = data.json()
        teams = json_data["teams"]
        for team in teams:
            new_team = Teams.objects.create(
                name=team["name"],
                mlb_id = team["id"],
                link = team["link"]
            )
