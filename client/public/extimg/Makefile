.PHONY: all white black

all: board.svg white black

board.svg:
	curl -s -o board.svg https://lichess1.org/assets/images/board/svg/brown.svg

white:
	@make -C white -j8

black:
	@make -C black -j8
