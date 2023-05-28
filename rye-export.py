REQUIREMENTS_TXT_PATH = "requirements.txt"
REQUIREMENTS_LOCK_PATH = "requirements.lock"


def main():
    requirements_txt: list[str]
    with open(REQUIREMENTS_LOCK_PATH) as f:
        lock = f.readlines()
        requirements_txt = [line for line in lock if not (line.startswith("-e") or line.startswith("#") or line == "\n")]

    with open(REQUIREMENTS_TXT_PATH, "w") as fr:
        fr.writelines(requirements_txt)


if __name__ == "__main__":
    main()
