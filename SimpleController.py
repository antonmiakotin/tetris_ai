import BoardStates
import GameBoard
import Shapes
from random import choice

class simple_controller:
    
    def __init__(self):
        self.board = GameBoard.Board()
        self.pieces = []
        shape_classes = [Shapes.square_shape, Shapes.t_shape, Shapes.l_shape, Shapes.reverse_l_shape, Shapes.i_shape]
        
        for i in range(10):
            cls = choice(shape_classes)
            self.pieces.append(cls)
            
    def get_board(self):
        return self.board
    def get_pieces(self):
        return self.pieces
    def get_child_states(self):
        print self.board.landed
        BoardStates.BoardStates.generate_child_states(self.board, Shapes.square_shape)
