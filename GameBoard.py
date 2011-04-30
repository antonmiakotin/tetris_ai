#!/usr/bin/env python
"""
Holds the UI elements for the board game
"""

LEFT = "left"
RIGHT = "right"
DOWN = "down"

direction_d = { "left": (-1, 0), "right": (1, 0), "down": (0, 1) }


class Board():
    """
    The board represents the tetris playing area. A grid of x by y blocks.
    """
    def __init__(self, scale=20, max_x=10, max_y=20, offset=3):
        """
        Init and config the tetris board, default configuration:
        Scale (block size in pixels) = 20
        max X (in blocks) = 10
        max Y (in blocks) = 20
        offset (in pixels) = 3
        """
        
        # blocks are indexed by there corrdinates e.g. (4,5), these are
        self.landed = []
        self.scale = scale
        self.max_x = max_x
        self.max_y = max_y
        self.offset = offset  
        #last piece that was added to the landed list 
        self.last_piece = None

    def check_for_complete_row( self ):
        """
        Look for a complete row of blocks, from the bottom up until the top row
        or until an empty row is reached.
        """
        rows_deleted = 0
                
        empty_row = 0

        # find the first empty row
        for y in xrange(self.max_y -1, -1, -1):
            row_is_empty = True
            for x in xrange(self.max_x):
                if (x,y) in self.landed:
                    row_is_empty = False
                    break;
            if row_is_empty:
                empty_row = y
                break

        # Now scan up and until a complete row is found. 
        y = self.max_y - 1
        while y > empty_row:
 
            complete_row = True
            for x in xrange(self.max_x):
                if not ((x,y) in self.landed):
                    complete_row = False
                    break;

            if complete_row:
                rows_deleted += 1
                
                #delete the completed row
                for x in xrange(self.max_x):
                    self.landed.remove((x,y))

                    
                # move all the rows above it down
                for ay in xrange(y-1, empty_row, -1):
                    for x in xrange(self.max_x):
                            if (x,ay) in self.landed:
                                self.landed.remove((x,ay))
                                self.landed.append((x,ay+1))
                # move the empty row down index down too
                empty_row +=1
                # y stays same as row above has moved down.
                
            else:
                y -= 1
                
        #self.output() # non-gui diagnostic
                
        # return the score, calculated by the number of rows deleted.        
        return rows_deleted
                
    def __str__( self ):
        string = ""
        board = self.get_board_state()
       # for i in board:
        #    string = string + str(i) + "\n"
        #return string
        return board
        
            
    def get_board_state(self):
        board_state = ""
        last_piece_coords = []
        if self.last_piece:
            last_piece_coords = self.last_piece.get_coords()
        
        for y in range(self.max_y):
            line = ""
            line += (str(y)+"\t")
            for x in range(self.max_x):
                if ((x,y) in self.landed):
                    if ((x,y) in last_piece_coords):
                        #mark piece that has just landed as + for dbugging
                        line += ("|+")
                    else:
                        line += ("|X")
                else:
                    line += ("|_")
            board_state += (line+"|\n")
        return board_state
    
    def add_shape(self, shape):
        self.last_piece = shape
        for block in shape.blocks:
            self.landed.append(block.coord())
            
    def copy_landed(self):
        new_board = []
        for tup in self.landed:
            new_board.append(tup)
        return new_board    
    
    def check_block( self, (x, y) ):
        """
        Check if the x, y coordinate can have a block placed there.
        That is; if there is a 'landed' block there or it is outside the
        board boundary, then return False, otherwise return true.
        """
        if x < 0 or x >= self.max_x or y < 0 or y >= self.max_y:
            return False
        elif (x,y) in self.landed:
            return False
        else:
            return True
