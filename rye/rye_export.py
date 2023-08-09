from logging import getLogger
from pathlib import Path

REQUIREMENTS_TXT_PATH = "requirements.txt"
REQUIREMENTS_LOCK_PATH = "requirements.lock"


def main() -> None:
    logger = getLogger(__name__)
    requirements_txt: list[str]
    with Path(REQUIREMENTS_LOCK_PATH).open() as f:
        lock = f.readlines()
        requirements_txt = [line for line in lock if not (line.startswith(("-e", "#")) or line == "\n")]

    with Path(REQUIREMENTS_LOCK_PATH).open("w") as fr:
        fr.writelines(requirements_txt)

    logger.info("Exported to requirements.txt!")


if __name__ == "__main__":
    main()
