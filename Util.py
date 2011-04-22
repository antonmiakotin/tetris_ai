# This object should be used to generate all possible states
# for a piece to land. Should return a list of optional game
# boards.

from GameBoard import *
from types import *
import Shapes
import copy
import State

class Util:
    
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
        #bottom and sides count
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
            
            right_hit = ((right in board.landed) or (right[0] > board.max_x))
            left_hit = ((left in board.landed) or (left[0] < 0))
            up_hit = (up in board.landed)
            down_hit = ((down in board.landed) or (down[1] > board.max_y))
            
            
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
        depth_score = Util.get_bottom_block(shape)
        '''
        print "\tTouching: ", touching_score
        print "\tDepth: ", depth_score
        print "\tTotal: ", depth_score + touching_score
        print "-"*20
        '''
        return  depth_score + touching_score


    
    @staticmethod
    def generate_child_states(state, shape_type):
        state.id = (state.id[0]+1, state.id[1])
        board = state.board
        print shape_type
        child_states = []
        num_rotate = 1
        if shape_type == Shapes.t_shape:
            num_rotate = 4
        elif shape_type == Shapes.z_shape or shape_type == Shapes.s_shape:
            num_rotate = 2
        elif shape_type == Shapes.l_shape or shape_type == Shapes.reverse_l_shape:
            num_rotate = 4
        elif shape_type == Shapes.i_shape:
            num_rotate = 2
        print str(num_rotate)
        
        id = 1
        


        #move back tomorrow
        for i in range(num_rotate):

            # This is a total hack, but works
            can_move_right = True

            #move piece down the column
            for x in range(board.max_x):

                if not can_move_right:
                    # stop evaluating
                    # you are about to repeat yourself
                    break

                score = 0
                #actually create a piece from the class that was passed in
                #starting at y=3, otherwise pieces don't have room to rotate
                shape = shape_type.rel_check_and_create(board, (0,3))

                #rotate shape to needed orientation
                if shape:
                    for j in range(i):
                        print "rotating clockwise"
                        shape.rotate()
    
                # Need to rotate the shape before moving it
                for z in range(x):
                    # keep track of this to pull us out of loop 
                    can_move_right = shape.move("right")

                for y in range(3,board.max_y):

                    #check to see that a piece can be created at the coordinate
                    if shape:
                        canmove =  shape.move("down")
                        if not canmove:
                            #either we've hit a piece or we've hit the bottom
                            #make a copy of the board
                            child_board = copy.deepcopy(board)

                            #calculate the score
                            score = Util.eval(shape, child_board)

                            #add the current piece to the 'landed' array of board
                            child_board.add_shape(shape)

                            #create a state that includes child board, the score and the parent board
                            #create child id
                            child_id = (state.id[0], id)

                            #increment id
                            id += 1
                            child_state = State.State(child_id, child_board, score, board)

                            #append a tuple that includes the score so we can sort
                            child_states.append((child_state.score, child_state))
                            print "stopped at: ", x,y
                            print "return state: ", child_id
                            break
        return child_states
    
