from math import pi

import aiofiles
import pytest
from shapely.geometry import Polygon

from reporter_lib.csv_reporters.reporter_abstraction import ReporterAbstract
from reporter_lib.schemas import PickResult


async def test_encode_active_cups(mock_pick_result: PickResult) -> None:
    """Test _encode_active_cups returns correctly formatted string."""
    result = ReporterAbstract._encode_active_cups(mock_pick_result, separator="-")
    assert result == "A-B-C", "Encoding of active cups is incorrect."


async def test_compactness(mock_polygon: Polygon) -> None:
    """Test _compactness returns the correct Polsby-Popper value."""
    expected_value = ((4 * pi * mock_polygon.area) / (mock_polygon.length**2)) * 100
    result = ReporterAbstract._compactness(mock_polygon)
    assert result == pytest.approx(expected_value, rel=1e-3), (
        "Compactness calculation is incorrect."
    )


async def test_get_output_file_name(mock_reporter: ReporterAbstract) -> None:
    """Test _get_output_file_name returns a properly formatted string."""
    result = mock_reporter._get_output_file_name()
    assert result.startswith("reports_"), (
        "Output filename does not start with 'reports_'"
    )
    assert result.endswith("test_postfix.csv"), (
        "Output filename does not end with 'test_postfix.csv'"
    )


async def test_load_data(mock_reporter: ReporterAbstract) -> None:
    """Test _load_data reads the file and decodes JSON properly."""
    mock_reporter._input_file = "tests/resources/test.json"
    await mock_reporter._load_data()

    assert len(mock_reporter._data.picks) == 5
    assert mock_reporter._data.time_estimate == {"action": 4.0, "wait": 0.2}
    assert mock_reporter._data.failed_filenames == ["report2.dxf"]
    assert mock_reporter._data.tec_config_label == "TestTEC1"
    assert len(mock_reporter._data.ply_results) == 2

    # Check all fields for the first pick only
    first_pick = mock_reporter._data.picks[0]
    assert first_pick.cell_label == "TestCell1"
    assert first_pick.end_effector_label == "TestEE1"
    assert first_pick.plyshape.label == "TestPly1"
    assert first_pick.plyshape.parent_file == "report1.dxf"
    assert first_pick.plyshape.material_label == "TestMat1"
    assert first_pick.plyshape.bounding_box_axes == (12.0, 15.0)
    assert first_pick.plyshape_orientation == 2.5
    assert first_pick.valid is True
    assert first_pick.reason == "Success"
    assert first_pick.end_effector_orientation == 0.0
    assert first_pick.end_effector_translation_x == 2.0
    assert first_pick.end_effector_translation_y == 3.0
    assert first_pick.active_valves == ["a", "b", "d"]
    assert first_pick.zone_index == 4
    assert first_pick.weight == 0.4


async def test_write_to_file_creates_correct_file(
    mock_reporter: ReporterAbstract,
) -> None:
    """
    Test if `_write_to_file` correctly writes semicolon-separated
     values to the actual file.
    """
    mock_reporter._rows = [
        ["Alice", 30, "New York"],
        ["Bob", 25, "Los Angeles"],
        ["Charlie, Jr.", 28, "San Francisco"],
    ]

    mock_reporter._fields = ["Name", "Age", "City"]
    mock_reporter._get_output_file_name = (
        lambda: "tests/resources/test_output.csv"
    )  # Mock method

    # Write to the actual file
    await mock_reporter._write_to_file()

    # Read and verify file content
    async with aiofiles.open("tests/resources/test_output.csv", mode="r") as file:
        content = await file.read()
    expected_content = (
        "\n".join([";".join(map(str, row)) for row in mock_reporter._rows]) + "\n"
    )

    assert content == expected_content, "File content does not match expected output."
