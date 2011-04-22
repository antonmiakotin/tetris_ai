from GameBoard import *
from types import *
import Shapes
import copy


# Need how many rows that have been destroyed in this state (0-4)
# Holds the proposed state and the path to get there
class State:
    def __init__(self,id, board, score, parent, game_score = 0, lines_killed = 0):
        #id is a tuple of (row in tree, index from left)
        self.id = id
        self.board = board
        self.score = score				# score from the evaluation of this move
        self.game_score = game_score	# current running score of the game
        self.parent = parent
        self.lines_killed = lines_killed
    def __str__(self):
        return "Board:\n" + "ID: " + str(self.id) + "\n" + str(self.board) + "\n" + "Score: " + str(self.score) + "\n"
