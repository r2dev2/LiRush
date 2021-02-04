import sys
from pathlib import Path


def get_public() -> Path:
    try:
        return Path(sys._MEIPASS) / "public"
    except AttributeError:
        return Path(__file__).resolve().parent / "../client/public"


def get_puzzle_csv() -> Path:
    try:
        return Path(sys._MEIPASS) / "data/lichess_db_puzzle.csv"
    except AttributeError:
        return Path("./data/lichess_db_puzzle.csv")
