import spotify
from display import create_display
from inky_display import show_image

access_token = spotify.get_access_token()
response = spotify.get_current_track(access_token)

print("Status:", response.status_code)

if response.status_code == 200:

    data = response.json()

    track = data["item"]

    print("Song:", track["name"])
    print(
        "Artist:",
        ", ".join(
            artist["name"]
            for artist in track["artists"]
        )
    )
    # integer index can be 1,2 or 3 depending on image dimensions

    img = create_display(access_token)
    show_image(img)

elif response.status_code == 204:
    print("Nothing is currently playing.")

else:
    print(response.text)