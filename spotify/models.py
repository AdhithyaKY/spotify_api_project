from django.db import models
from django.contrib.postgres.fields import ArrayField

class SpotifyToken(models.Model):
    user = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    refresh_token = models.CharField(max_length=500)
    access_token = models.CharField(max_length=500)
    expires_in = models.DateTimeField()
    token_type = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Spotify Tokens"
        verbose_name_plural = "Spotify Tokens"

class TopArtists(models.Model):
    user = models.CharField(max_length=50, unique=True)
    artist_names = ArrayField(models.CharField(max_length=50, blank=True),size=20)
    artist_image_urls = ArrayField(models.CharField(max_length=500, blank=True),size=20)
    
    class Meta:
        verbose_name = "Top Artists"
        verbose_name_plural = "Top Artists"