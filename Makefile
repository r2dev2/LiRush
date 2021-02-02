py = python3
pip = ${py} -m pip

all: puzzles client

puzzles: data/lichess_db_puzzle.csv

pyrequirements:
	cat requirements.txt | grep "#" | sed 's/# //g' | $(py) || $(pip) install -r requirements.txt

test: pyrequirements
	$(py) -m mypy .
	$(py) -m pytest server/tests

format: pyrequirements
	$(py) -m black server
	$(py) -m isort server

client/node_modules: client/package.json
	cd client && npm i

client/public/build/.built: client/node_modules client/src/*
	cd client && DEV=1 npm run build
	@touch client/public/build/.built

client: client/public/build/.built

data/lichess_db_puzzle.csv:
	curl -o lichess_db_puzzle.csv.bz2 https://database.lichess.org/lichess_db_puzzle.csv.bz2
	mkdir -p data
	bzip2 -d lichess_db_puzzle.csv.bz2
	mv lichess_db_puzzle.csv data
