import Shapes
from random import choice

shape_classes = [Shapes.square_shape, Shapes.t_shape, Shapes.l_shape, Shapes.reverse_l_shape, Shapes.i_shape]
random_pieces = []
    #pic random pieces
for i in range(10):
    fptr = open(str(i) + "rg.tgame","w")
    for j in range(100):
        cls = choice(shape_classes)
        fptr.write(str(cls)[15:-2] + "\n")



