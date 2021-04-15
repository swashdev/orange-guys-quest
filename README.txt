Thank you for downloading Orange Guy's Quest Classic, by Philip Pavlick.

 -- Introduction --
Orange Guy's Quest is an old game project that I wrote while learning to
program in high school.  It was last modified in 2011 and was found again
several years later while I was going through old programming projects.  I
found that I still liked it, so I decided to patch it up and release it to the
world.  Hopefully as time comes I'll have time to further improve upon it.

Orange Guy's Quest Classic requires Python and Pygame, but has no further
dependencies.  If memory serves me correctly it was originally written for
Python 2.7 and should be compatible with this version of Python.  No word yet
on whether it is forwards-compatible with Python 3, but I wouldn't think so.

 -- Rules --
You are Orange Guy.  This game is a platformer inspired by old dungeon
crawlers, so naturally your only objective is to find the down staircase (red)
by opening doors (blue) with keys (green) while avoiding enemies and spikes
(purple).  Along your way you may also encounter golden keys (yellow) which
open hidden doors.

Most of the instructions are given in the first few levels.  The BACKSPACE key
is used to restart the level; falling off the level won't do this for you.

 -- Running the Game --
After you have Python and Pygame installed, you should be able to run Orange
Guy's Quest on any system from within its directory by using the following
command:

 python orange.py

 -- Command-line Options --
The following command line options can be used to configure your game from the
command line.  All of these will override the default configuration (see below)

 -? or --help           Runs the game with a set of introductory levels rather
 --intro                than the standard or user-defined level set.

 --levels               The next argument will be the path to a level file

 -r or -s               Retro or Sprite graphics
 -a or -b               Ancient or Blocky graphics

 -B                     Activates Big Player mode

 -w or -x               the next argument will be the Width of the window in
                        pixels
 -h or -y               the next argument will be the Height of the window in
                        pixels
 -W                     the next two values will be the game Window's width
                        and height, respectively

 -D                     shows Debug output in the terminal
 
For example, if I want my original block-style graphics with debug output and
choosing levels from a fresh batch I've just cooked up, I can use this command:

 python orange.py -b -D --levels new-levels.txt

If I wanted to run a larger game window so I can see more of the levels at
once, I might use either of these two commands:

 python orange.py -W 800 600
 python orange.py -w 800 -h 600

 -- Configuration --
You can make some configuration changes by altering the source code in
orange.py.  You will find the configuration options after scrolling past the
license information message.

LEVELFILE specifes where the game can find levels.  If you specify a file that
does not exist, the game will complain at you.  You can also specify what
level file to use in the command line options (see above), but this config
flag has been included for those times when you just really don't feel like
typing in the same file name over and over again.

INTROLEVELS contains the path to some introductory levels for players who are
new at the game.  This value can not be changed, but the levels it represents
can be accessed with the -?, --help, or --intro command line options.

USERECTS configures whether what graphics the game will display.  If set to
True, it will give you the original block graphics that I used when I first
started coding the game.  Any other value will give a prompt allowing you to
choose.

WIN_X and WIN_Y set the width and height of the game window, respectively.
Note that the game does not scale the sprites relative to window size; such a
feature was attempted at one point but it made the entire game a framerate
disaster for some reason.

In theory, blocky graphics are faster because they don't require reading image
files (aside from images files for the text) but modern computers should be
fast enough to run either version.

DEBUG will allow you to see debug output; I do not recommend setting
this to True, as you can enable this using the -D command line option (see
above)
