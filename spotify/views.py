from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from rest_framework.views import APIView
from requests import Request, post
from rest_framework import status
from rest_framework.response import Response

from .credentials import REDIRECT_URI, CLIENT_ID, CLIENT_SECRET
from .models import SpotifyToken
from .utils import is_user_authenticated_with_spotify, update_or_create_user_tokens, is_user_authenticated_with_spotify


@login_required
def remove_user_token(request):
    user_token = SpotifyToken.objects.filter(user=request.user).delete()
    messages.success(request, ("Successfully removed spotify authentication."))
    return redirect('profile')


class AuthorizationURL(APIView):
    def get(self, request, format=None):
        scopes = 'ugc-image-upload user-read-playback-state user-modify-playback-state user-read-currently-playing user-read-private user-read-email user-follow-modify user-follow-read user-library-modify user-library-read streaming app-remote-control user-read-playback-position user-top-read user-read-recently-played playlist-modify-private playlist-read-collaborative playlist-read-private playlist-modify-public'

        url = Request('GET', 'https://accounts.spotify.com/authorize', params={
            'scope': scopes,
            'show_dialog': 'true',
            'state': 'spo',
            'response_type': 'code',
            'redirect_uri': REDIRECT_URI,
            'client_id': CLIENT_ID
        }).prepare().url

        return redirect(url)


class RequestAccessToken(APIView):
    def get(self, request, format=None):
        code = request.GET.get('code')
        error = request.GET.get('error')
        if error:
            messages.warning(
                request, ("Spotify authentication failed. Did you mean to click 'Agree' on the Spotify page? Try logging in to Spotify again."))
            return redirect('/profile/')

        response = post('https://accounts.spotify.com/api/token', data={
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': REDIRECT_URI,
        }).json()

        access_token = response.get('access_token')
        token_type = response.get('token_type')
        refresh_token = response.get('refresh_token')
        expires_in = response.get('expires_in')
        error = response.get('error')

        update_or_create_user_tokens(
            request.user, access_token, token_type, expires_in, refresh_token)

        return redirect('/')


class IsAuthenticated(APIView):
    def get(self, request, format=None):
        is_authenticated = is_user_authenticated_with_spotify(
            self.request.user)
        return Response({'status': is_authenticated}, status=status.HTTP_OK)
