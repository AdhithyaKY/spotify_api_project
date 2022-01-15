from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from rest_framework.views import APIView
from requests import Request, post
from rest_framework import status
from rest_framework.response import Response

from .credentials import REDIRECT_URI, CLIENT_ID, CLIENT_SECRET
from .models import SpotifyToken, TopArtists
from .utils import is_user_authenticated_with_spotify, update_or_create_user_tokens, is_user_authenticated_with_spotify, get_user_top_artists, get_user_top_tracks, update_or_create_user_top_artists


@login_required
def remove_user_token(request):
    user_token = SpotifyToken.objects.filter(user=request.user).delete()
    messages.success(request, ("Successfully removed spotify authentication."))
    return redirect('profile')

def select_artists(request):
    top_artists_info = TopArtists.objects.filter(user=request.user)
    image_urls = top_artists_info[0].artist_image_urls
    artist_names = top_artists_info[0].artist_names
    combined_list = []
    if(len(image_urls) == len(artist_names)):
        for i in range(len(image_urls)):
            combined_list.append((image_urls[i],artist_names[i]))
    
    return render(request, 'spotify/selectartists.html', {'combined_info':combined_list})

class GetUserTopArtists(APIView):
    def get(self, request, format=None):
        artist_names = []
        artist_image_urls = []
        result = get_user_top_artists(self.request.user)
        
        for segment in result['items']:
            artist_names.append(segment['name'])
            artist_image_urls.append(segment['images'][0]['url'])

        update_or_create_user_top_artists(request.user, artist_names, artist_image_urls)

        return Response({'artists': result}, status=status.HTTP_200_OK)

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
        else:
            messages.success(request, ("Spotify authentication success."))

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
        print(self.request.user)
        is_authenticated = is_user_authenticated_with_spotify(
            self.request.user)
        print(is_authenticated)
        return Response({'authenticated': is_authenticated}, status=status.HTTP_200_OK)


