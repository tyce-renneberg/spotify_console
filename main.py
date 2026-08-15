import spotify
from spotify_requests import get_current_track
from display import create_display
from inky_display import show_image
import time

need_authorization = True
time_to_change_display = False
token_expires_at = 0
access_token = ""
refresh_token = ""
response = ""
current_track = ""
last_track = ""

while True:
    if need_authorization:
        access_token, refresh_token = spotify.get_tokens()
        token_expires_at = time.time() + 3600
        need_authorization = False
    elif time.time() >= token_expires_at - 60:
        # get new access token using refresh token
        access_token = spotify.get_new_token(refresh_token)
        token_expires_at = time.time() + 3600

    response = get_current_track(access_token)

    if response.status_code == 200:
        last_track = current_track
        current_track = response.json()["item"]["name"]

    if last_track != current_track:
        time_to_change_display = True

    if time_to_change_display:
        if response.status_code == 200:
            img = create_display(access_token)
            #img.show()
            show_image(img)

        elif response.status_code == 204:
            print("Nothing is currently playing.")

        else:
            print(response.text)

        time_to_change_display = False

    time.sleep(2)