TEST_CMD = python3 -m doctest

all: test

test:
	$(TEST_CMD) *.py

clean:
	rm -f *.pyc
	rm -rf __pycache__
	rm -rf *.txt
