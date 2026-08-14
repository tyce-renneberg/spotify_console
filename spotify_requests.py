import spotify
from requests import get
import json


def get_current_track(access_token):
  url = (
    "https://api.spotify.com/v1/"
    "me/player/currently-playing"
  )
  response = get(
    url,
    headers=spotify.get_auth_header(access_token)
  )
  return response

def get_album_url(access_token):
  response = get_current_track(access_token).json()
  return response["item"]["album"]["images"][0]["url"]

def get_song_name(access_token):
  response = get_current_track(access_token).json()
  return response["item"]["name"]

def get_artist_name(access_token):
  response = get_current_track(access_token).json()
  track = response["item"]
  artist_string = ", ".join(artist["name"] for artist in track["artists"] )
  return artist_string