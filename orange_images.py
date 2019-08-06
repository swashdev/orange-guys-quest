# Copyright (c) 2011-2019 Philip Pavlick
# 
# <swashdev@pm.me> wrote this file.  Feel free to do whatever you want
# with it as long as you retain this notice and don't hold me liable for any
# damages; there is no warranty.  If you really want to pay me back, maybe
# someday you can buy me some sunflower seeds and we'll call it even.
# Have fun.
#   - Philip Pavlick

# Functions for loading images for Orange Guy's Quest
from pygame import image

SPRITES = { "player":None,"key":None,"key2":None,"door":None,"spike":None, \
            "rat":None,"exit":None,"end":None,"dead":None,"won":None,
            "goblin":None,"ghost":None,"skull":None,"bat":None \
          }

# Returns a pygame image
def get_sprite( key, d = '/', DEBUG = False ):
  global SPRITES
  if SPRITES[key] != None:
    return SPRITES[key]
  else:
    if DEBUG:
      print "Load: " + key + " sprite"
    SPRITES[key] = image.load( get_image_link( key, d ) )
    if DEBUG:
      print "Work: Converting " + key + " sprite"
    if key != "dead":
      SPRITES[key].set_colorkey( (255, 255, 255) )
    else:
      SPRITES[key].set_colorkey( (255, 128, 255) )
    SPRITES[key].convert_alpha()
    return SPRITES[key]

def get_image_link( key, d ):
  il = "Images" + d
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
