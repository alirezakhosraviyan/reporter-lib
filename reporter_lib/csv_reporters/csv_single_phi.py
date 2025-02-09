from collections import Counter
from logging import Logger

from shapely.geometry.polygon import Polygon

from reporter_lib.csv_reporters.csv_bounding_box import CSVBoundingBoxFormatter
from reporter_lib.csv_reporters.reporter_abstraction import ReporterAbstract
from reporter_lib.schemas import PickResult


class CSVSinglePhiFormatter(CSVBoundingBoxFormatter, ReporterAbstract):
    def __init__(
        self,
        input_file: str,
        logger: Logger,
    ) -> None:
        super().__init__(
            input_file=input_file,
            logger=logger,
        )

        self._output_file_name_postfix = "_simple_b"
        self._display_name = "Simple Data Output w Bounding Box (CSV)"

    @staticmethod
    async def _picks_primary_failure_reason(picks: list[PickResult]) -> str:
        """
        Returns the primary failure reason of a list of invalid picks.
        Primary failure reason is the most common reason for failure."""
        if len([pick for pick in picks if not pick.valid]) == 0:
            return ""

        return Counter(
            [pick.reason.split("-")[-1] for pick in picks if not pick.valid]
        ).most_common(n=1)[0][0]

    @staticmethod
    async def _picks_first_valid(picks: list[PickResult]) -> PickResult:
        """
        Returns the first valid pick in a list of picks.
        Return last pick if no valid pick found.
        """
        for pick in picks:
            if pick.valid:
                return pick
        return picks[-1]

    async def _process_data(self) -> None:
        """
        Process a list of PlyResults and store the results in self._rows.
        """
        for ply in self._data.ply_results:
            pick = await self._picks_first_valid(ply.picks)
            primary_failure_reason = await self._picks_primary_failure_reason(ply.picks)
            ply_id = pick.plyshape.label
            parent_file = pick.plyshape.parent_file
            geom: Polygon = pick.plyshape.geom
            area = geom.area
            perimeter = geom.length
            compactness_value = self._compactness(geom)

            # Holes
            polygons = [Polygon(h.coords) for h in geom.interiors]
            num_holes = len(polygons)
            holes_perimeter = sum(h.length for h in polygons)
            holes_area = sum([h.area for h in polygons])

            self._rows.append(
                [
                    parent_file,
                    ply_id,
                    pick.cell_label,
                    pick.end_effector_label,
                    area,
                    perimeter,
                    compactness_value,
                    num_holes,
                    holes_perimeter,
                    holes_area,
                    pick.plyshape.material_label,
                    pick.plyshape_orientation,
                    pick.valid,
                    primary_failure_reason,
                    pick.zone_index,
                    pick.weight,
                    pick.end_effector_translation_x,
                    pick.end_effector_translation_y,
                    pick.end_effector_orientation,
                    len(pick.active_valves),
                    round(pick.plyshape.bounding_box_axes[0]),
                    round(pick.plyshape.bounding_box_axes[1]),
                    self._encode_active_cups(pick),
                ]
            )
