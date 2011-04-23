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
        id = (0,0)
        init_state = State.State(id, board, 0, None)

        for piece in piece_list:
            # first grab the first set of states given the parent state
            state_tuples = Util.generate_child_states(init_state, piece)
            # sort the states based on score
            state_tuples = sorted(state_tuples, key=lambda state: state[0], reverse = True)


            #hold all of the states to remove
            pruned_states = []

            for state_tuple in state_tuples:
                # if under the threshold
                if under_threshold(threshold, state_tuple[1].board.landed):
                    # remove the ones where less than 4 lines have been created
                    if state_tuple[1].lines_killed < 4 and state_tuple[1].lines_killed != 0:
                        print "removing " + str(state_tuple[1])
                        pruned_states.append(state_tuple)

            # else place the ones where a line has been created to the front
                else:
                    if state_tuple[1].lines_killed > 0:
                        # put it in at the front of the list
                        tmp = state_tuples.pop[state_tuples.index(state_tuple)]
                        state_tuples.insert(0,tmp)

            #yikes we removed everything! undo undo!
            if len(pruned_states) == len(state_tuples):
                #unmark all but the last one because it's the best
                
                pruned_states = pruned_states[:-1]
                
            #remove the ones we marked
            for s in pruned_states:
                state_tuples.remove(s)
                    
            # remove all but the best choice
            if len(state_tuples) != 1:
                state_tuples = state_tuples[:1]

            print "stuff"
            for tup in state_tuples:
                print str(tup[1])

            # make this the choice state. 
            init_state = State.State(id, state_tuples.pop()[1].board, 0, None)
            # loop back and grab the next piece

        # print the state of the last board?

def under_threshold(threshold, coord_list):
    y = 20
    for coord in coord_list:
        if coord[1] < y:
            y = coord[1]
            
    return y > threshold
