"""
The window to show all of the status stuff
"""
FILENAME = 'tetris_games.log'

from Tkinter import *
from Shapes import *

class StatusWindow( Frame ):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.window = Toplevel()
        self.scrollbar = Scrollbar(self.window)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.text = Text(self.window, width=80, height=40)
        self.text.pack()
        self.file = open(FILENAME, 'a')
        self.file.write("********************New Game!********************\n\n")

#checkboxes frame
        self.shape_check_boxes = Frame(self.window)

        self.square_on_off = IntVar()
        self.square_check =  Checkbutton(self.shape_check_boxes, text="square", variable=self.square_on_off)
        self.square_check.select()
        self.square_check.pack(side=LEFT)

        self.t_on_off = IntVar()
        self.t_check =  Checkbutton(self.shape_check_boxes, text="t", variable=self.t_on_off)
        self.t_check.select()
        self.t_check.pack(side=LEFT)

        self.l_on_off = IntVar()
        self.l_check =  Checkbutton(self.shape_check_boxes, text="l", variable = self.l_on_off)
        self.l_check.select()
        self.l_check.pack(side=LEFT)

        self.reverse_l_on_off = IntVar()
        self.reverse_l_check =  Checkbutton(self.shape_check_boxes, text="reverse_l",variable = self.reverse_l_on_off)
        self.reverse_l_check.select()
        self.reverse_l_check.pack(side=LEFT)

        self.z_on_off = IntVar()
        self.z_check =  Checkbutton(self.shape_check_boxes, text="z", variable=self.z_on_off)
        self.z_check.select()
        self.z_check.pack(side=LEFT)

        self.s_on_off = IntVar()
        self.s_check = Checkbutton(self.shape_check_boxes, text="s", variable=self.s_on_off)
        self.s_check.select()
        self.s_check.pack(side=LEFT)

        self.i_on_off = IntVar()
        self.i_check = Checkbutton(self.shape_check_boxes, text="i", variable=self.i_on_off)
        self.i_check.select()
        self.i_check.pack(side=LEFT)

        self.shape_check_boxes.pack()

        #attach the two together
        self.text.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.text.yview)

    def log_text(self, string):

        self.text.insert(END, string + "\n")
        self.text.yview(END)
        self.file.write(string + "\n")
        #add a line if the piece has landed
        if(string == "LANDED"):
            self.text.insert(END, "\n")
            self.file.write("\n")


    def new_shape(self,s):
        if s:
            self.text.insert(END, s.toString() + "\n")
            self.file.write(s.toString() + "\n")

    def log_board(self,b):
        if b:
            self.text.insert(END, b.toString())
            self.file.write(b.toString())

    def get_shapes(self):
        l = []
        if(self.square_on_off.get() == 1): l.append(square_shape)
        if(self.t_on_off.get() == 1): l.append(t_shape)
        if(self.l_on_off.get() == 1): l.append(l_shape)
        if(self.reverse_l_on_off.get() == 1): l.append(reverse_l_shape)
        if(self.z_on_off.get() == 1): l.append(z_shape)
        if(self.s_on_off.get() == 1): l.append(s_shape)
        if(self.i_on_off.get() == 1): l.append(i_shape)

        #if you don't want any shapes, you get them all!!!!! 
        if(l): return l
        else:
            return [square_shape,
                    t_shape,
                    l_shape,
                    reverse_l_shape,
                    z_shape,
                    s_shape,
                    i_shape ]
    def __del__(self):
        self.file.close()
