# This method takes a board, a file with a list of pieces, and a threshold.
# While it plays it will not consider states where lines have been created
# in order to try and create a tetris every time it clears lines thus scoring
# the most points
# Stephen Kalpin
from  Util import *

# Method runs the algorithm
class AggressiveSearch:
    @staticmethod
    def run(board, piece_list, hi_threshold, low_threshold):
        count = 0
        score = 0
        # for list of pieces
        id = (0,0)
        init_state = State.State(id, board, 0, None)
        current_threshold = hi_threshold

        for piece in piece_list:
            # first grab the first set of states given the parent state
            state_tuples = Util.generate_child_states(init_state, piece)
            # sort the states based on score
            state_tuples = sorted(state_tuples, key=lambda state: state[0], reverse = True)


            #hold all of the states to remove
            pruned_states = []
            count += 1
            for state_tuple in state_tuples:
                # if under the current_threshold
                if under_current_threshold(current_threshold, state_tuple[1].board.landed):
                    current_threshold = hi_threshold
                    # remove the ones where less than 4 lines have been created
                    if state_tuple[1].lines_killed < 4:
                        if state_tuple[1].lines_killed != 0:
                            pruned_states.append(state_tuple)

            # else place the ones where a line has been created to the front
                else:
                    if state_tuple[1].lines_killed > 0:
                        # choose this state
                        tmp = state_tuple
                        state_tuples.remove(state_tuple)
                        state_tuples.insert(0,tmp)
                        current_threshold = low_threshold


            #yikes we removed everything! undo undo!
            if len(pruned_states) == len(state_tuples):
                #unmark the last one because it's the best
                pruned_states = pruned_states[:-1]
                #we just lost the game
                if len(pruned_states) == 0:
                    print "lost game at piece",count
                    break

                
            #remove the ones we marked
            for s in pruned_states:
                state_tuples.remove(s)
            
            # remove all but the best choice
#            if len(state_tuples) != 1:
            state_tuples = state_tuples[:1]

            #grab the score
            score += state_tuples[0][1].game_score
        
#            if not (len(state_tuples) == 0):
            # make this the choice state. 
#            print state_tuples[0][1].board
            last_board = state_tuples[0][1].board
            init_state = State.State(id, state_tuples.pop()[1].board, 0, None)
                


                
            # loop back and grab the next piece

        # print the state of the last board
        print str(low_threshold) + "," + str(hi_threshold) + "," + str(score) + "," + str(count)

def under_current_threshold(current_threshold, coord_list):
    y = 20
    for coord in coord_list:
        if coord[1] < y:
            y = coord[1]
            
    return y > current_threshold
