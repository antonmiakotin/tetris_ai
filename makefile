<<<<<<< HEAD
#This is a makefile
run:
	python Tetris.py
=======
runa: clean
	python main.py -A 0rg.tgame 5 9 0 

runl: clean
	python main.py -L 0rg.tgame

runb: clean
	python main.py -B 0rg.tgame
>>>>>>> removeTK

clean:
	rm -f *~
	rm -f *.pyc
