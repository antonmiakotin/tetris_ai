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
    
    child_boards = [board]
    f = open("output.txt", 'w')   

    for i in range(5):
        for board in child_boards:
            #run states function
            child_states = BoardStates.BoardStates.generate_child_states(board, Shapes.t_shape)
            #sort all boards, highest score first
            child_states = sorted(child_states, key=lambda state: state[0], reverse = True)
            #pick the top 3
            child_states = child_states[:3]
            #output to file
            f.write( "BASE STATE\n" )
            f.write( "#"*30+"\n" )
            f.write( str(board) )
            f.write( "CHILD STATES\n" )
            f.write ( "#"*30+"\n" )
            for state in child_states:
                f.write( str(state[1]) )
            
            
            #since child_states are actually tuples of (score, state)
            child_boards = []
            for tup in child_states:
                #extract all boards from state
                child_boards.append(tup[1].board)

    
    
   

