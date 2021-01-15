import random
from typing import List, Optional

from fastapi import FastAPI

import server.puzzle as puzzle

app = FastAPI()
puzzledb = puzzle.PuzzleList()


@app.get("/puzzles")
async def puzzles(start: int, end: int, pmax: Optional[int]) -> List[puzzle.Puzzle]:
    inside_range = puzzledb.within_rating_range(start, end)
    if pmax is None:
        return inside_range
    return random.sample(inside_range, pmax)


@app.get("/")
async def root():
    return {"message": "Hello World"}
