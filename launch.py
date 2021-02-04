import time
import webbrowser

import uvicorn # type: ignore

from server import app


@app.on_event("startup")
def open_lirush() -> None:
    webbrowser.open("http://127.0.0.1:42069/play")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=42069)
