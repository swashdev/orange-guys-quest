# Copyright (c) 2011-2017 Philip Pavlick
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# 
# Like most of the software that I write, this software has an additional
# "careware clause."  If you like this software and would like to support the
# creator, please read "letter.txt" (in this directory)

# Functions for loading images for Orange Guy's Quest
from pygame import image

SPRITES = { "player":None,"key":None,"key2":None,"door":None,"spike":None, \
            "rat":None,"exit":None,"end":None,"dead":None,"goblin":None, \
            "ghost":None,"skull":None,"bat":None \
          }
ALPHA = { 'a':None, 'b':None, 'c':None, 'd':None, 'e':None, 'f':None, \
          'g':None, 'h':None, 'i':None, 'j':None, 'k':None, 'l':None, \
          'm':None, 'n':None, 'o':None, 'p':None, 'q':None, 'r':None, \
          's':None, 't':None, 'u':None, 'v':None, 'w':None, 'x':None, \
          'y':None, 'z':None \
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

# Returns a pygame image
def get_alpha( char, d = '/', DEBUG = False ):
  global ALPHA
  ch = char.lower()
  if ALPHA[ch] != None:
    return ALPHA[ch]
  else:
    if DEBUG:
      print "Load: Alphabet sprite \'" + ch + "\'"
    ALPHA[ch] = image.load( "Images" + d + "Font2" + d + ch + ".gif" )
    return ALPHA[ch]

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
  if key == "goblin":
    return il + "goblin.png"
  if key == "ghost":
    return il + "dimensionalSpirit.png"
  if key == "skull":
    return il + "possessedSkull.png"
