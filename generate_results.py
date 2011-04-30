import os, sys

system_call = ""

for i in range ( 10 ):
    for j in range( 12,14 ):
        for k in range( 4,6 ):
            system_call = "python main.py -A " + str(i) + "rg.tgame " + str(k) + " " + str(j) + " " + str(i)
            os.system(system_call)
#            print system_call
