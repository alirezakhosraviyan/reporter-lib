import argparse
import asyncio
import logging
import os

# Importing all csv reporter class to be available in globals()
from reporter_lib.csv_reporters import *  # noqa
from reporter_lib.csv_reporters.reporter_abstraction import ReporterAbstract
from reporter_lib.utils import setup_logger


async def main() -> None:
    """
    Main function for handling command-line arguments and
    executing the appropriate report exporter.

    - Parses command-line arguments.
    - Validates input file existence.
    - Instantiates the selected reporter and executes
      the export process asynchronously.
    """
    description = "Exporting Report from events"
    parser = argparse.ArgumentParser(
        description=description,
        add_help=True,
    )

    # Required arguments
    parser.add_argument(
        "input_file",
        type=str,
        help="Input file to test with",
    )

    parser.add_argument(
        "export_type",  # (must match a subclass of ReporterAbstract)
        type=str,
        choices=[subclass.__name__ for subclass in ReporterAbstract.__subclasses__()],
        help="Choose export type between available ones",
    )

    # Optional arguments
    parser.add_argument(
        "-p",
        "--production",  # Flag to indicate whether to use production settings
        action="store_true",
        help="Boolean flag indicating whether to use production settings",
    )

    args = parser.parse_args()

    # Set up logger based on production flag
    logger = setup_logger(log_level=logging.DEBUG if args.production else logging.INFO)

    # Validate if input file exists
    if not os.path.exists(args.input_file):
        logger.error(f"Input file {args.input_file} does not exist")
        return

    # Dynamically instantiate the appropriate Reporter subclass
    reporter: ReporterAbstract = globals()[args.export_type](
        input_file=args.input_file, logger=logger
    )

    # Execute the report export process asynchronously
    await reporter.execute()


def entry() -> None:
    """
    Entrypoint function for the CLI application.
    - Sets up the event loop and runs the main function.
    """
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())


if __name__ == "__main__":
    entry()
