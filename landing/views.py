from django.shortcuts import redirect, render
from django.http import HttpResponse
from spotipy.oauth2 import SpotifyOAuth
from requests import Request, post
from rest_framework import status
from rest_framework.response import Response
from spotify.credentials import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI

posts = [
    {
        'author': 'CoreyMS',
        'title': 'blog post 1',
        'content': 'first post',
        'date_posted': 'august 27, 2018'
    },
    {
        'author': 'jane doe',
        'title': 'blog post 2',
        'content': '2nd post',
        'date_posted': 'august 27, 2018'
    }
]


def home(request):
    context = {
        'posts': posts
    }
    return render(request, 'landing/home.html', context)


def about(request):
    return render(request, 'landing/about.html', {'title': 'about'})


def stats(request):
    return render(request, 'landing/stats.html', {'title': 'stats'})


def spotify_login(request):
    scope = 'ugc-image-upload user-read-playback-state user-modify-playback-state user-read-currently-playing user-read-private user-read-email user-follow-modify user-follow-read user-library-modify user-library-read streaming app-remote-control user-read-playback-position user-top-read user-read-recently-played playlist-modify-private playlist-read-collaborative playlist-read-private playlist-modify-public'

    sp_auth = SpotifyOAuth(
        scope=scope,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
    )
    #
    # Note: You should parse this somehow. It may not be in a pretty format.
    redirect_url = sp_auth.get_authorize_url()
    return redirect(redirect_url)


def callback(request):
    scope = 'ugc-image-upload user-read-playback-state user-modify-playback-state user-read-currently-playing user-read-private user-read-email user-follow-modify user-follow-read user-library-modify user-library-read streaming app-remote-control user-read-playback-position user-top-read user-read-recently-played playlist-modify-private playlist-read-collaborative playlist-read-private playlist-modify-public'

    sp_auth = SpotifyOAuth(
        scope=scope,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
    )
    code = request.GET.get("code", "")
    token = sp_auth.get_access_token(code=code, as_dict=True)

    return render(request, 'landing/callback.html', token)
