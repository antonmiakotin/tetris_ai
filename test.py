import SimpleController
import GameBoard
import BoardStates
import Shapes

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
    
    #run states function
    child_states = BoardStates.BoardStates.generate_child_states(board, Shapes.square_shape)
    #sort all boards, highest score first
    child_states = sorted(child_states, key=lambda state: state[0], reverse = True)

    child_boards = []
    #since child_states are actually tuples of (score, state)
    for tup in child_states:
        #extract all boards from state
        child_boards.append(tup[1].board)
    
    grand_child_states = []
    
        
    grand_child_states = BoardStates.BoardStates.generate_child_states(child_boards[0], Shapes.square_shape)
    grand_child_states = sorted(grand_child_states, key=lambda state: state[0], reverse = True)
    
    
    f = open("output.txt", 'w')
    f.write( "BASE STATE\n" )
    f.write( "#"*30+"\n" )
    f.write( str(child_boards[0]) )
    f.write( "CHILD STATES\n" )
    f.write ( "#"*30+"\n" )
    for state in grand_child_states:
        f.write( str(state[1]) )
