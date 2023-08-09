import json
from pathlib import Path
from typing import Any


def get_cwd() -> Path:
    return Path.cwd()


def read_json(filename: str) -> dict[str, Any]:
    path = get_cwd() / filename
    with path.open(mode="r") as f:
        return json.load(f)


def remove_file_extension(filename: str) -> str:
    return filename.removesuffix(Path(filename).suffix)


def write_log(filename: str, data: str, *, append: bool = True) -> None:
    m = "a" if append else "w"
    with Path(filename).open(mode=m) as f:
        f.write(data)
        return
