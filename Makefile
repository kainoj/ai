TEST_CMD = python3 -m doctest

all: test

test:
	$(TEST_CMD) *.py

zad2:
	python validator.py zad2 python3 ex2.py

zad4:
	python validator.py zad4 python3 ex4.py

clean:
	rm -f *.pyc
	rm -rf __pycache__
	rm -rf *.txt
