import json
from logging import Logger
from unittest.mock import MagicMock

import pytest
from shapely.geometry import Polygon

from reporter_lib.csv_reporters.reporter_abstraction import ReporterAbstract
from reporter_lib.schemas import PickResult, PlyShape


@pytest.fixture
def mock_logger() -> MagicMock:
    """Fixture to provide a mock logger."""
    return MagicMock(spec=Logger)


@pytest.fixture
def mock_pick_result() -> PickResult:
    """Fixture to provide a mock PickResult instance."""
    return PickResult(active_valves=["A", "B", "C"], plyshape=MagicMock(PlyShape))


@pytest.fixture
def sample_json_data() -> bytes:
    """Fixture to provide sample JSON data as bytes."""
    return json.dumps([{"active_valves": ["X", "Y", "Z"]}]).encode("utf-8")


@pytest.fixture
def mock_polygon() -> Polygon:
    """Fixture to provide a sample polygon for testing compactness calculations."""
    return Polygon([(0, 0), (4, 0), (4, 3), (0, 3), (0, 0)])


@pytest.fixture
def mock_reporter(mock_logger: Logger) -> ReporterAbstract:
    """Fixture to create a mock subclass of ReporterAbstract for testing."""

    class MockReporter(ReporterAbstract):
        async def _process_data(self) -> None:
            return

    return MockReporter(
        "Test Report",
        "test_input.json",
        "test_postfix",
        mock_logger,
    )
