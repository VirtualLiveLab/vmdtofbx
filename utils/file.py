import pathlib


def glob_files(dir: str, path: str) -> list[pathlib.Path]:
    p = pathlib.Path(dir)
    return list(p.glob(f"**/{path}"))


def get_cog_path(path: pathlib.Path) -> str:
    return path.as_posix().removesuffix(path.suffix).replace("/", ".")
