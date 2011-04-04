#!/usr/bin/env python
"""
Tetris game controller
"""
from GameBoard import *
from Shapes import *
from random import randint
from StatusWindow import *
import tkMessageBox

NO_OF_LEVELS = 10
SCALE = 20
OFFSET = 3
MAXX = 10
MAXY = 22

LEFT = "left"
RIGHT = "right"
DOWN = "down"

direction_d = { "left": (-1, 0), "right": (1, 0), "down": (0, 1) }

def level_thresholds( first_level, no_of_levels ):
    """
    Calculates the score at which the level will change, for n levels.
    """
    thresholds =[]
    for x in xrange( no_of_levels ):
        multiplier = 2**x
        thresholds.append( first_level * multiplier )
    
    return thresholds
    
class game_controller(object):
    """
    Main game loop and receives GUI callback events for keypresses etc...
    """
    def __init__(self, parent):
        """
        Intialise the game...
        """
        self.parent = parent
        self.score = 0
        self.level = 0
        self.delay = 1000    #ms
        
        #lookup table
        self.shapes = [square_shape,
                      t_shape,
                      l_shape,
                      reverse_l_shape,
                      z_shape,
                      s_shape,
                      i_shape ]
        
        self.thresholds = level_thresholds( 500, NO_OF_LEVELS )
        
        self.status_bar = status_bar( parent )
        self.status_bar.pack(side=TOP,fill=X)
        #print "Status bar width",self.status_bar.cget("width")

        self.status_bar.set("Score: %-7d\t Level: %d " % (
            self.score, self.level+1)
        )
        #create the status window
        self.status_window = StatusWindow(parent)
        self.status_window.pack()

        #create the game board
        self.board = Board(
            parent,
            scale=SCALE,
            max_x=MAXX,
            max_y=MAXY,
            offset=OFFSET
            )
        
        self.board.pack(side=BOTTOM)
        self.board.focus()
        

        self.parent.bind("<Left>", self.left_callback)
        self.parent.bind("<Right>", self.right_callback)
        self.parent.bind("<Up>", self.up_callback)
        self.parent.bind("<Down>", self.down_callback)
        self.parent.bind("a", self.a_callback)
        self.parent.bind("s", self.s_callback)
        self.parent.bind("p", self.p_callback)
        
        self.shape = self.get_next_shape()
        #self.board.output()

        self.after_id = self.parent.after( self.delay, self.move_my_shape )
        
    def handle_move(self, direction):
        #if you can't move then you've hit something
        if not self.shape.move( direction ):
            self.status_window.log_text("HIT")
            # if your heading down then the shape has 'landed'
            if direction == DOWN:
                self.score += self.board.check_for_complete_row(
                    self.shape.blocks
                    )
                del self.shape
                self.status_window.log_text("LANDED")
                self.shape = self.get_next_shape()

                # If the shape returned is None, then this indicates that
                # that the check before creating it failed and the
                # game is over!
                if self.shape is None:
                    self.status_window.log_text("GAME OVER!")
                    tkMessageBox.showwarning(
                        title="GAME OVER",
                        message ="Score: %7d\tLevel: %d\t" % (
                            self.score, self.level),

                        )
                    Toplevel().destroy()
                    self.parent.destroy()
                    sys.exit(0)
                
                # do we go up a level?
                if (self.level < NO_OF_LEVELS and 
                    self.score >= self.thresholds[ self.level]):
                    self.level+=1
                    self.delay-=100
                    
                self.status_bar.set("Score: %-7d\t Level: %d " % (
                    self.score, self.level+1)
                )
                
                # Signal that the shape has 'landed'
                return False
        return True

    def left_callback( self, event ):
        if self.shape:
            self.status_window.log_text("LEFT")
            self.handle_move( LEFT )
        
    def right_callback( self, event ):
        if self.shape:
            self.status_window.log_text("RIGHT")
            self.handle_move( RIGHT )

    def up_callback( self, event ):
        if self.shape:
            # drop the tetrominoe to the bottom
            while self.handle_move( DOWN ):
                pass

    def down_callback( self, event ):
        if self.shape:
            self.status_window.log_text("DOWN")            
            self.handle_move( DOWN )
            
    def a_callback( self, event):
        if self.shape:
            self.shape.rotate(clockwise=True)
            self.status_window.log_text("ROTATE CLOCKWISE")           
            
    def s_callback( self, event):
        if self.shape:
            self.shape.rotate(clockwise=False)
            self.status_window.log_text("ROTATE COUNTERCLOCKWISE")           
        
    def p_callback(self, event):
        self.parent.after_cancel( self.after_id )
        tkMessageBox.askquestion(
            title = "Paused!",
            message="Continue?",
            type=tkMessageBox.OK)
        self.after_id = self.parent.after( self.delay, self.move_my_shape )
    
    def move_my_shape( self ):
        if self.shape:
            self.handle_move( DOWN )
            self.after_id = self.parent.after( self.delay, self.move_my_shape )
        
    def get_next_shape( self ):
        """
        Randomly select which tetrominoe will be used next.
        """
        the_shape = self.shapes[ randint(0,len(self.shapes)-1) ]
        self.status_window.new_shape(the_shape)
        return the_shape.check_and_create(self.board)