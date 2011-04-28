#!/usr/bin/env python
from Tkinter import *
"""
Holds the UI elements for the board game
"""

LEFT = "left"
RIGHT = "right"
DOWN = "down"

direction_d = { "left": (-1, 0), "right": (1, 0), "down": (0, 1) }


class Board( Frame ):
    """
    The board represents the tetris playing area. A grid of x by y blocks.
    """
    def __init__(self, parent, scale=20, max_x=10, max_y=20, offset=3):
        """
        Init and config the tetris board, default configuration:
        Scale (block size in pixels) = 20
        max X (in blocks) = 10
        max Y (in blocks) = 20
        offset (in pixels) = 3
        """
        Frame.__init__(self,parent)

        # blocks are indexed by there corrdinates e.g. (4,5), these are
        self.landed = []
        self.landed_tk = {}
        self.parent = parent
        self.scale = scale
        self.max_x = max_x
        self.max_y = max_y
        self.offset = offset
        self.canvas = Canvas(parent, 
                             height=(max_y * scale) + offset,
                             width= (max_x * scale) + offset)
        self.canvas.pack()
        self.offset = offset
        #last piece that was added to the landed list 
        self.last_piece = None

    def check_for_complete_row( self, blocks ):
        """
        Look for a complete row of blocks, from the bottom up until the top row
        or until an empty row is reached.
        """
        
        # Add the blocks to those in the grid that have already landed
        for block in blocks:
            self.landed_tk[ block.coord() ] = block.id

        rows_deleted = 0
                
        empty_row = 0

        # find the first empty row
        for y in xrange(self.max_y -1, -1, -1):
            row_is_empty = True
            for x in xrange(self.max_x):
                if self.landed_tk.get((x,y),None):
#                if (x,y) in self.landed:
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
                if self.landed_tk.get((x,y),None) is None:
#                if not ((x,y) in self.landed):
                    complete_row = False
                    break;

            if complete_row:
                rows_deleted += 1
                
                #delete the completed row
                for x in xrange(self.max_x):
                    block = self.landed_tk.pop((x,y))
                    self.delete_block(block)
                    del block
                    self.landed.remove((x,y))

                    
                # move all the rows above it down
                for ay in xrange(y-1, empty_row, -1):
                    for x in xrange(self.max_x):
                        block = self.landed_tk.get((x,ay),None)
                        if block:
                            block = self.landed_tk.pop((x,ay))
                            dx,dy = direction_d[DOWN]
                            self.move_block(block, direction_d[DOWN])
                            self.landed_tk[(x+dx, ay+dy)] = block

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
        #return (100 * rows_deleted) * rows_deleted
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
        elif self.landed_tk.has_key( (x,y) ): 
            return False
        else:
            return True

    def add_block( self, (x, y), colour):
        """
        Create a block by drawing it on the canvas, return
        it's ID to the caller.
        """
        rx = (x * self.scale) + self.offset
        ry = (y * self.scale) + self.offset
        
        return self.canvas.create_rectangle(
            rx, ry, rx+self.scale, ry+self.scale, fill=colour
        )
        
    def move_block( self, id, coord):
        """
        Move the block, identified by 'id', by x and y. Note this is a
        relative movement, e.g. move 10, 10 means move 10 pixels right and
        10 pixels down NOT move to position 10,10. 
        """
        x, y = coord
        self.canvas.move(id, x*self.scale, y*self.scale)
        
    def delete_block(self, id):
        """
        Delete the identified block
        """
        self.canvas.delete( id )
