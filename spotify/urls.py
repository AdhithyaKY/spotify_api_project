from django.urls import path
from .views import AuthorizationURL, RequestAccessToken, IsAuthenticated

urlpatterns = [
    path('get-authorization-url', AuthorizationURL.as_view()),
    path('redirect', RequestAccessToken.as_view()),
    path('is_authenticated', IsAuthenticated.as_view()),
]