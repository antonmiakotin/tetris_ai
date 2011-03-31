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
from GameBoard import *
from GameController import *
from Shapes import *

if __name__ == "__main__":
    root = Tk()
    root.title("Tetris Tk")
    theGame = game_controller( root )
    
    root.mainloop()
