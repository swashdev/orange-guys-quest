#! /usr/bin/env python

# Orange Guy's Quest mainfile

#Contains code from pymike's public domain collision and camera tutorials
#Pymike's website: http://pymike.pynguins.com/
#This code has been heavily modified and is unrecognizable unless you look
#closely.
#
# This is free and unencumbered software released into the public domain.
# Anyone is free to copy, modify, publish, use, compile, sell, or distribute
# this software, for any purpose, commercial or non-commercial, and by any
# means.
# For more information, please refer to UNLICENSE or to <http://unlicense.org>

#import os
import sys
import random
import pygame
from pygame.locals import *

print "Welcome to Orange Guy's Quest Classic, by Philip Pavlick."

##########################
# Configuration options: #
##########################

# Set LEVELPATH to the file where you have your levels saved.  By default,
# this is ./orange-levels.  Don't set it to ./extraLevels.txt because those
# levels are awful.
# Can be set with -l <file> or --level <file> in the command line
LEVELPATH = "orange-levels"

# Much like LEVELPATH, determines the path for the introductory levels.
# Can be accessed with --help, -?, or --intro, but should not be modified.
INTROLEVELS = "help.txt"

# Set USERECTS to True to force the old-school Atari2600-style blocky
# graphics or False to use the Retro pixel graphics.  Any other value will
# give a prompt.
# Can be set to False with -r or -s, or True with -a or -b, in the command line
USERECTS = False

# Set these to the pixel values you want the game to use for the screen.  Note
# that the game was originally programmed for a 640x480 window, and it looks
# just fine in that resolution.
# Can be set with -W in the command line, or individually with -x or -w for
# WIN_X and -y or -h for WIN_Y
WIN_X = 640
WIN_Y = 480

# Set BIGPLAYER to True to restore the player's original large hitbox.  This is
# not recommended, but I thought people might get a chuckle out of this.
# Can be set with -B in the command line
BIGPLAYER = False

# Set this to True if you want annoying debug messages in your console.
# Can be set with -D in the command line
DEBUG = False

##########################
# Pre-code configuration #
##########################

getting_help = False

vars = sys.argv
vars.pop(0)
while len( vars ) > 0:
  global USERECTS,LEVELPATH,BIGPLAYER,DEBUG
  opt = vars.pop(0)
  if opt == "-r":
    USERECTS = False
  elif opt == "-b" or opt == '-a':
    USERECTS = True
  elif opt == "-B":
    BIGPLAYER = True
  elif opt == "-D":
    DEBUG = True
  elif opt == "-W":
    WIN_X = int(vars.pop(0))
    WIN_Y = int(vars.pop(0))
  elif opt == "-x" or opt == "-w":
    WIN_X = int(vars.pop(0))
  elif opt == "-y" or opt == "-h":
    WIN_Y = int(vars.pop(0))
  elif opt == "-l" or opt == "--levels":
    if len(vars) > 0:
      LEVELPATH = vars.pop(0)
    else:
      raise SystemExit, "Not enough parameters for --levels: Must specify a file."
  elif opt in ["-?", "--help", "--levels"]:
    LEVELPATH = INTROLEVELS
    getting_help = True

while USERECTS not in [True,False]:
    print "Use [R]etro or [A]ncient graphics? [R/A]"
    USERECTS=raw_input("[\'\b").upper()
    if USERECTS=="R":
        USERECTS=False
    elif USERECTS=="A":
        USERECTS=True
    
# Initialise pygame
#os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()

# Set up the display
pygame.display.set_caption("Orange Guy's Quest!!")
screen = pygame.display.set_mode((WIN_X, WIN_Y))
if DEBUG:
  print "Create: PyGame screen"

#pygame.display.toggle_fullscreen()

##################################
# Pre-code variable declarations #
##################################

clock = pygame.time.Clock()
walls = [] # List to hold the walls

jumpDY=0

timeBuffer=0

tele_rect=pygame.Rect(0,0,16,16)

end_rect=None
won = False

lvlMessage=""

# Important: See ``fonts/readme-proggy.txt'' for the Proggy license
font = pygame.font.Font("fonts/ProggySquareSZ.ttf", 24)
text = None
textpos = None
message_delay = 0

# Sprite declarations:
import orange_images

######################
# Class declarations #
######################

# Class for the orange dude
class Player(object):
    jump=False
    dJump=False
    dead = False
    sprite=None
    ID="Player"
    color=(255,128,0)
    def __init__(self):
        global BIGPLAYER
        if not BIGPLAYER:
          self.rect = pygame.Rect(32, 32, 8, 16)
        else:
          self.rect = pygame.Rect(32, 32, 16, 16)
        if not USERECTS:
          self.sprite = orange_images.get_sprite( "player", DEBUG )

    def move(self, dx, dy):
        if not self.dead: 
            # Move each axis separately. Note that this checks for collisions both times.
            if dx != 0:
                self.move_single_axis(dx, 0)
            if dy != 0:
                self.move_single_axis(0, dy)
    
    def move_single_axis(self, dx, dy):
        
        # Move the rect
        self.rect.x += dx
        self.rect.y += dy

        # If you collide with a wall, move out based on velocity
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if wall.ID not in ["Enemy","spike","Key","Portal","Destination"]:
                    if dx > 0: # Moving right; Hit the left side of the wall
                        self.rect.right = wall.rect.left
                    if dx < 0: # Moving left; Hit the right side of the wall
                        self.rect.left = wall.rect.right
                    if dy > 0: # Moving down; Hit the top side of the wall
                        self.rect.bottom = wall.rect.top
                        self.jump=False#Edited by me to simulate landing
                        self.dJump=False
                        global jumpDY
                        jumpDY=0
                        #if wall.ID=="Mover":
                        #    self.rect.x+=wall.direction
                    if dy < 0: # Moving up; Hit the bottom side of the wall
                        self.rect.top = wall.rect.bottom
                        global jumpDY
                        jumpDY=0
                elif wall.ID in ["Enemy","spike"]:
                    if DEBUG:
                      print "Event: Player killed by "+wall.ID
                    global text, textpos
                    text = font.render("You are dead.  Press BACKSPACE to restart.", 1, (255, 128, 0))
                    textpos = text.get_rect(centerx=screen.get_width()/2)
                    self.dead = True
                elif wall.ID=="Key":
                    for object in walls:
                        if object.ID=="Door":
                            if object.Color==wall.Color:
                                object.Open()
                elif wall.ID == "Portal":
                    if DEBUG:
                      print "Event: Player touched a portal"
                    for object in walls:
                        if object.ID=="Destination":
                            self.rect = object.rect
                            if DEBUG:
                              print "Zzzap!  Sent player to", self.rect.x, self.rect.y

# Nice class to hold a wall rect
class Wall(object):
    sprite=None
    ID="Wall"
    color=(255,255,255)
    def __init__(self, pos):
        global walls
        walls.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], 16, 16)

class Mover(Wall):
    ID="Mover"
    direction=-1
    difference=0
    maxDiff=5
    h=0
    v=0
    def __init__(self,coord,direction):
        self.h=direction[0]
        self.v=direction[1]
        super(Mover,self).__init__(coord)
    def update(self):
        if self.direction==1:
            if self.difference<self.maxDiff*16:
                self.rect.x+=self.h
                self.rect.y+=self.v
                self.difference+=1
            else:
                self.direction=-1
        else:
            if self.difference>-(self.maxDiff*16):
                self.rect.x-=self.h
                self.rect.y-=self.v
                self.difference-=1
            else:
                self.direction=1
                
        dx = self.h * self.direction
        dy = self.v * self.direction

        # If you collide with a wall, move out based on velocity
        for wall in walls:
            if wall.ID=="Door" and self.rect.colliderect(wall.rect):
                if dx > 0: # Moving right; Hit the left side of the wall
                    self.rect.right = wall.rect.left
                    self.direction *= -1
                if dx < 0: # Moving left; Hit the right side of the wall
                    self.rect.left = wall.rect.right
                    self.direction *= -1
                if dy > 0: # Moving down; Hit the top of the wall
                    self.rect.bottom = wall.rect.top
                    self.direction *= -1
                if dy < 0:
                    self.rect.top = wall.rect.bottom
                    self.direction *= -1
            #if wall.ID=="Player" and self.rect.colliderect(wall.rect):
                #wall.move(self.direction,1)

class Door(Wall):
    close=True
    openx=1#1 for right, -1 for left, 0 for none
    openy=1#1 for down, -1 for up, 0 for none
    sprite=None
    ID="Door"
    Color="blue"
    def Open(self):
        if self.close:
            self.rect.x+=(16*self.openx)
            self.rect.y+=(16*self.openy)
            self.close=False
            if DEBUG:
              print "Event: Open door"
    def __init__(self, pos,openx,openy,color="green"):
        if color.lower()=="red":
            self.color=(255,255,255)
            self.Color="red"
            self.sprite = "HIDDEN"
        else:
            self.Color="green"
            self.color=(0,0,255)
            if not USERECTS:
              self.sprite = orange_images.get_sprite( "door", DEBUG )
        self.rect=pygame.Rect(pos[0],pos[1],16,16)
        self.openx=openx
        self.openy=openy

class Key(Wall):
    ID="Key"
    Color="blue"
    sprite=None
    def __init__(self,pos,color="green"):
        self.Color=color
        if color=="red":
            if not USERECTS:
              self.sprite = orange_images.get_sprite( "key2", DEBUG )
            self.color=(255,255,0)
            self.Color="red"
        else:
            if not USERECTS:
              self.sprite = orange_images.get_sprite( "key", DEBUG )
            self.Color="green"
            self.color=(0,255,0)
        super(Key,self).__init__(pos)

class Portal(Wall):
    ID="Portal"
    color = (0, 0, 255)

class Destination(Wall):
    ID="Destination"
    def __init__(self, pos):
        global walls
        walls.append(self)
        if BIGPLAYER:
          self.rect = pygame.Rect(pos[0], pos[1], 16, 16)
        else:
          self.rect = pygame.Rect(pos[0], pos[1],  8, 16)

class Enemy(Mover):
    difference=0
    maxDiff=5
    direction=1
    ID="Enemy"
    species="giantRat"
    sprite=None
    h=1
    v=0
    color=(255,0,255)
    def __init__(self,x,y,size1,size2,direction,maximum=5,type="random"):
        self.rect=pygame.Rect(x,y,size1,size2)
        if direction not in [-1,1]:
            self.direction=random.choice([-1,1])
        else:
            self.direction=direction
        if maximum<0:
            maximum=random.randrange(6)
        else:
            self.maxDiff=maximum
        if type == "bat":
          self.v = 1
          self.h = 0
        else:
          self.v = 0
          self.h = 1
        if not USERECTS:
          if type == "random":
              self.sprite = orange_images.get_sprite( \
                              random.choice( ["rat","bat"] ), DEBUG )
          else:
              self.sprite = orange_images.get_sprite( type.lower(), DEBUG )

class Spike(Enemy):
    ID="spike"

# Holds the level layout in a list of strings.
class Level(object):
    level = []
    Message=""
    def create(self):
        global walls,player,end_rect,lvlExit,end_rect_offset,tele_rect,camera
        if DEBUG:
          print "Work: Building level"
        # Parse the level string above. W = wall, E = exit
        x = y = 0
        self.Message = ""
        get_message = False
        for row in self.level:
            for col in row:
                if get_message:
                    if col == '\"':
                        if DEBUG:
                            print "Work: Message collection stopped... final \
message:\n\"" + self.Message + "\""
                        get_message = False
                    else:
                        self.Message += col
                    continue
                if col == ";":
                    if DEBUG:
                        print "Comment found--ignoring following text"
                    break
                if col == "W":
                    Wall((x, y))
                if col=="-":
                    Mover((x,y),(1,0))
                if col=="|":
                    Mover((x,y),(0,1))
                if col == "E":
                    end_rect = pygame.Rect(x, y, 16, 16)
                    if not USERECTS:
                      lvlExit = orange_images.get_sprite( "exit", DEBUG )
                    end_rect_offset = 0
                    if DEBUG:
                      print "Event: Place ending object at", x, y
                if col=="A":
                    end_rect = pygame.Rect(x + 4, y, 8, 16)
                    if not USERECTS:
                      lvlExit = orange_images.get_sprite( "end", DEBUG )
                    end_rect_offset = -4
                    if DEBUG:
                      print "Event: Place ending object at", x, y
                if col=="K":
                    key=Key((x,y))
                if col=="R":
                    key=Key((x,y),color="red")
                if col in ["8","*"]:
                    if col=="8":
                        Color="green"
                    else:
                        Color="red"
                    door=Door((x,y),0,-1,color=Color)
                    walls.append(door)
                if col in ["2","@"]:
                    if col=="2":
                        Color="green"
                    else:
                        Color="red"
                    door=Door((x,y),0,1,color=Color)
                    walls.append(door)
                if col in ["4","$"]:
                    if col=="4":
                        Color="green"
                    else:
                        Color="red"
                    door=Door((x,y),-1,0,color=Color)
                    walls.append(door)
                if col in ["6","^"]:
                    if col=="6":
                        Color="green"
                    else:
                        Color="red"
                    door=Door((x,y),1,0,color=Color)
                    walls.append(door)
                if col in ["7","&"]:
                    if col=="7":
                        Color="green"
                    else:
                        Color="red"
                    door=Door((x,y),-1,-1,color=Color)
                    walls.append(door)
                if col in ["9","("]:
                    if col=="9":
                        Color="green"
                    else:
                        Color="red"
                    door=Door((x,y),1,-1,color=Color)
                    walls.append(door)
                if col in ["1","!"]:
                    if col=="1":
                        Color="green"
                    else:
                        Color="red"
                    door=Door((x,y),-1,1,color=Color)
                    walls.append(door)
                if col in ["3","#"]:
                    if col=="3":
                        Color="green"
                    else:
                        Color="red"
                    door=Door((x,y),1,1,color=Color)
                    walls.append(door)
                if col=="T":
                    Portal( (x, y) )
                if col=="t":
                    Destination( (x, y) )
                if col=="P":
                    player.rect.x=x
                    player.rect.y=y
                    if DEBUG:
                      print "Event: Place player object at", x, y
                if col=="M":
                    mine_rect=Enemy(x,y,16,16,2,type="rat")
                    walls.append(mine_rect)
                if col=="k":
                    mine_rect=Enemy(x,y,16,16,2,type="ratking")
                    mine_rect.species = "ratking"
                    walls.append(mine_rect)
                if col=="B":
                    mine_rect=Enemy(x,y,16,16,2,type="bat")
                    walls.append(mine_rect)
                if col=="S":
                    spike=Spike(x,y,16,16,2,type="spike")
                    walls.append(spike)
                if col=="D":
                    tele_rect=pygame.Rect(x,y,16,16)
                if col == '\"':
                    if DEBUG:
                        print "Work: Message found in level; collecting..."
                    get_message = True
                if not get_message:
                    x += 16
            if not get_message:
                y += 16
                x = 0

            if len( self.Message ) > 0:
                global text, textpos, message_delay, font
                text = font.render(self.Message, 1, (255, 128, 0))
                textpos = text.get_rect(centerx=screen.get_width()/2)
                if len( self.Message ) > 10:
                    message_delay = 500 + (10 * (len( self.Message ) - 10))
                else:
                    message_delay = 500
            else:
                global text
                text = None
            
    def __init__(self,lObjects,Message=""):
        global Levels
        self.level=lObjects
        if DEBUG:
          print "Create: Level object"
        self.Message=Message

# Returns a new rect for drawing by the camera's offset.
def translate(rect):
    return pygame.Rect(rect.x - camera.x, rect.y - camera.y, 
        rect.w, rect.h)

#########################################
# Final initializations before mainloop #
#########################################

import orange_levels

levelIndex=0
levels = orange_levels.get_levels( LEVELPATH, DEBUG )
Levels=[]

if DEBUG:
  print "Work: Passing level strings into level list"
for level_string in levels:
    Levels.append( Level( level_string ) )
    
if len( Levels ) <= 0:
  raise SystemExit, "Did not find any valid levels in ./" + LEVELPATH + \
                    "\nCheck ./doc/levels.txt for help"

player = Player() # Create the player

# This is the camera, simply a rect.
camera = pygame.Rect(0, 0, screen.get_width(), screen.get_height())
if DEBUG:
  print "Create: camera"

lvlExit=None
end_rect_offset = 0
player_rect_offset = -4
if BIGPLAYER:
  player_rect_offset = 0

# Build the first level from data
Levels[0].create()

#############
# main loop #
#############

running=True
quitMsg = "Thanks for playing!"

while running:
    global jumpDY,text,message_delay
    
    clock.tick(60)
    
    for e in pygame.event.get():
        if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
            running = False
        elif e.type == pygame.KEYDOWN and e.key == pygame.K_BACKSPACE:
            if DEBUG:
              print "Event: Level reset"
            delete=True
            while delete:
                try:
                    walls.remove(walls[0])
                except:
                    delete=False
            Levels[levelIndex].create()
            jumpDY=0
            player.jump=False
            player.dJump=False
            player.dead = False
    
    # Move the player if an arrow key is pressed
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT]:
        player.move(-2, 0)
    if key[pygame.K_RIGHT]:
        player.move(2, 0)
    if not player.dJump:#Edited to simulate jumping
        if key[pygame.K_UP]:
            if not player.jump:
                player.jump=True#Edited to simulate jumping
                jumpDY=-2.1
                timeBuffer=16
            elif timeBuffer==0:
                player.dJump=True
                jumpDY=-2.1
    player.move(0, jumpDY)
    jumpDY+=0.1

    camera.x=player.rect.x-int(screen.get_width()/2)
    camera.y=player.rect.y-int(screen.get_height()/2)
    
    # Just added this to make it slightly fun ;)
    if player.rect.colliderect(end_rect) or player.rect.colliderect(tele_rect):
        levelIndex+=1
        delete=True
        while delete:
            try:
                walls.remove(walls[0])
            except:
                delete=False
        jumpDY=0
        player.jump=False
        player.dJump=False
        if DEBUG:
          print "Event: Level win"
        if levelIndex < len( Levels ):
          Levels[levelIndex].create()
        else:
          # A special message if you've gotten the sword (the sword doesn't
          # exist yet in the game, so this just displays when you win)
          running = False
          if not getting_help:
              won = True
    
    # Draw the scene
    screen.fill((0, 0, 0))
    for wall in walls:

        # Translate the object's rect to the camera's offset for drawing
        if wall.rect.right >= camera.left \
        and wall.rect.left <= camera.right \
        and wall.rect.bottom >= camera.top \
        and wall.rect.top <= camera.bottom:
            draw=True
        else:
            draw=False
        wall.rect = translate(wall.rect)
        if wall.ID in ["Enemy","Mover"]:
            wall.update()
        if wall.ID != "Destination":
            if USERECTS==True or wall.ID == "Portal":
                pygame.draw.rect(screen,wall.color,wall.rect)
                if wall.ID == "Portal":
                    pygame.draw.rect( screen, (0, 0, 0), \
                    pygame.Rect( wall.rect.x + 4, wall.rect.y + 4, \
                                 wall.rect.w - 8, wall.rect.h - 8 ) )
                if wall.ID == "Enemy":
                    if wall.species == "ratking":
                        pygame.draw.rect( screen, (255, 255, 0), \
                        pygame.Rect( wall.rect.x + 4, wall.rect.y - 4, 8, 4 ) )

            else:
                if wall.ID in ["Door","Key","spike","Enemy"] and draw:
                    if wall.sprite!="HIDDEN":
                        if wall.ID == "Enemy" and wall.species == "ratking":
                            screen.blit(wall.sprite,(wall.rect.x,wall.rect.y - 1))
                        else:
                            screen.blit(wall.sprite,(wall.rect.x,wall.rect.y))
                    else:
                        pygame.draw.rect(screen,(255,255,255),wall.rect)
                elif draw and wall.ID in ["Wall","Mover"]:
                    pygame.draw.rect(screen, (255, 255, 255), wall.rect)

    player.rect=translate(player.rect)
    tele_rect=translate(tele_rect)
    end_rect=translate(end_rect)

    pygame.draw.rect(screen,(255,255,255),tele_rect)
    if USERECTS==False:
        screen.blit(lvlExit,(end_rect.x + end_rect_offset,end_rect.y))
        if not player.dead:
          screen.blit(player.sprite, \
                        (player.rect.x + player_rect_offset,player.rect.y))
        else:
          screen.blit(orange_images.get_sprite( "dead", DEBUG ), \
                        (player.rect.x + player_rect_offset,player.rect.y))
    else:
        pygame.draw.rect(screen,(255,0,0),end_rect)
        if not player.dead:
          pygame.draw.rect(screen,(255,128,0),player.rect)
        else:
          pygame.draw.rect(screen,(255,128,0), \
          pygame.Rect(player.rect.x, player.rect.y+8, 16, 8))

    if player.dead:
      # We are guaranteed by the player's `update' function that `text' here
      # has been set, as has `textpos'
      screen.blit( text, textpos )
    elif text != None and message_delay > 0:
      screen.blit(text,textpos)
      message_delay -= 1

    pygame.display.flip()


    if timeBuffer>0:
        timeBuffer-=1

if won:

    screen.fill((0, 0, 0))

    text = font.render( "Congratulations!", 1, (255, 128, 0) )
    textpos = text.get_rect( centerx = screen.get_width() / 2 )
    textpos.y = 16

    screen.blit( text, textpos )

    text = font.render( "You've recovered the legendary sword", 1, (255, 128, 0) )
    textpos = text.get_rect( centerx = screen.get_width() / 2 )
    textpos.y = 32

    screen.blit( text, textpos )

    text = font.render( "of the Dragon King!", 1, (255, 128, 0) )
    textpos = text.get_rect( centerx = screen.get_width() / 2 )
    textpos.y = 48

    screen.blit( text, textpos )

    text = font.render( "You've reached the end of the game.", 1, (255, 128, 0) )
    textpos = text.get_rect( centerx = screen.get_width() / 2 )
    textpos.y = 80

    screen.blit( text, textpos )

    text = font.render( "Press ESCAPE to finish.", 1, (255, 128, 0) )
    textpos = text.get_rect( centerx = screen.get_width() / 2 )
    textpos.y = 96

    screen.blit( text, textpos )

    text = font.render( "Original game by Philip Pavlick", 1, (255, 128, 0) )
    textpos = text.get_rect( centerx = screen.get_width() / 2 )
    textpos.y = 216

    screen.blit( text, textpos )

    text = font.render( "Special thanks to my family and friends", 1, (255, 128, 0) )
    textpos = text.get_rect( centerx = screen.get_width() / 2 )
    textpos.y = 232

    screen.blit( text, textpos )

    text = font.render( "who got a kick out of this dumb computer game", 1, (255, 128, 0) )
    textpos = text.get_rect( centerx = screen.get_width() / 2 )
    textpos.y = 248

    screen.blit( text, textpos )

    text = font.render( "I wrote ages ago", 1, (255, 128, 0) )
    textpos = text.get_rect( centerx = screen.get_width() / 2 )
    textpos.y = 264

    screen.blit( text, textpos )

    text = font.render( "(seriously, this source code is terrible!)", 1, (255, 128, 0) )
    textpos = text.get_rect( centerx = screen.get_width() / 2 )
    textpos.y = 280

    screen.blit( text, textpos )

    text = font.render( "For more and better games,", 1, (255, 128, 0) )
    textpos = text.get_rect( centerx = screen.get_width() / 2 )
    textpos.y = 312

    screen.blit( text, textpos )

    text = font.render( "check back at my website at", 1, (255, 128, 0) )
    textpos = text.get_rect( centerx = screen.get_width() / 2 )
    textpos.y = 328

    screen.blit( text, textpos )

    text = font.render( "www.pavlick.net", 1, (255, 128, 0) )
    textpos = text.get_rect( centerx = screen.get_width() / 2 )
    textpos.y = 344

    screen.blit( text, textpos )

    text = font.render( "or", 1, (255, 128, 0) )
    textpos = text.get_rect( centerx = screen.get_width() / 2 )
    textpos.y = 360

    screen.blit( text, textpos )

    text = font.render( "swashdev.github.io", 1, (255, 128, 0) )
    textpos = text.get_rect( centerx = screen.get_width() / 2 )
    textpos.y = 376

    screen.blit( text, textpos )

    text = font.render( "Thank you so much for playing!", 1, (255, 128, 0) )
    textpos = text.get_rect( centerx = screen.get_width() / 2 )
    textpos.y = 408

    screen.blit( text, textpos )

    if USERECTS:

        if BIGPLAYER:
            pygame.draw.rect( screen, player.color, \
                    pygame.Rect( screen.get_width() / 2, 144, \
                                 16, 16 ) )
        else:
            pygame.draw.rect( screen, player.color, \
                    pygame.Rect( screen.get_width() / 2, 144, \
                                 8, 16 ) )

        pygame.draw.rect( screen, (255, 0, 0), \
                    pygame.Rect( (screen.get_width() / 2) - 6, 134, \
                                 8, 16 ) )

    else:

        screen.blit( orange_images.get_sprite( "won" ), \
                     pygame.Rect( (screen.get_width() / 2) - 6, 134, \
                                  15, 32 ) )

    pygame.display.flip()

    running = True

    while running:

        for e in pygame.event.get():
            if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                running = False

print quitMsg
