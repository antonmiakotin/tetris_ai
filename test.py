import SimpleController
import GameBoard

if __name__ == "__main__":
    #create controller
    cont = SimpleController.Simple_Controller()
    
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
    #replace the controller's board with this one
    cont.board = board
    
    
    #run states function
    cont.get_child_states()
    
     
