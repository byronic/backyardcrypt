# Taken from http://code.activestate.com/recipes/134892-getch-like-unbuffered-character-reading-from-stdin/
#  on 10 May 2012
#
# Only aesthetic modifications were made by Byron
#
# C++/Borland conio.h style getch() -- does not print the character to screen, great for menus
# TODO: test on Windows; Byron has already tested on linux

#   USAGE EXAMPLE:
#    in the file needing to call getch:
#1. from __getch import getch

#2. print "getch testing"
#3. k = "z"
#4. while k != "q":
#5. 	k = getch()
#6.	print k
#
#   EXAMPLE 2:
#
#   from __getch import getch
#
#   # more code ...
#   print "Press any key to continue..."
#   getch()


class _getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""
    def __init__(self):
        try:
            self.impl = _getchWindows()
        except ImportError:
            self.impl = _getchUnix()

    def __call__(self): return self.impl()


class _getchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _getchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()


getch = _getch()
