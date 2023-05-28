def main():
    requirements_txt: list[str]
    with open("requirements.lock") as f:
        lock = f.readlines()
        requirements_txt = [line for line in lock if not (line.startswith("-e") or line.startswith("#") or line == "\n")]

    with open("requirements.txt", "w") as fr:
        fr.writelines(requirements_txt)


if __name__ == "__main__":
    main()
