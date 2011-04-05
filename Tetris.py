#!/usr/bin/env python
"""
Tetris Tk - A tetris clone written in Python using the Tkinter GUI library.

Controls:
    Left Arrow      Move left
    Right Arrow     Move right
    Down Arrow      Move down
    Up Arrow        Drop Tetronimoe to the bottom
    'a'             Rotate anti-clockwise (to the left)
    'b'             Rotate clockwise (to the right)
    'p'             Pause the game.
"""

from Tkinter import *
import tkMessageBox
import sys
import fileinput
from GameBoard import *
from GameController import *
from Shapes import *

if __name__ == "__main__":
    #run the game in file input mode
    if(len(sys.argv) > 1):
        if sys.argv[1] == "-f":
            argsize = len(sys.argv)
            for i in range(2,argsize):
                fptr = open(sys.argv[i], 'r')
                lines = fptr.readlines()
                root = Tk()
                root.title("Tetris Tk")
                theGame = game_controller(root, lines, i - 1)
                root.mainloop()
        else:
            print "Usage -f [filename] [filename] ..."
    else:
        root = Tk()
        root.title("Tetris Tk")
        theGame = game_controller( root, None )
        
        root.mainloop()
