Thank you for downloading Orange Guy's Quest, version 1.1, by Philip Pavlick.

 -- Introduction --
Orange Guy's Quest is an old game project that I wrote while learning to
program in high school.  It was last modified in 2011 and was found again
several years later while I was going through old programming projects.  I
found that I still liked it, so I decided to patch it up and release it to the
world.  Hopefully as time comes I'll have time to further improve upon it.

Version 1.0 and 1.1 both require Python and Pygame, but have no further
dependencies.  If memory serves me correctly they were originally written for
Python 2.7 and should be compatible with this version of Python.  No word yet
on whether it is forwards-compatible with Python 3, but I wouldn't think so.

 -- Rules --
You are Orange Guy.  This game is a platformer inspired by old dungeon
crawlers, so naturally your only objective is to find the down staircase (red)
by opening doors (blue) with keys (green) while avoiding enemies and spikes
(purple).  Along your way you may also encounter golden keys (yellow) which
open hidden doors.

Most of the instructions are given in the first few levels save for one: the
BACKSPACE key is used to restart the level; falling off the level won't do
this for you.  In the classic versions of the game, being killed by an enemy
or a spike will kill the game immediately.

 -- Running the Game --
After you have Python and Pygame installed, you should be able to run Orange
Guy's Quest on any system from within its directory by using the following
command:

 python orange.py

You will first see a license agreement.  Read this if you haven't already, and
then press ENTER to start the game.  Depending on your configuration (see
below) you may also be prompted to choose between fancy Retro pixel graphics
or the original Ancient Atari 2600-style block graphics.

 -- Command-line Options --
The following command line options can be used to configure your game from the
command line.  All of these will override the default configuration (see below)

 -r or -s               Retro or Sprite graphics
 -a or -b               Ancient or Blocky graphics
 -D                     shows Debug output in the terminal

 --levels               The next argument will be the path to a level file
 
For example, if I want my original block-style graphics with debug output and
choosing levels from a fresh batch I've just cooked up, I can use this command:

 python orange.py -b -D --levels new-levels.txt

 -- Configuration --
You can make some configuration changes by altering the source code in
orange.py.  You will find the configuration options after scrolling past the
license information message.

In version 1.1, the WINDOWS configuration setting was added.  This defaults to
False.  If set to True, the game will use a backslash (\) instead of a slash
(/) to go down directory trees.  You shouldn't need to change this, but it's
included "just in case."

The next configuration option is USERECTS.  This defaults to False, which will
give you some pleasing retro pixel art graphics.  If you set USERECTS to True,
it will give you the original block graphics that I used when I first started
coding the game.  Any other value will give a prompt allowing you to choose.

Ostensibly blocky graphics are faster because they don't require reading image
files (aside from images files for the text) but modern computers should be
fast enough to run either version.

There are two additional configuration options in version 1.1: LEVELFILE and
DEBUG.  DEBUG will allow you to see debug output; I do not recommend setting
this to True, as you can enable this using the -D command line option (see
above)

LEVELFILE specifes where the game can find levels.  If you specify a file that
does not exist, the game will complain at you.  You can also specify what
level file to use in the command line options (see above), but this
config flag has been included for those times when you just really don't feel
like typing in the same file name over and over again.
