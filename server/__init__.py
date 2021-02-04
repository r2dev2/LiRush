import random
from pathlib import Path
from typing import List, Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

import server.puzzle as puzzle
import server.utils as utils

public = utils.get_public()

app = FastAPI()
app.mount("/public", StaticFiles(directory=f"{public}"), name="pub")

puzzledb = puzzle.PuzzleList()


@app.get("/puzzles")
async def puzzles(start: int, end: int, pmax: Optional[int]):
    inside_range = puzzledb.within_rating_range(start, end)
    if pmax is None or len(inside_range) <= pmax:
        return [i.to_dict() for i in inside_range]
    return [i.to_dict() for i in random.sample(inside_range, pmax)]


@app.get("/play/")
async def root():
    return FileResponse(f"{public / 'index.html'}")
