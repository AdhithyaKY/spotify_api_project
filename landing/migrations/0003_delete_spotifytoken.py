# Generated by Django 3.2.10 on 2022-01-04 14:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0002_alter_spotifytoken_refresh_token'),
    ]

    operations = [
        migrations.DeleteModel(
            name='SpotifyToken',
        ),
    ]
