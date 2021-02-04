import webbrowser

import uvicorn # type: ignore

from server import app


@app.on_event("startup")
def open_lirush() -> None:
    print("Go to http://localhost:42069/play")
    webbrowser.open("http://localhost:42069/play")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=42069, log_level="error")
