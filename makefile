runa: clean
	python main.py -A 0rg.tgame 3 18 0 

runl: clean
	python main.py -L 0rg.tgame

runb: clean
	python main.py -B 0rg.tgame

clean:
	rm -f *~
	rm -f *.pyc
