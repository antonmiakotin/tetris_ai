# This method takes a board, a file with a list of pieces, and a threshold.
# While it plays it will not consider states where lines have been created
# in order to try and create a tetris every time it clears lines thus scoring
# the most points
# Stephen Kalpin
from  Util import *
import time
import sys

debug = False
pictures = False


# Method runs the algorithm
class AggressiveSearch:

    def __init__(self,board,piece_list,hi_threshold,low_threshold,game = 0):
        self.board = board
        self.parent = board.parent
        self.piece_list = piece_list
        self.hi_threshold = hi_threshold
        self.low_threshold = low_threshold
        self.game = game
        self.count = 0
        self.score = 0
        self.id = (0,0)
        self.init_state = State.State(self.id, board, 0, None)
        self.current_threshold = hi_threshold
        self.current_piece = 0
        self.board.pack_tk()
        self.tetris_count = 0

        self.after_id = self.parent.after( 0, self.run)        

    def run( self ):
        if len(self.piece_list) > self.current_piece:
            piece = self.piece_list[self.current_piece]
            # first grab the first set of states given the parent state
            state_tuples = Util.generate_child_states(self.init_state, piece)

            
            
            # You just lost the self.game
            # ****************************************
            if len(state_tuples) == 0:
                if debug == True:
                    print "lost self.game"
                Toplevel().quit()
                self.board.parent.quit()
                print str(self.game) + "," + str(self.hi_threshold) + "," + str(self.low_threshold) + "," + str(self.score) + "," + str(self.tetris_count) + "," + str(self.count)
                sys.exit(0)
                return

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
            if under_current_threshold(self.current_threshold, state_tuples[0][1].board.landed):
                if debug == True:
                    print "current mode: only tetrises"
                self.current_threshold = self.hi_threshold
                if len(lines_list_4) != 0:
                    self.init_state = lines_list_4[0][1]
                    self.tetris_count += 1

                elif len(lines_list_0) != 0:
                    self.init_state = lines_list_0[0][1]

                elif len(lines_list_3) != 0:
                    self.init_state = lines_list_3[0][1]

                elif len(lines_list_2) != 0:
                    self.init_state = lines_list_2[0][1]

                elif len(lines_list_1) != 0:
                    self.init_state = lines_list_1[0][1]

            else:
                self.current_threshold = self.low_threshold
                if debug == True:
                    print "current mode: knock it down"
                if len(lines_list_4) != 0:
                    self.init_state = lines_list_4[0][1]
                elif len(lines_list_3) != 0:
                    self.init_state = lines_list_3[0][1]
                elif len(lines_list_2) != 0:
                    self.init_state = lines_list_2[0][1]
                elif len(lines_list_1) != 0:
                    self.init_state = lines_list_1[0][1]
                elif len(lines_list_0) != 0:
                    self.init_state = lines_list_0[0][1]

            
            self.count += 1
            self.score = self.init_state.game_score
            if debug == True:
                print self.init_state.board
                time.sleep(.5)
            # loop back and grab the next piece
            # self.board = self.init_state.board
            # self.board.pack(side=BOTTOM)
            # self.board.focus()
            if pictures == True:
                self.board.save_tk()
            self.board.canvas.delete(ALL)
            for coord in self.init_state.board.landed:
                self.board.add_block(coord, "blue")

            for block in self.init_state.board.last_piece.blocks:
                if block.coord() in self.init_state.board.landed:
                    self.board.add_block(block.coord(),"red")

            self.current_piece += 1
            self.after_id = self.parent.after( 1, self.run )
            
        else:
            Toplevel().quit()
            self.board.parent.quit()
            # print the state of the last board after everything is done
            print str(self.game) + "," + str(self.hi_threshold) + "," + str(self.low_threshold) + "," + str(self.score) + "," + str(self.tetris_count) + "," + str(self.count)
            sys.exit(0)

def under_current_threshold(current_threshold, coord_list):
    y = 20
    for coord in coord_list:
        if coord[1] < y:
            y = coord[1]
    return y > current_threshold

