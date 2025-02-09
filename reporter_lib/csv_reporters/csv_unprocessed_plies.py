from logging import Logger

from reporter_lib.csv_reporters.reporter_abstraction import ReporterAbstract


class CSVUnprocessedPliesFormatter(ReporterAbstract):
    _fields = ["filename"]

    def __init__(
        self,
        input_file: str,
        logger: Logger,
    ) -> None:
        super().__init__(
            display_name="Overview of DXF files with warnings (CSV)",
            input_file=input_file,
            output_file_name_postfix="_unprocessed",
            logger=logger,
        )

    async def _process_data(self) -> None:
        """
        Process the data and generate a row for each failed filename.
        """
        for file in self._data.failed_filenames:
            self._rows.append([file])
