import json
from abc import ABC, abstractmethod
from datetime import datetime
from logging import Logger
from math import pi

import aiofiles
from shapely.geometry.polygon import Polygon

from reporter_lib.schemas import PickResult, Report
from reporter_lib.utils import ReportEncoder


class ReporterAbstract(ABC):
    _fields: list[str] = []
    _rows: list[list[str]] = []
    _data: list[PickResult]
    _output_file_name_postfix: str = ""

    def __init__(
        self,
        display_name: str,
        display_description: str,
        input_file: str,
        output_file_name_postfix: str,
        logger: Logger,
    ):
        self._display_name = display_name
        self._display_description = display_description
        self._input_file = input_file
        self._output_file_name_postfix = output_file_name_postfix
        self._logger = logger

    @staticmethod
    def _encode_active_cups(pick: PickResult, separator="*") -> str:
        return separator.join(pick.active_valves)

    @staticmethod
    def _compactness(geom: Polygon) -> float:
        """Polsby-Popper measure of compactness: in range 0-100%"""
        return (
            ((4 * pi * geom.area) / (geom.length**2)) * 100 if geom.length != 0 else 0
        )

    def _get_output_file_name(self):
        return (
            f"reports_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            f"{self._output_file_name_postfix}.csv"
        )

    async def _write_to_file(self) -> None:
        async with aiofiles.open(
            self._get_output_file_name(), mode="w", newline=""
        ) as file:
            # adding headers
            self._rows.insert(0, self._fields)
            # adding rows
            for row in self._rows:
                line = ";".join(map(str, row)) + "\n"  # Converting list to CSV line
                await file.write(line)  # Asynchronously writing to file

    async def _load_data(self) -> None:
        async with aiofiles.open(self._input_file, mode="rb") as file:
            content = await file.read()
            self._data: Report = json.loads(
                content, object_hook=ReportEncoder.decode_special
            )

    @abstractmethod
    async def _process_data(self) -> str:
        raise NotImplementedError

    async def execute(self):
        await self._load_data()
        await self._process_data()
        await self._write_to_file()
