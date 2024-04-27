import sys

from loguru import logger

from app.visual import run


def main(args: list[str]) -> None:
    if len(args) < 2:
        logger.error("Не хватает параметров!")

    run(args[1])


if __name__ == "__main__":
    main(sys.argv)
