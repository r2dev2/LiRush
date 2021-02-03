files := pawn.png knight.png bishop.png rook.png queen.png king.png

all: ${files}

.SECONDEXPANSION:
${files}: %: $$(%)
	curl -s -o $@ https://raw.githubusercontent.com/r2dev2/WayChess/master/img/black/$@
