#!/usr/bin/env python
"""
contains all of the definitions needed for a block, and creating
the different tetris shapes

"""
LEFT = "left"
RIGHT = "right"
DOWN = "down"

direction_d = { "left": (-1, 0), "right": (1, 0), "down": (0, 1) }

class Block(object):
    def __init__( self, id, (x, y)):
        self.id = id
        self.x = x
        self.y = y
        
    def coord( self ):
        return (self.x, self.y)
        
class shape(object):
    """
    Shape is the  Base class for the game pieces e.g. square, T, S, Z, L,
    reverse L and I. Shapes are constructed of blocks. 
    """
    @classmethod        
    def check_and_create(cls, board, coords, colour ):
        """
        Check if the blocks that make the shape can be placed in empty coords
        before creating and returning the shape instance. Otherwise, return
        None.
        """
        for coord in coords:
            if not board.check_block( coord ):
                return None
        
        return cls( board, coords, colour)
    
    def __str__(self):
        return "SHAPE"
            
    def __init__(self, board, coords, colour ):
        """
        Initialise the shape base.
        """
        self.board = board
        self.blocks = []
        
        for coord in coords:
            block = Block(self.board.add_block( coord, colour), coord)
            
            self.blocks.append( block )

    def move( self, direction ):
        """
        Move the blocks in the direction indicated by adding (dx, dy) to the
        current block coordinates
        """
        d_x, d_y = direction_d[direction]
        
        for block in self.blocks:

            x = block.x + d_x
            y = block.y + d_y
            
            if not self.board.check_block( (x, y) ):
                return False
            
        for block in self.blocks:
            
            x = block.x + d_x
            y = block.y + d_y
            
            self.board.move_block( block.id, (d_x, d_y) )
            
            block.x = x
            block.y = y
        
        return True
            
    def rotate(self, clockwise = True):
        """
        Rotate the blocks around the 'middle' block, 90-degrees. The
        middle block is always the index 0 block in the list of blocks
        that make up a shape.
        """
        # TO DO: Refactor for DRY
        middle = self.blocks[0]
        rel = []
        for block in self.blocks:
            rel.append( (block.x-middle.x, block.y-middle.y ) )
            
        # to rotate 90-degrees (x,y) = (-y, x)
        # First check that the there are no collisions or out of bounds moves.
        for idx in xrange(len(self.blocks)):
            rel_x, rel_y = rel[idx]
            if clockwise:
                x = middle.x+rel_y
                y = middle.y-rel_x
            else:
                x = middle.x-rel_y
                y = middle.y+rel_x
            
            if not self.board.check_block( (x, y) ):
                return False
            
        for idx in xrange(len(self.blocks)):
            rel_x, rel_y = rel[idx]
            if clockwise:
                x = middle.x+rel_y
                y = middle.y-rel_x
            else:
                x = middle.x-rel_y
                y = middle.y+rel_x
            
            
            diff_x = x - self.blocks[idx].x 
            diff_y = y - self.blocks[idx].y 
            
            self.board.move_block( self.blocks[idx].id, (diff_x, diff_y) )
            
            self.blocks[idx].x = x
            self.blocks[idx].y = y
       
        return True

    @staticmethod
    def list_from_str_list(lines):
        lst = []
        for line in lines:
            if line == "square_shape\n":
                lst.append(square_shape)
            elif line == "t_shape\n":
                lst.append(t_shape)
            elif line == "l_shape\n":
                lst.append(l_shape)
            elif line == "reverse_l_shape\n":
                lst.append(reverse_l_shape)
            elif line == "z_shape\n":
                lst.append(z_shape)
            elif line == "s_shape\n":
                lst.append(s_shape)
            elif line == "i_shape\n":
                lst.append(i_shape)

        return lst

class shape_limited_rotate( shape ):
    """
    This is a base class for the shapes like the S, Z and I that don't fully
    rotate (which would result in the shape moving *up* one block on a 180).
    Instead they toggle between 90 degrees clockwise and then back 90 degrees
    anti-clockwise.
    """
    def __init__( self, board, coords, colour ):
        self.clockwise = True
        super(shape_limited_rotate, self).__init__(board, coords, colour)
    
    def rotate(self, clockwise=True):
        """
        Clockwise, is used to indicate if the shape should rotate clockwise
        or back again anti-clockwise. It is toggled.
        """
        super(shape_limited_rotate, self).rotate(clockwise=self.clockwise)
        if self.clockwise:
            self.clockwise=False
        else:
            self.clockwise=True
        

class square_shape( shape ):
    @classmethod
    def check_and_create( cls, board ):
        coords = [(4,0),(5,0),(4,1),(5,1)]
        return super(square_shape, cls).check_and_create(board, coords, "red")
        
    def rotate(self, clockwise=True):
        """
        Override the rotate method for the square shape to do exactly nothing!
        """
        pass

    def __str__(self):
        return "square_shape"
        
class t_shape( shape ):
    @classmethod
    def check_and_create( cls, board ):
        coords = [(4,0),(3,0),(5,0),(4,1)]
        return super(t_shape, cls).check_and_create(board, coords, "yellow" )

    def __str__(self):
        return "t_shape"

class l_shape( shape ):
    @classmethod
    def check_and_create( cls, board ):
        coords = [(4,0),(3,0),(5,0),(3,1)]
        return super(l_shape, cls).check_and_create(board, coords, "orange")
    def __str__(self):
        return "l_shape"

class reverse_l_shape( shape ):
    @classmethod
    def check_and_create( cls, board ):
        coords = [(5,0),(4,0),(6,0),(6,1)]
        return super(reverse_l_shape, cls).check_and_create(
            board, coords, "green")
    def __str__(self):
        return "reverse_l_shape"

class z_shape( shape_limited_rotate ):
    @classmethod
    def check_and_create( cls, board ):
        coords =[(5,0),(4,0),(5,1),(6,1)]
        return super(z_shape, cls).check_and_create(board, coords, "purple")
    def __str__(self):
        return "z_shape"

class s_shape( shape_limited_rotate ):
    @classmethod
    def check_and_create( cls, board ):
        coords =[(5,1),(4,1),(5,0),(6,0)]
        return super(s_shape, cls).check_and_create(board, coords, "magenta")
    def __str__(self):
        return "s_shape"

class i_shape( shape_limited_rotate ):
    @classmethod
    def check_and_create( cls, board ):
        coords =[(4,0),(3,0),(5,0),(6,0)]
        return super(i_shape, cls).check_and_create(board, coords, "blue")
    def __str__(self):
        return "i_shape"
