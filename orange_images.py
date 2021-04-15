# This is free and unencumbered software released into the public domain.
# Anyone is free to copy, modify, publish, use, compile, sell, or distribute
# this software, for any purpose, commercial or non-commercial, and by any
# means.
# For more information, please refer to UNLICENSE or to <http://unlicense.org>

# Functions for loading images for Orange Guy's Quest
from pygame import image

SPRITES = { "player":None,"key":None,"key2":None,"door":None,"spike":None, \
            "rat":None,"ratking":None,"exit":None,"end":None,"dead":None, \
            "won":None,"goblin":None,"ghost":None,"skull":None,"bat":None \
          }

# Returns a pygame image
def get_sprite( key, DEBUG = False ):
  global SPRITES
  if SPRITES[key] != None:
    return SPRITES[key]
  else:
    if DEBUG:
      print "Load: " + key + " sprite"
    SPRITES[key] = image.load( get_image_link( key ) )
    if DEBUG:
      print "Work: Converting " + key + " sprite"
    if key != "dead":
      SPRITES[key].set_colorkey( (255, 255, 255) )
    else:
      SPRITES[key].set_colorkey( (255, 128, 255) )
    SPRITES[key].convert_alpha()
    return SPRITES[key]

def get_image_link( key ):
  il = "Images/"
  if key == "player":
    return il + "maincharsprite.png"
  if key == "key":
    return il + "keynew.png"
  if key == "key2":
    return il + "keyRednew.png"
  if key == "door":
    return il + "door.png"
  if key == "spike":
    return il + "spike.png"
  if key == "rat":
    return il + "giantRat.png"
  if key == "ratking":
    return il + "ratking.png"
  if key == "bat":
    return il + "bat.png"
  if key == "exit":
    return il + "lvlExit.png"
  if key == "end":
    return il + "end.png"
  if key == "dead":
    return il + "dead.png"
  if key == "won":
    return il + "maincharend.png"
  if key == "goblin":
    return il + "goblin.png"
  if key == "ghost":
    return il + "dimensionalSpirit.png"
  if key == "skull":
    return il + "possessedSkull.png"
