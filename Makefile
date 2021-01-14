py = python3

all: puzzles

puzzles: data/lichess_db_puzzle.csv

test:
	$(py) -m pytest server/tests

format:
	$(py) -m black server
	$(py) -m isort server

data/lichess_db_puzzle.csv:
	curl -o lichess_db_puzzle.csv.bz2 https://database.lichess.org/lichess_db_puzzle.csv.bz2
	mkdir -p data
	bzip2 -d lichess_db_puzzle.csv.bz2
	mv lichess_db_puzzle.csv data
