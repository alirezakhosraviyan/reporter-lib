from logging import Logger

from reporter_lib.csv_reporters.reporter_abstraction import ReporterAbstract


class CSVUnprocessedPliesFormatter(ReporterAbstract):
    _fields = ["filename"]

    def __init__(
        self,
        display_name: str,
        display_description: str,
        input_file: str,
        logger: Logger,
    ) -> None:
        super().__init__(
            display_name=display_name,
            display_description=display_description,
            input_file=input_file,
            _output_file_name_postfix="_unprocessed",
            logger=logger,
        )

    async def _process_data(self) -> None:
        for file in self._data.failed_filenames:
            self._rows.append([file])
