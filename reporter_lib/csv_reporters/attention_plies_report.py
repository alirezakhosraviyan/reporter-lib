from logging import Logger

from reporter_lib.csv_reporters.reporter_abstraction import ReporterAbstract
from reporter_lib.schemas import PlyResult


class CSVAttentionPliesFormatter(ReporterAbstract):
    """CSV formatter for attention plies report."""

    _fields = ["file", "ply", "cell", "ee", "success_rate"]

    def __init__(
        self,
        input_file: str,
        logger: Logger,
    ) -> None:
        super().__init__(
            display_name="Plies Requiring Attention Overview (CSV)",
            input_file=input_file,
            output_file_name_postfix="_attention",
            logger=logger,
        )

    async def _get_sorted_ply_results(self) -> list[PlyResult]:
        """Sort the ply results by their success rate in descending order.

        Returns:
            A list of PlyResult objects sorted by their success rate.
        """
        return sorted(
            self._data.ply_results, key=lambda p: p.success_rate, reverse=True
        )

    async def _process_data(self) -> None:
        """Process the data and generate the output rows.

        Sort the ply results by their success rate in descending order, and
        then generate a row for each ply with success rate less than 100%.
        The row contains the parent file, the ply label, the cell label, the
        end effector label and the success rate in percentage.
        """
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
