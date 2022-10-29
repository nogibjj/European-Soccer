install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

format:
	find . -name '*.py' | xargs black

lint:
	find . -name '*.py' | xargs pylint --output-format=colorized --disable=R,C,W1203,W1202,W1514
test:

all: install format lint test
