from logging import Logger

from reporter_lib.csv_reporters.reporter_abstraction import ReporterAbstract


class CSVTimeEstFormatter(ReporterAbstract):
    _fields = ["process", "time", "cell", "ee", "material", "time_est_config"]

    def __init__(
        self,
        input_file: str,
        logger: Logger,
    ) -> None:
        super().__init__(
            display_name="Time Estimate (CSV)",
            input_file=input_file,
            output_file_name_postfix="_time_est",
            logger=logger,
        )

    async def _process_data(self) -> None:
        """
        Process the data and generate the output rows.
        """
        pick = self._data.picks[0]
        for process, time in self._data.time_estimate.items():
            self._rows.append(
                [
                    process,
                    time,
                    pick.cell_label,
                    pick.end_effector_label,
                    pick.plyshape.material_label,
                    self._data.tec_config_label,
                ]
            )
