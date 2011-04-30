# This method takes a board, a file with a list of pieces, and a threshold.
# While it plays it will not consider states where lines have been created
# in order to try and create a tetris every time it clears lines thus scoring
# the most points
# Stephen Kalpin
from  Util import *
import time

debug = True


# Method runs the algorithm
class AggressiveSearch:
    @staticmethod
    def run(board, piece_list, hi_threshold, low_threshold, game = 0):
        count = 0
        score = 0
        # for list of pieces
        id = (0,0)
        init_state = State.State(id, board, 0, None)
        current_threshold = hi_threshold

        for piece in piece_list:
            # first grab the first set of states given the parent state
            state_tuples = Util.generate_child_states(init_state, piece)

            
            
            # You just lost the game
            # ****************************************
            if len(state_tuples) == 0:
                if debug == True:
                    print "lost game"
                break

            #****************************************
            # split the states into 5 different lists
            #****************************************
            lines_list_4 = []
            lines_list_3 = []
            lines_list_2 = []
            lines_list_1 = []
            lines_list_0 = []
            
            for state_tuple in state_tuples:
                if state_tuple[1].lines_killed == 4:
                    lines_list_4.append(state_tuple)
                elif state_tuple[1].lines_killed == 3:
                    lines_list_3.append(state_tuple)
                elif state_tuple[1].lines_killed == 2:
                    lines_list_2.append(state_tuple)
                elif state_tuple[1].lines_killed == 1:
                    lines_list_1.append(state_tuple)
                elif state_tuple[1].lines_killed == 0:
                    lines_list_0.append(state_tuple)

            #sort each of the lists
            lines_list_4 = sorted(lines_list_4, key=lambda state: state[0], reverse = True)
            lines_list_3 = sorted(lines_list_3, key=lambda state: state[0], reverse = True)
            lines_list_2 = sorted(lines_list_2, key=lambda state: state[0], reverse = True)
            lines_list_1 = sorted(lines_list_1, key=lambda state: state[0], reverse = True)
            lines_list_0 = sorted(lines_list_0, key=lambda state: state[0], reverse = True)

            
            #if the current threshold is under the high threshold order them like 4 0 3 2 1
            #then pick the best of those
            if under_current_threshold(current_threshold, state_tuples[0][1].board.landed):
                if debug == True:
                    print "current mode: only tetrises"
                current_threshold = hi_threshold
                if len(lines_list_4) != 0:
                    init_state = lines_list_4[0][1]

                elif len(lines_list_0) != 0:
                    init_state = lines_list_0[0][1]

                elif len(lines_list_3) != 0:
                    init_state = lines_list_3[0][1]

                elif len(lines_list_2) != 0:
                    init_state = lines_list_2[0][1]

                elif len(lines_list_1) != 0:
                    init_state = lines_list_1[0][1]

            else:
                current_threshold = low_threshold
                if debug == True:
                    print "current mode: knock it down"
                if len(lines_list_4) != 0:
                    init_state = lines_list_4[0][1]
                elif len(lines_list_3) != 0:
                    init_state = lines_list_3[0][1]
                elif len(lines_list_2) != 0:
                    init_state = lines_list_2[0][1]
                elif len(lines_list_1) != 0:
                    init_state = lines_list_1[0][1]
                elif len(lines_list_0) != 0:
                    init_state = lines_list_0[0][1]

            
            count += 1
            score = init_state.game_score
            if debug == True:
                print init_state.board
                time.sleep(.5)
            # loop back and grab the next piece

        # print the state of the last board after everything is done
        print str(game) + "," + str(hi_threshold) + "," + str(low_threshold) + "," + str(score) + "," + str(count)

def under_current_threshold(current_threshold, coord_list):
    y = 20
    for coord in coord_list:
        if coord[1] < y:
            y = coord[1]
    return y > current_threshold

