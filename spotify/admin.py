from django.contrib import admin

from spotify.models import SpotifyToken, TopArtists

admin.site.register(TopArtists)
admin.site.register(SpotifyToken)
