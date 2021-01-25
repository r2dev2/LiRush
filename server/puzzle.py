from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from server.wrappers import add_slots


@add_slots
@dataclass(order=True)
class Puzzle:
    fen: str
    moves: str
    rating: int
    rating_deviation: int
    nbplays: int
    themes: str
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
            _popularity,
            plays,
            themes,
            gameurl,
        ) = line.strip().split(",")
        return cls(
            fen,
            moves,
            int(rating),
            int(rating_deviation),
            int(plays),
            themes,
            gameurl[20:],
        )

    def to_dict(self):
        return {k: getattr(self, k) for k in self.__slots__}


class PuzzleList(List[Puzzle]):
    cache: Dict[Path, List[Puzzle]] = dict()

    def __init__(self, fp: Optional[Path] = None):
        if fp is None:
            fp = Path("./data/lichess_db_puzzle.csv")
        try:
            self[:] = self.cache[fp][:]
        except KeyError:
            with open(fp, "r") as fin:
                super().__init__(map(Puzzle.from_csv_line, fin))
            self.sort()
            self.cache[fp] = self
        self.first: Dict[int, int] = dict()
        self.second: Dict[int, int] = dict()
        for i, p in enumerate(self):
            r = p.rating
            self.first[r] = min(self.first.get(r, i), i)
            self.second[r] = max(self.second.get(r, i), i)

    def within_rating_range(self, start: int, end: int) -> List[Puzzle]:
        i_start = self.__binary_search_for_rating(start, False)
        i_end = self.__binary_search_for_rating(end, True)
        i_start = i_start if i_start is not None else 0
        i_end = i_end if i_end is not None else len(self)
        while self.__not_in_between(i_start, start, end):
            i_start += 1
        while self.__not_in_between(i_end, start, end):
            i_end -= 1
        return self[i_start:i_end]

    def sort(self, *args, **kwargs):
        super().sort(*args, **kwargs, key=Puzzle.key)

    def __binary_search_for_rating(
        self, rating: int, is_high: bool = False
    ) -> Optional[int]:
        l = len(self)
        low = 0
        high = l - 1
        mid = 0
        id_map = self.second if is_high else self.first

        while low <= high:
            mid = (high + low) // 2
            if self[mid].rating < rating:
                low = mid + 1
            elif self[mid].rating > rating:
                high = mid - 1
            else:
                return id_map.get(rating, mid)

        if is_high and low <= l:
            return low
        if not is_high and high >= 0:
            return high
        return None

    def __not_in_between(self, idx: int, beg: int, end: int) -> bool:
        try:
            return not beg <= self[idx].rating <= end
        except IndexError:
            return False
