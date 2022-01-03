from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='landing-home'),
    path('about/', views.about, name='landing-about'),
    path('stats.html', views.stats, name='landing-stats'),
    path('spotify_login/', views.spotify_login, name='landing-spotify'),
    path('callback/', views.callback, name='landing-callback')
]
