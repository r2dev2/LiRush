from dataclasses import asdict, dataclass
from pathlib import Path
from typing import List, Optional, Tuple


@dataclass(order=True)
class Puzzle:
    fen: str
    moves: List[str]
    rating: int
    rating_deviation: int
    popularity: int
    nbplays: int
    themes: List[str]
    game_url: str

    @staticmethod
    def key(puzzle: "Puzzle") -> Tuple[int, int]:
        return (puzzle.rating, puzzle.nbplays)

    @classmethod
    def from_csv_line(cls, line: str) -> "Puzzle":
        (
            _pid,
            fen,
            moves,
            rating,
            rating_deviation,
            popularity,
            plays,
            themes,
            gameurl,
        ) = line.strip().split(",")
        return cls(
            fen,
            moves.split(" "),
            int(rating),
            int(rating_deviation),
            int(popularity),
            int(plays),
            themes.split(" "),
            gameurl,
        )


class PuzzleList(List[Puzzle]):
    def __init__(self, fp: Optional[Path] = None):
        if fp is None:
            fp = Path("./data/lichess_db_puzzle.csv")
        with open(fp, "r") as fin:
            super().__init__(map(Puzzle.from_csv_line, fin))
        self.sort()

    def sort(self, *args, **kwargs):
        super().sort(*args, **kwargs, key=Puzzle.key)
