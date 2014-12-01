first: all

all:

test:
	python3 -m unittest discover -v tests/ '*_test.py'

clean:
	rm -fv parser.out parsetab.py

pep8:
	find . -name '*.py' -exec pep8 -r {} \;
