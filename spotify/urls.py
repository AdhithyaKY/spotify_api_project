from django.urls import path
from .views import AuthorizationURL

urlpatterns = [
    path('/get-authorization-url', AuthorizationURL.as_view()),
]