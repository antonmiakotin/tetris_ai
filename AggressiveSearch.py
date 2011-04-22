# This method takes a board, a file with a list of pieces, and a threshold.
# While it plays it will not consider states where lines have been created
# in order to try and create a tetris every time it clears lines thus scoring
# the most points
# Stephen Kalpin
from  BoardStates import *

# Method runs the algorithm
class AggressiveSearch:
    @staticmethod
    def run(board, piece_list, threshold):
        # for list of pieces
        for piece in piece_list:
        
            # first grab the first set of states given the parent state
            id = (0,0)
            init_state = State(id, board, 0, None)
            state_tuples = BoardStates.generate_child_states(init_state, piece)

            for state in state_tuples:
                print str(state_tuples[0]) + str(state_tuples[1]) + "\n"

                # order them by points
                # if under the threshold
                # remove the ones where less than 4 lines have been created
                # else place the ones where a line has been created to the front
                # remove all but the best 3 choices
                # if lines have been created calculate the points
                # expand the results on those 3 choices
                # as we want to remove those first
                # loop back and grab the next piece
                #
                # after all pieces have been played
                # return board with highest score
