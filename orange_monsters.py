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

# Monster data file for Orange Guy's Quest
# This file DEPENDS ON:
#   orange_images.py

# This file is designed for people adding new monster data to Orange Guy's
# Quest.  The below dictionary contains monster data indexed with symbols.
# If the level reading function in the `Level' class from ``orange.py'' finds
# one of the symbols in this dictionary, it will create a new `Enemy' from
# this dictionary.  The monster data is formatted like this:
# ( width, height, horizontal_speed, vertical_speed, direction, max_distance,
#   type, sprite (usually orange_images.get_sprite) )
#
# Note that if the map symbol is one of W, >, <, -, +, E, A, K, G, P, D, 1, 2,
# 3, 4, 6, 7, 8, 9, !, @, #, $, ^, &, *, or (, the level generation function
# will not use it for this purpose.  S also will not be used, since those are
# spikes and not a monster.
#
# Helpful tip: There are a few ways to fiddle with monster movement.
# Setting both horizontal_speed and vertical_speed to 0 will automatically
# cause the monster to hold still at all times.  So will setting direction or
# max_distance to 0.
# Setting direction to a value other than -1, 1, or 0 will cause direction to
# be selected randomly.  Setting max_distance to less than 0 will cause a
# value between 0 and 5 to be chosen.
# Setting type to None will cause the game to randomly choose "bat" or "rat"
# but will not impact movement settings.
# Setting sprite to None will cause the game to attempt to get a sprite based
# on what type was set to.
#
# IMPORTANT: type is case-sensitive.
# 
# This is the EASY WAY to add new monsters to the game; more complex stuff
# will require editing the `Enemy' class in ``orange.py''

import orange_images

# `d' is a variable used to determine if '/' or '\' is used for directories.
# It is usually '/'

d = '/'

mondata = {
    'r':(16, 16, 1, 0,  1, 5, "rat", orange_images.get_sprite( "rat", d )),
    'R':(16, 16, 1, 0, -1, 5, "rat", orange_images.get_sprite( "rat", d )),
    'b':(16, 16, 0, 1,  1, 5, "bat", orange_images.get_sprite( "bat", d )),
    'B':(16, 16, 0, 1, -1, 5, "bat", orange_images.get_sprite( "bat", d ))
          }
