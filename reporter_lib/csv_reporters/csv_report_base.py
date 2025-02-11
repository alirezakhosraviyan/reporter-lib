from logging import Logger

from shapely.geometry.polygon import Polygon

from .reporter_abstraction import ReporterAbstract


class CSVReportFormatter(ReporterAbstract):
    """Base class for CSV reporters."""

    _fields = [
        "file",
        "ply",
        "cell",
        "ee",
        "area",
        "perimeter",
        "compactness",
        "num_holes",
        "holes_perimeter",
        "holes_area",
        "material",
        "ply_phi",
        "valid",
        "reason",
        "zone",
        "weight",
        "ee_x",
        "ee_y",
        "ee_phi",
        "num_cups",
        "active_cups",
    ]

    def __init__(
        self,
        input_file: str,
        logger: Logger,
    ) -> None:
        super().__init__(
            display_name="Detailed Data Output (CSV)",
            input_file=input_file,
            output_file_name_postfix="",
            logger=logger,
        )

    async def _process_data(self) -> None:
        """
        Process a list of PickResults and store the results in self._rows.
        """
        for pick in self._data.picks:
            parent_file = pick.plyshape.parent_file
            ply_id = pick.plyshape.label
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
                    pick.reason,
                    pick.zone_index,
                    pick.weight,
                    pick.end_effector_translation_x,
                    pick.end_effector_translation_y,
                    pick.end_effector_orientation,
                    len(pick.active_valves),
                    self._encode_active_cups(pick),
                ]
            )
