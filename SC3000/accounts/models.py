from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class FavoriteTeams(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Storing teams as a string for now, will store as
    teams = models.CharField(max_length=500)
