import GameBoard
import Util
from Shapes import *
from  AggressiveSearch import *
import local
import bfs
import sys

from random import choice
if __name__ == "__main__":
    #create game board, fill with some squares to test eval
    board = GameBoard.Board()
    
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

    init_state = State.State(id, board, 0, None)
    child_states = [init_state]
    
    #run the game in file input mode
    if(len(sys.argv) > 1):
        if ("-L" in sys.argv) or ("-l" in sys.argv):    # not that clever, just pass -L as the first argument
            # and the filename as the second
            fptr = open(sys.argv[2], 'r')
            lines = fptr.readlines()
            fptr.close()
            pieces = shape.list_from_str_list(lines)
            # pass in the board and the file name
            local.run(board, pieces)
        elif "-A" in sys.argv:
            fptr = open(sys.argv[2], 'r')
            lines = fptr.readlines()
            fptr.close()
            pieces = shape.list_from_str_list(lines)
            AggressiveSearch.run(board, pieces, int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])) 

        elif ("-B" in sys.argv) or ("-b" in sys.argv):
            fptr = open(sys.argv[2], 'r')
            lines = fptr.readlines()
            fptr.close()
            pieces = shape.list_from_str_list(lines)
            # $> python main.py -b <game_file> <max_tree_depth> <branching_factor>
            if len(sys.argv) >= 5:
                bfs.run(board, pieces, int(sys.argv[3]), int(sys.argv[4]))
            elif len(sys.argv) == 4:
                bfs.run(board, pieces, int(sys.argv[3]))
            else:
                bfs.run(board, pieces)
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
            

    
    
   

