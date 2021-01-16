from server.puzzle import Puzzle, PuzzleList


def test_from_csv_line():
    lines = [
        "0000D,5rk1/1p3ppp/pq3b2/8/8/1P1Q1N2/P4PPP/3R2K1 w - - 2 27,d3d6 f8d8 d6d8 f6d8,1426,500,2,0,advantage endgame short,https://lichess.org/F8M8OS71#53",
        "0009B,r2qr1k1/b1p2ppp/pp4n1/P1P1p3/4P1n1/B2P2Pb/3NBP1P/RN1QR1K1 b - - 1 16,b6c5 e2g4 h3g4 d1g4,1500,500,2,0,advantage middlegame short,https://lichess.org/4MWQCxQ6/black#32",
        "00206,r3kb1r/pppqpn1p/5p2/3p1bpQ/2PP4/4P1B1/PP3PPP/RN2KB1R w KQkq - 1 11,b1c3 f5g4 h5g4 d7g4,1236,500,-5,0,advantage opening short trappedPiece,https://lichess.org/MbJRo6PT#21",
    ]
    correct = [
        Puzzle(
            "5rk1/1p3ppp/pq3b2/8/8/1P1Q1N2/P4PPP/3R2K1 w - - 2 27",
            "d3d6 f8d8 d6d8 f6d8",
            1426,
            500,
            0,
            "advantage endgame short",
            "F8M8OS71#53",
        )
    ]
    assert all(p == c for p, c in zip(map(Puzzle.from_csv_line, lines), correct))


def test_from_csv():
    if "puzzles" not in globals():
        globals()["puzzles"] = PuzzleList()
    assert all(f.rating <= s.rating for f, s in zip(puzzles, puzzles[1:]))


def test_bin_search():
    if "puzzles" not in globals():
        globals()["puzzles"] = PuzzleList()

    regular_use = puzzles.within_rating_range(1600, 1800)
    assert all(1600 <= f.rating <= 1800 for f in regular_use)

    below600 = puzzles.within_rating_range(0, 500)
    assert all(0 <= f.rating <= 500 for f in below600)

    above3500 = puzzles.within_rating_range(3500, 5000)
    assert all(3500 <= f.rating <= 5000 for f in above3500)

    low_rated = puzzles.within_rating_range(600, 800)
    lower_rated = puzzles.within_rating_range(600, 700)
    assert len(low_rated) >= len(lower_rated)
