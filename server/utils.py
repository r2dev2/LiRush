from pathlib import Path


def get_public() -> Path:
    return Path(__file__).resolve().parent / "../client/public"
