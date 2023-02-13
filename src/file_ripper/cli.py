import logging
import sys

import click

from exit_codes import ExitCode
from .commands import run_file_ripper_once, run_file_ripper_continuously


@click.group()
def cli():
    pass


@cli.command("exec")
@click.argument("definitions_file", type=click.File("rt"))
@click.option("-fmt", "--format", "definitions_format", type=str, default="json")
@click.option("-ro", "--run-once", "run_once", is_flag=True, default=False)
@click.option("-ti", "--time-interval", "time_interval", type=int, default=5)
def handle_exec(definitions_file, definitions_format, run_once, time_interval):
    if run_once:
        run_file_ripper_once(definitions_file, definitions_format)
    else:
        run_file_ripper_continuously(definitions_file, definitions_format, time_interval)
    return ExitCode.OK


def main(argv=None):
    try:
        return cli(argv)
    except Exception as exc:
        logging.exception("Exception encountered running file-ripper", exc_info=exc)
        return ExitCode.SOFTWARE


if __name__ == "__main__":
    sys.exit(main())
