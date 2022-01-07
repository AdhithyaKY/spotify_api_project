import os

CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
# if in aws, change to:
REDIRECT_URI = "http://ec2-54-172-154-161.compute-1.amazonaws.com:8000/spotify/redirect/"
# if testing locally, change to:
#REDIRECT_URI = "http://127.0.0.1:8000/spotify/redirect/"
