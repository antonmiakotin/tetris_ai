run0: clean
	python main.py -A 0rg.tgame

run1: clean
	python main.py -A 1rg.tgame

run2: clean
	python main.py -A 2rg.tgame

run3: clean
	python main.py -A 3rg.tgame

run4: clean
	python main.py -A 4rg.tgame

run5: clean
	python main.py -A 5rg.tgame

run6: clean
	python main.py -A 6rg.tgame

run7: clean
	python main.py -A 7rg.tgame

run8: clean
	python main.py -A 8rg.tgame

run9: clean
	python main.py -A 9rg.tgame

clean:
	rm -f *~
	rm -f *.pyc
