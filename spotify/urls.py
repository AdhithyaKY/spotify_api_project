from django.urls import path
from .views import AuthorizationURL, RequestAccessToken, IsAuthenticated

urlpatterns = [
    path('get-authorization-url/', AuthorizationURL.as_view(), name='spotify-auth'),
    path('redirect/', RequestAccessToken.as_view(), name='spotify-redirect'),
    path('is_authenticated/', IsAuthenticated.as_view(), name='spotify-auth-check'),
]
