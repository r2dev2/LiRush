import random
from typing import List, Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import server.puzzle as puzzle

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
puzzledb = puzzle.PuzzleList()


@app.get("/puzzles")
async def puzzles(start: int, end: int, pmax: Optional[int]):
    inside_range = puzzledb.within_rating_range(start, end)
    if pmax is None or len(inside_range) <= pmax:
        return [i.to_dict() for i in inside_range]
    return [i.to_dict() for i in random.sample(inside_range, pmax)]


@app.get("/")
async def root():
    return {"message": "Hello World"}
