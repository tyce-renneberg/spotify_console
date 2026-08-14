from inky.auto import auto

inky = auto()

def show_image(image):
  inky.set_image(image)
  inky.show()