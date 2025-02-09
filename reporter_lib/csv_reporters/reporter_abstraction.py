import json
import os
from abc import ABC, abstractmethod
from datetime import datetime
from logging import Logger
from math import pi

import aiofiles
from shapely.geometry.polygon import Polygon

from reporter_lib.schemas import PickResult, Report
from reporter_lib.utils import ReportEncoder


class ReporterAbstract(ABC):
    """
    Abstract base class for generating reports asynchronously.
    """

    _fields: list[str] = []  # List of field names for the report

    def __init__(
        self,
        display_name: str,
        input_file: str,
        output_file_name_postfix: str,
        logger: Logger,
    ):
        """
        Initializes the reporter with necessary metadata and input/output file details.

        :param display_name: Name of the report type
        :param input_file: Path to the input JSON file
        :param output_file_name_postfix: Postfix for output filename
        :param logger: Logger instance for logging messages
        """
        self._display_name = display_name
        self._input_file = input_file
        self._output_file_name_postfix = output_file_name_postfix
        self._logger = logger
        self._rows: list[
            list[str | int | float | None]
        ] = []  # Stores processed report data
        self._data: Report  # Placeholder for loaded report data

    @staticmethod
    def _encode_active_cups(pick: PickResult, separator: str = "*") -> str:
        """
        Encodes active vacuum cups in a pick result using a specified separator.

        :param pick: PickResult object containing active cup data
        :param separator: String separator for encoding active cups
        :return: Encoded string of active cups
        """
        return separator.join(pick.active_valves)

    @staticmethod
    def _compactness(geom: Polygon) -> float:
        """
        Computes the Polsby-Popper compactness measure of a shape.
        The value is between 0-100%, where higher values indicate more compact shapes.

        :param geom: Polygon geometry of the object
        :return: Compactness percentage
        """
        return (
            ((4 * pi * geom.area) / (geom.length**2)) * 100 if geom.length != 0 else 0
        )

    def _get_output_file_name(self) -> str:
        """
        Generates a timestamped output filename for the report.

        :return: Output filename as a string
        """
        return (
            f"output/reports_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            f"{self._output_file_name_postfix}.csv"
        )

    async def _write_to_file(self) -> None:
        """
        Asynchronously writes the processed data to a CSV file.
        """
        filename = self._get_output_file_name()
        if os.path.dirname(filename):
            os.makedirs(os.path.dirname(filename), exist_ok=True)

        async with aiofiles.open(filename, mode="w", newline="") as file:
            # Write the header row
            header_line = ";".join(map(str, self._fields)) + "\n"
            await file.write(header_line)

            # Write each data row
            for row in self._rows:
                line = (
                    ";".join(map(str, row)) + "\n"
                )  # Convert list to CSV-formatted string
                await file.write(line)  # Write line asynchronously

    async def _load_data(self) -> None:
        """
        Asynchronously loads JSON data from the input file
        and decodes it into a Report object.
        """
        async with aiofiles.open(self._input_file, mode="rb") as file:
            content = await file.read()
            self._data = json.loads(content, object_hook=ReportEncoder.decode_special)

    @abstractmethod
    async def _process_data(self) -> None:
        """
        Abstract method to process loaded data. Must be implemented in subclasses.
        """
        raise NotImplementedError

    async def execute(self) -> None:
        """
        Executes the report generation workflow:
        1. Loads data from the input file
        2. Processes the data (to be implemented by subclasses)
        3. Writes processed data to the output CSV file
        """
        await self._load_data()
        await self._process_data()
        await self._write_to_file()
