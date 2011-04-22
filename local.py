import GameBoard
import Util
import Shapes
from random import choice
import State


if __name__ == "__main__":
    #for now controller doesn't do anything
    #do all work manually
    
    #create game board, fill with some squares to test eval
    board = GameBoard.Board()
    
    #fill in the bottom row
    for x in range (20):
        board.landed.append((x,19))
    #throw some more random blocks
    board.landed.append((3,18))
    board.landed.append((2,18))
    board.landed.append((7,18))
    board.landed.append((7,17))
    
    f = open("output.txt", 'w')   

    shape_classes = [Shapes.square_shape, Shapes.t_shape, Shapes.l_shape, Shapes.reverse_l_shape, Shapes.i_shape]
    random_pieces = []
    #pic random pieces
    for i in range(10):
        cls = choice(shape_classes)
        random_pieces.append(cls)
    id = (0,0)
    init_state = State.State(id, board, 0, None)
    child_states = [init_state]
    #random_pieces = [Shapes.i_shape]

    for piece in random_pieces:
        
        for i in range(len(child_states)):
            #need to remove root nodes from board list
            state = child_states.pop(i)
            #run states function
            result_tuples = Util.Util.generate_child_states(state, piece)
            
            #sort all boards, highest score first
            result_tuples = sorted(result_tuples, key=lambda state: state[0], reverse = True)
            #pick the top 3
            result_tuples = result_tuples[:2]

            #output to file
            f.write( "BASE STATE\n" )
            f.write( "#"*30+"\n" )
            f.write( str(state) )
            f.write( "CHILD STATES\n" )
            f.write ( "#"*30+"\n" )
            for tup in result_tuples:
                f.write( str(tup[1]) )
                child_states.append(tup[1])
