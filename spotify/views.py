from django.shortcuts import render, redirect
from .credentials import REDIRECT_URI, CLIENT_ID, CLIENT_SECRET
from rest_framework.views import APIView
from requests import Request, post
from rest_framework import status
from rest_framework.response import Response
from .utils import is_user_authenticated_with_spotify, update_or_create_user_tokens, is_user_authenticated_with_spotify


class AuthorizationURL(APIView):
    def get(self, request, format=None):
        scopes = 'ugc-image-upload user-read-playback-state user-modify-playback-state user-read-currently-playing user-read-private user-read-email user-follow-modify user-follow-read user-library-modify user-library-read streaming app-remote-control user-read-playback-position user-top-read user-read-recently-played playlist-modify-private playlist-read-collaborative playlist-read-private playlist-modify-public'

        url = Request('GET', 'https://accounts.spotify.com/authorize', params={
            'scope': scopes,
            'response_type': 'code',
            'redirect_uri': REDIRECT_URI,
            'client_id': CLIENT_ID
        }).prepare().url

        return redirect(url)


class RequestAccessToken(APIView):
    def get(self, request, format=None):
        code = request.GET.get('code')
        error = request.GET.get('error')

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

        if not request.session.exists(request.session.session_key):
            request.session.create()

        update_or_create_user_tokens(
            request.session.session_key, access_token, token_type, expires_in, refresh_token)

        return redirect('/')


class IsAuthenticated(APIView):
    def get(self, request, format=None):
        is_authenticated = is_user_authenticated_with_spotify(
            self.request.session.session_key)
        return Response({'status': is_authenticated}, status=status.HTTP_OK)
