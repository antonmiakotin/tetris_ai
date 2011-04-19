# This object should be used to generate all possible states
# for a piece to land. Should return a list of optional game
# boards.

from GameBoard import *
from types import *
from Shapes import *
import copy

# Holds the proposed state and the path to get there
class State:
    def __init__(self, board, score, parent):
        self.board = board
        self.score = score
        self. parent = parent
    def __str__(self):
        return "Board:\n" + str(self.board) + "\n" + "Score: " + str(self.score) + "\n"



class BoardStates:
    
    @staticmethod
    def did_shape_land(board, shape):
        #coordinates of all the blocks in a shape
        #need to keep track so we only check the bottom blocks of shape
        blocks_coords = []
        for block in shape.blocks:
            blocks_coords.append(block.coord())
        for block in shape.blocks:
            if block.coord() not in blocks_coords:
                #working with bottom face of shape
                xcoord = block.coord()[0]
                ycoord = block.coord()[1]
                #check_block returns True if piece can be placed there
                #if piece cannot be placed there, it landed, return true
                keep_going = board.check_block(xcoord, ycoord+1)
                if not keep_going:
                    return True
        return False
        
    #returns y-coordinate of bottom most block
    @staticmethod
    def get_bottom_block(shape):
        min_y = -1
        for block in shape.blocks:
            y_temp = block.coord()[1]
            if y_temp > min_y:
                min_y = y_temp
        return min_y
    
    #assigns value to the block's placement
    @staticmethod
    def eval(shape, board):
        # +1 for every touching square, + y-coordinate 
        total_score = 0
        touching_score = 0
        depth_score = 0
        #don't count own blocks as touching        
        already_hit = []
        for block in shape.blocks:
            current = block.coord()
            #print "current:", current
            
            #create tuples of coordinates of blocks to check
            right = (current[0]+1, current[1])
            left = (current[0]-1, current[1])
            #TK coord system is down and to right
            #that's why up and down are reversed
            down = (current[0], current[1]+1)
            up = (current[0], current[1]-1)
            
            right_hit = (right in board.landed)
            left_hit = (left in board.landed)
            up_hit = (up in board.landed)
            down_hit = (down in board.landed)
            
            
            if( right_hit and (right not in already_hit)):
                #print "\tright hit", right
                already_hit.append(right)
                touching_score += 1
            if ( left_hit and (left not in already_hit) ):
                #print "\tleft hit", left
                already_hit.append(left)
                touching_score += 1
            if ( up_hit and (up not in already_hit) ):
                #print "\tup hit", up
                already_hit.append(up)
                touching_score += 1
            if ( down_hit and (down not in already_hit) ):
                #print "\tdown hit", down
                already_hit.append(down)
                touching_score += 1
        depth_score = BoardStates.get_bottom_block(shape)
        '''
        print "\tTouching: ", touching_score
        print "\tDepth: ", depth_score
        print "\tTotal: ", depth_score + touching_score
        print "-"*20
        '''
        return  depth_score + touching_score


    #we probably don't need this method, don't toss yet
    @staticmethod
    def get_width_height(shape):
        min_x = 11
        max_x = -1
        min_y = 22
        max_y = -1
        for block in shape.blocks:
            x = block.coord()[0]
            y = block.coord()[1]
            if x < min_x:
                min_x = x
            if x > max_x:
                max_x = x
            if y < min_y:
                min_y = y
            if y > max_y:
                max_y = y
        return (max_x - min_x + 1, max_y - min_y +1)
    
    
    @staticmethod
    def generate_child_states(board, shape_type):
                
        child_states = []
        
        #move piece down the column
        for x in range(board.max_x):
            score = 0
            shape = shape_type.rel_check_and_create(board, (x,0))
            for y in range(board.max_y):
                #print x,y
                if shape:
                    canmove =  shape.move("down")
                    if not canmove:
                        #print "can't move"
                        child_board = copy.deepcopy(board)
                        score = BoardStates.eval(shape, child_board)
                        child_board.add_shape(shape)
                        child_state = State(child_board, score, board)
                        child_states.append((child_state.score, child_state))
                        break
        child_states = sorted(child_states, key=lambda state: state[0], reverse = True)
        print "BASE STATE"
        print "#"*30
        print board
        print "CHILD STATES"
        print "#"*30
        for state in child_states:
            print state[1]
    

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

