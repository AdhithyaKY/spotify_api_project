from django.urls import path
from .views import AuthorizationURL, GetUserTopArtists, RequestAccessToken, IsAuthenticated, remove_user_token
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('get-authorization-url/', login_required(AuthorizationURL.as_view()), name='spotify-auth'),
    path('redirect/', login_required(RequestAccessToken.as_view()), name='spotify-redirect'),
    path('is_authenticated/', login_required(IsAuthenticated.as_view()), name='spotify-auth-check'),
    path('remove_auth/', remove_user_token, name='spotify-remove-auth'),
    path('get_user_top_artists/', login_required(GetUserTopArtists.as_view()), name="spotify-user-top-artists")
]
