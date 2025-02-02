from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Teams(models.Model):
    name = models.CharField(max_length=500)
    mlb_id = models.IntegerField()
    link = models.CharField(max_length=500)

    def __str__(self):
        return self.name

class Favorite_Teams(models.Model):
    team = models.ForeignKey(Teams, related_name="fans", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="teams", on_delete=models.CASCADE)

    def __str__(self):
        return self.team.name
