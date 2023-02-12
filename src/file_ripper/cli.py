import logging
import sys

import click
import signal

from exit_codes import ExitCode


@click.group()
def cli():
    pass


@cli.command("exec")
@click.argument("definitions_file", type=click.File("rt"))
@click.option("-fmt", "--format", "definitions_format", type=str, default="json")
@click.option("-ro", "--run_once", "run_once", is_flag=True, default=False)
def handle_exec(definitions_file, definitions_format, run_once):
    if run_once:
        print("only once")
    else:
        print("continuous")
    return ExitCode.OK


def main(argv=None):
    try:
        return cli(argv)
    except Exception as exc:
        logging.exception("Exception encountered running file-ripper", exc_info=exc)
        return ExitCode.SOFTWARE


if __name__ == "__main__":
    sys.exit(main())
