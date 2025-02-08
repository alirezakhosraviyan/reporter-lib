from logging import Logger

from reporter_lib.csv_reporters.reporter_abstraction import ReporterAbstract
from reporter_lib.schemas import PlyResult


class CSVAttentionPliesFormatter(ReporterAbstract):
    _fields = ["file", "ply", "cell", "ee", "success_rate"]

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
            output_file_name_postfix="_attention",
            logger=logger,
        )

    async def _get_sorted_ply_results(self) -> list[PlyResult]:
        return sorted(
            self._data.ply_results, key=lambda p: p.success_rate, reverse=True
        )

    async def _process_data(self) -> None:
        ply_results = await self._get_sorted_ply_results()

        for ply in ply_results:
            if ply.success_rate < 1:
                self._rows.append(
                    [
                        ply.picks[0].plyshape.parent_file,
                        ply.picks[0].plyshape.label,
                        ply.picks[0].cell_label,
                        ply.picks[0].end_effector_label,
                        round(100 * ply.success_rate),
                    ]
                )
