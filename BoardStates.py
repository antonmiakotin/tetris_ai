# This object should be used to generate all possible states
# for a piece to land. Should return a list of optional game
# boards.

from GameBoard import *
from types import *
from Shapes import *
import copy

# Holds the proposed state and the path to get there
class state_and_path:
    def __init__(self, state,path):
        self.state = state
        self.path = path
    def __str__(self):
        return str(self.state) + " " + str(self.path)



class BoardStates:
    @staticmethod
    def generate_child_states(board, piece):
        #get the current state of the board
        parent_state = []
        for k,v in board.landed.iteritems():
            parent_state.append(k)
        
        #if the piece is a square piece
        # if piece is square_shape: 
        child_states = []
        child_path = []
        print board
        
        #if it's a square!
        if piece is square_shape:
            for x in range(board.max_x):
                for y in range(board.max_y):
                    if board.check_block([x,y]) == True and board.check_block([x+1,y]) == True and board.check_block([x+1,y-1]) == True:
                        if board.check_block([x,y+1]) == False or board.check_block([x+1,y+1]) == False:
                            l = copy.deepcopy(parent_state)
                            l.append((x,y))
                            l.append((x+1,y))
                            l.append((x,y-1))
                            l.append((x+1,y-1))
                            child_path = BoardStates.get_left_right_from_int(x, piece)
                            current_state = state_and_path(l,child_path)
                            child_states.append(current_state)
            for s in child_states:
                print s
            return child_states



    #only works for square right now
    @staticmethod
    def get_left_right_from_int(i, piece):
        l = []
        if piece is square_shape:
            if i < 4:
                for i in range (4 - i):
                    l.append("<Left>")
            elif i > 4:
                for i in range ( i-4 ):
                    l.append("<Right>")
        return l

                    #add to state list
        #evaluate all the possible places it could land
        #add them to the state list
        #return the state list

        #if piece is ...

