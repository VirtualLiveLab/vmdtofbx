from utils.file import get_cwd, glob_files


class CogLoader:
    def __init__(self, directory: str) -> None:
        self._cwd = get_cwd()
        self._cog_path = self._cwd / directory

    def glob_cog(self, file_name: str, /, *, as_relative: bool = False) -> list[str]:
        cogs = list(glob_files(self._cog_path, file_name))
        if as_relative:
            cogs = [path.relative_to(self._cwd) for path in cogs]

        return [f.as_posix().removesuffix(f.suffix).replace("/", ".") for f in cogs]
