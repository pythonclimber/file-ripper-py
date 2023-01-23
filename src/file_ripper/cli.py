import logging


def cli():
    pass


def main():
    try:
        cli()
    except Exception as exc:
        logging.exception("Exception encountered running file-ripper", exc_info=exc)


if __name__ == "__main__":
    main()
