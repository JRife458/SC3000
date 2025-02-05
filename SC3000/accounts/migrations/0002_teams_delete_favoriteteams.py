# Generated by Django 5.1.5 on 2025-02-02 02:28

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Teams',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('mlb_id', models.IntegerField()),
                ('sport', models.CharField(max_length=500)),
                ('league', models.CharField(max_length=500)),
                ('division', models.CharField(max_length=500)),
                ('link', models.CharField(max_length=500)),
                ('fans', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='FavoriteTeams',
        ),
    ]
