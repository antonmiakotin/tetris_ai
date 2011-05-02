import GameBoard
import Util
from Shapes import *
from  AggressiveSearch import *
import local
import bfs
import sys

from random import choice
class main(object):

    def __init__(self,parent, argv):
    #create game board, fill with some squares to test eval
        self.board = GameBoard.Board( parent )

    #throw some more random blocks
    # board.landed.append((3,18))
    # board.landed.append((2,18))
    # board.landed.append((4,18))
    # board.landed.append((5,18))
    # board.landed.append((6,18))
    # board.landed.append((7,18))
    # board.landed.append((8,18))
    # board.landed.append((9,18))
    # board.landed.append((7,17))
    
#    f = open("output.txt", 'w')   
        self.parent = parent
        self.argv = argv
        init_state = State.State(id, self.board, 0, None)
        child_states = [init_state]
        self.after_id = self.parent.after( 0, self.run )
    
    def run(self):
    #run the game in file input mode
        if(len(self.argv) > 1):
            if ("-L" in self.argv) or ("-l" in self.argv):    # not that clever, just pass -L as the first argument
                # and the filename as the second
                print self.argv[2]
                fptr = open(self.argv[2], 'r')
                lines = fptr.readlines()
                fptr.close()
                pieces = shape.list_from_str_list(lines)
                loc = local.local(self.board, pieces)
                
            elif "-A" in self.argv:
                fptr = open(self.argv[2], 'r')
                lines = fptr.readlines()
                fptr.close()
                pieces = shape.list_from_str_list(lines)
                a = AggressiveSearch(self.board, pieces, int(self.argv[3]), int(self.argv[4]), int(self.argv[5]))

            elif ("-B" in self.argv) or ("-b" in self.argv):
                fptr = open(self.argv[1], 'r')
                lines = fptr.readlines()
                fptr.close()
                pieces = shape.list_from_str_list(lines)
                # $> python main.py -b <game_file> <max_tree_depth> <branching_factor>
                if len(self.argv) >= 5:
                    bfs.run(self.board, pieces, int(self.argv[2]), int(self.argv[3]))
                elif len(self.argv) == 4:
                    bfs.run(self.board, pieces, int(self.argv[2]))
                else:
                    bfs.run(self.board, pieces)
        else:
            print "Usage -[LAB] [filename].tgame"


    # This shoudl all be moved to LocalSearch.py or something like that
    # for piece in random_pieces:
        
    #     for i in range(len(child_states)):
    #         #need to remove root nodes from board list
    #         state = child_states.pop(i)
    #         #run states function
    #         result_tuples = BoardStates.BoardStates.generate_child_states(state, piece)
            
    #         #sort all boards, highest score first
    #         result_tuples = sorted(result_tuples, key=lambda state: state[0], reverse = True)
    #         #pick the top 3
    #         result_tuples = result_tuples[:30]
    #         #output to file
    #         f.write( "BASE STATE\n" )
    #         f.write( "#"*30+"\n" )
    #         f.write( str(state) )
    #         f.write( "CHILD STATES\n" )
    #         f.write ( "#"*30+"\n" )
    #         for tup in result_tuples:
    #             f.write( str(tup[1]) )
    #             child_states.append(tup[1])
            

    
    
   

