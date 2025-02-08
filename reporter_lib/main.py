import argparse
import asyncio
import logging
import os

from reporter_lib.csv_reporters.reporter_abstraction import ReporterAbstract
from reporter_lib.utils import setup_logger


async def main() -> None:
    description = "Exporting Report from events"
    parser = argparse.ArgumentParser(
        description=description,
        add_help=True,
    )

    # required arguments
    parser.add_argument(
        "input-file",
        type=str,
        default=False,
        help="Input file to test with",
    )

    parser.add_argument(
        "export_type",
        type=str,
        choices=[subclass.__name__ for subclass in ReporterAbstract.__subclasses__()],
        help="Choose export type between available ones",
    )

    # optional arguments
    parser.add_argument(
        "-p",
        "--production",
        type=bool,
        default=False,
        help="boolean indicating whether to use production settings",
    )

    args = parser.parse_args()

    logger = setup_logger(log_level=logging.DEBUG if args.production else logging.INFO)

    if not os.path.exists(args.input_file):
        logger.error(f"Input file {args.input_file} does not exist")
        return

    reporter: ReporterAbstract = globals()[args.export_type](
        input_file=args.input_file, logger=logger
    )
    await reporter.execute()


def entry() -> None:
    """
    Entrypoint for the CLI Application
    """
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())


if __name__ == "__main__":
    entry()
