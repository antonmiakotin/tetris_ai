# This method takes a board, a file with a list of pieces, and a threshold.
# While it plays it will not consider states where lines have been created
# in order to try and create a tetris every time it clears lines thus scoring
# the most points
# Stephen Kalpin
from  Util import *

# Method runs the algorithm
class AggressiveSearch:
    @staticmethod
    def run(board, piece_list, threshold):
        # for list of pieces
        for piece in piece_list:
        
            # first grab the first set of states given the parent state
            id = (0,0)
            init_state = State.State(id, board, 0, None)
            state_tuples = Util.generate_child_states(init_state, piece)
            # sort the states based on score
            state_tuples = sorted(state_tuples, key=lambda state: state[0], reverse = True)

            for state_tuple in state_tuples:
                # if under the threshold
                if under_threshold(threshold, state_tuple[1].board.landed):
                    # remove the ones where less than 4 lines have been created
                    if state_tuple[1].lines_killed < 4:
                        print "removing str(state_tuple[1]"
                        state_tuples.remove(state_tuple)

            # else place the ones where a line has been created to the front
                else:
                    if state_tuple[1].lines_killed > 0:
                        # put it in at the front of the list
                        tmp = state_tuples.pop[state_tuples.index(state_tuple)]
                        state_tuples.insert(0,tmp)
                    
            # remove all but the best 3 choices
            state_tuples
            # if lines have been created calculate the points
            # expand the results on those 3 choices
            # as we want to remove those first
            # loop back and grab the next piece
            #
            # after all pieces have been played
            # return board with highest score


def under_threshold(threshold, coord_list):
    y = 20
    for coord in coord_list:
        if coord[0] < y:
            y = coord[0]
    
            
    return y < threshold
        


    
    
