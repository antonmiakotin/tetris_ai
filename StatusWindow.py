"""
The window to show all of the status stuff
"""

from Tkinter import *

class StatusWindow( Frame ):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.window = Toplevel(height = 500, width=500)
        self.scrollbar = Scrollbar(self.window)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.text = Text(self.window, width = 80, height = 10)
        self.text.pack()

        #attach the two together
        self.text.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.text.yview)

    def log_text(self, string):
        self.text.insert(END, string)

        

