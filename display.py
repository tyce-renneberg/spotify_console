from PIL import Image, ImageDraw, ImageFont
import spotify
from io import BytesIO
import requests

def image_from_url(image_url):
  response = requests.get(image_url)
  response.raise_for_status()
  album_cover = Image.open(BytesIO(response.content)).convert("RGBA")
  return album_cover.resize((440,440))

def create_background():
  return Image.new("RGB", (800,480), (255,255,255))

def shorten_text(draw,text,font):
   if draw.textlength(text,font=font) <= 240:
      return text
   else:
      while draw.textlength(text + "...", font=font) > 240:
         text = text[:-1]
      return text + "..."

def create_display(access_token):
  # get album cover
  image_url = spotify.get_album_url(access_token)
  album_cover = image_from_url(image_url)

  # paste album cover onto white background
  background = create_background()
  background.paste(album_cover,(100,20))

  # draw song + album information onto screen
  draw = ImageDraw.Draw(background)
  song_font = ImageFont.truetype("Oswald-Medium.ttf", 35)
  song_name = shorten_text(draw, spotify.get_song_name(access_token), song_font)
  artist_font = ImageFont.truetype("Oswald-Medium.ttf", 20)
  artist_name = shorten_text(draw, spotify.get_artist_name(access_token), artist_font)

  draw.text(
     (550,50),
     song_name, 
     font = song_font, fill = (0,0,0)
     )
  draw.text(
     (550,95),
     artist_name, 
     font = artist_font, 
     fill = (0,0,0)
     )
  
  return background