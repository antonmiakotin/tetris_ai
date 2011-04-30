import os, sys

system_call = ""

for i in range ( 10 ):
    for j in range( 20 ):
        for k in range(j):
            system_call = "python main.py -A " + str(i) + "rg.tgame " + str(k) + " " + str(j) + " " + str(i)
            os.system(system_call)
