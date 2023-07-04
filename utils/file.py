import pathlib


def get_cwd() -> pathlib.Path:
    return pathlib.Path.cwd()


def glob_files(dir: pathlib.Path, file_name: str) -> list[pathlib.Path]:
    return list(dir.glob(f"**/{file_name}"))


def convert_to_cog(path: pathlib.Path) -> str:
    return path.as_posix().removesuffix(path.suffix).replace("/", ".")
