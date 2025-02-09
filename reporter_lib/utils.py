import json
import logging
import sys
from typing import Any

from shapely import wkt

from reporter_lib.schemas import PickResult, PlyResult, PlyShape, Report


def setup_logger(
    name: str = "reporter_lib", log_level: int = logging.INFO
) -> logging.Logger:
    """
    Sets up and returns a logger with the specified name, level,
    and optional file output.
    """
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    # adding handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    return logger


class ReportEncoder(json.JSONEncoder):
    _PLY_SHAPE_KEY = "__ply_shape__"
    _PLY_RESULT_KEY = "__ply_result__"
    _PICK_RESULT_KEY = "__pick_result__"
    _POLYGON_KEY = "__polygon__"
    _REPORT_KEY = "__report__"

    @staticmethod
    def decode_special(dct: dict[str, dict[str, Any]]) -> object:
        if ReportEncoder._REPORT_KEY in dct:
            return Report(**dct[ReportEncoder._REPORT_KEY])
        if ReportEncoder._POLYGON_KEY in dct:
            return wkt.loads(dct[ReportEncoder._POLYGON_KEY])
        if ReportEncoder._PLY_SHAPE_KEY in dct:
            return PlyShape(**dct[ReportEncoder._PLY_SHAPE_KEY])
        if ReportEncoder._PLY_RESULT_KEY in dct:
            return PlyResult(**dct[ReportEncoder._PLY_RESULT_KEY])
        if ReportEncoder._PICK_RESULT_KEY in dct:
            return PickResult(**dct[ReportEncoder._PICK_RESULT_KEY])
        return dct
