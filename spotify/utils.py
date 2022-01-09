from .models import SpotifyToken, TopArtists
from django.utils import timezone
from datetime import timedelta
from .credentials import CLIENT_ID, CLIENT_SECRET
from requests import post, get, put

BASE_API_URL = "https://api.spotify.com/v1/me"

def get_user_tokens(user):
    user_tokens = SpotifyToken.objects.filter(user=user)
    if user_tokens.exists():
        return user_tokens[0]
    else:
        return None

def get_user_top_artists_from_db(user):
    top_artists = TopArtists.objects.filter(user=user)
    if (top_artists.exists()):
        return top_artists[0]
    else:
        return None

def update_or_create_user_tokens(user, access_token, token_type, expires_in, refresh_token):
    tokens = get_user_tokens(user)
    print(tokens)
    expires_in = timezone.now() + timedelta(seconds=expires_in)

    if tokens:
        tokens.access_token = access_token
        tokens.refresh_token = refresh_token
        tokens.expires_in = expires_in
        tokens.token_type = token_type
        tokens.save(update_fields=['access_token',
                    'refresh_token', 'expires_in', 'token_type'])
    else:
        tokens = SpotifyToken(user=user, access_token=access_token,
                              refresh_token=refresh_token, token_type=token_type, expires_in=expires_in)
        tokens.save()

def update_or_create_user_top_artists(user, artist_names, artist_image_urls):
    top_artists = get_user_top_artists_from_db(user)
    
    if top_artists:
        top_artists.artist_names = artist_names
        top_artists.artist_image_urls = artist_image_urls
        top_artists.save(update_fields=['artist_names', 'artist_image_urls'])
    else:
        top_artists = TopArtists(user=user, artist_names=artist_names, artist_image_urls=artist_image_urls)
        top_artists.save()

def is_user_authenticated_with_spotify(user):
    tokens = get_user_tokens(user)
    if tokens:
        expiration_time = tokens.expires_in
        if (expiration_time <= timezone.now()):
            refresh_user_spotify_token(user)
        return True
    return False


def refresh_user_spotify_token(user):

    refresh_token = get_user_tokens(user).refresh_token

    response = post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }).json()

    new_access_token = response.get('access_token')
    token_type = response.get('token_type')
    expires_in = response.get('expires_in')
    refresh_token = response.get('refresh_token')

    update_or_create_user_tokens(
        user, new_access_token, token_type, expires_in, refresh_token)

def execute_spotify_api_request(user, api_endpoint, post_request=False, put_request=False):
    user_tokens = get_user_tokens(user)
    headers = {'Content-Type': 'application/json',
               'Authorization': "Bearer " + user_tokens.access_token}

    if post_request:
        post(BASE_API_URL + api_endpoint, headers=headers)
    if put_request:
        put(BASE_API_URL + api_endpoint, headers=headers)

    response = get(BASE_API_URL + api_endpoint, {}, headers=headers)

    try:
        return response.json()
    except:
        return {'Error': 'Error occurred with API Request.'}


def get_user_top_artists(user):
    if (is_user_authenticated_with_spotify(user)):
        return execute_spotify_api_request(user, "/top/artists")
    else:
        return {'Error': 'User does not have spotify tokens, cannot retrieve top artists.'}

def get_user_top_tracks(user):
    if (is_user_authenticated_with_spotify(user)):
        return execute_spotify_api_request(user, "/top/tracks")
    else:
        return {'Error': 'User does not have spotify tokens, cannot retrieve top tracks.'}