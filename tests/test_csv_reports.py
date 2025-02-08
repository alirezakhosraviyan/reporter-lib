from unittest.mock import MagicMock

import aiofiles

from reporter_lib.csv_reporters import (
    CSVAttentionPliesFormatter,
    CSVBoundingBoxFormatter,
    CSVReportFormatter,
    CSVSinglePhiFormatter,
    CSVTimeEstFormatter,
    CSVUnprocessedPliesFormatter,
)
from tests.resources.expected_results import (
    EXPECTED_RESULT_ATTENTION_PLIES,
    EXPECTED_RESULT_BASE,
    EXPECTED_RESULT_BOUNDING_BOX,
    EXPECTED_RESULT_SINGLE_PHI,
    EXPECTED_RESULT_TIME_EST,
    EXPECTED_RESULT_UNPROCESSED_PLIES,
)


async def test_csv_report_base(mock_logger: MagicMock) -> None:
    reporter = CSVReportFormatter(
        "Test Report",
        "Test Description",
        "tests/resources/test.json",
        mock_logger,
    )

    reporter._get_output_file_name = (
        lambda: "tests/resources/test_output.csv"
    )  # Mock method

    await reporter.execute()

    # Read and verify file content
    async with aiofiles.open("tests/resources/test_output.csv", mode="r") as file:
        content = await file.read()

    expected_content = (
        "\n".join([";".join(map(str, row)) for row in EXPECTED_RESULT_BASE]) + "\n"
    )

    assert content == expected_content, "File content does not match expected output."


async def test_csv_report_attention_plies(mock_logger: MagicMock) -> None:
    reporter = CSVAttentionPliesFormatter(
        "Test Report",
        "Test Description",
        "tests/resources/test.json",
        mock_logger,
    )

    reporter._get_output_file_name = (
        lambda: "tests/resources/test_output.csv"
    )  # Mock method

    await reporter.execute()

    # Read and verify file content
    async with aiofiles.open("tests/resources/test_output.csv", mode="r") as file:
        content = await file.read()

    expected_content = (
        "\n".join([";".join(map(str, row)) for row in EXPECTED_RESULT_ATTENTION_PLIES])
        + "\n"
    )

    assert content == expected_content, "File content does not match expected output."


async def test_csv_report_unprocessed_plies(mock_logger: MagicMock) -> None:
    reporter = CSVUnprocessedPliesFormatter(
        "Test Report",
        "Test Description",
        "tests/resources/test.json",
        mock_logger,
    )

    reporter._get_output_file_name = (
        lambda: "tests/resources/test_output.csv"
    )  # Mock method

    await reporter.execute()

    # Read and verify file content
    async with aiofiles.open("tests/resources/test_output.csv", mode="r") as file:
        content = await file.read()

    expected_content = (
        "\n".join(
            [";".join(map(str, row)) for row in EXPECTED_RESULT_UNPROCESSED_PLIES]
        )
        + "\n"
    )

    assert content == expected_content, "File content does not match expected output."


async def test_csv_report_bounding_box(mock_logger: MagicMock) -> None:
    reporter = CSVBoundingBoxFormatter(
        "Test Report",
        "Test Description",
        "tests/resources/test.json",
        mock_logger,
    )

    reporter._get_output_file_name = (
        lambda: "tests/resources/test_output.csv"
    )  # Mock method

    await reporter.execute()

    # Read and verify file content
    async with aiofiles.open("tests/resources/test_output.csv", mode="r") as file:
        content = await file.read()

    expected_content = (
        "\n".join([";".join(map(str, row)) for row in EXPECTED_RESULT_BOUNDING_BOX])
        + "\n"
    )

    assert content == expected_content, "File content does not match expected output."


async def test_csv_report_single_phi(mock_logger: MagicMock) -> None:
    reporter = CSVSinglePhiFormatter(
        "Test Report",
        "Test Description",
        "tests/resources/test.json",
        mock_logger,
    )

    reporter._get_output_file_name = (
        lambda: "tests/resources/test_output.csv"
    )  # Mock method

    await reporter.execute()

    # Read and verify file content
    async with aiofiles.open("tests/resources/test_output.csv", mode="r") as file:
        content = await file.read()

    expected_content = (
        "\n".join([";".join(map(str, row)) for row in EXPECTED_RESULT_SINGLE_PHI])
        + "\n"
    )

    assert content == expected_content, "File content does not match expected output."


async def test_csv_report_time_est(mock_logger: MagicMock) -> None:
    reporter = CSVTimeEstFormatter(
        "Test Report",
        "Test Description",
        "tests/resources/test.json",
        mock_logger,
    )

    reporter._get_output_file_name = (
        lambda: "tests/resources/test_output.csv"
    )  # Mock method

    await reporter.execute()

    # Read and verify file content
    async with aiofiles.open("tests/resources/test_output.csv", mode="r") as file:
        content = await file.read()

    expected_content = (
        "\n".join([";".join(map(str, row)) for row in EXPECTED_RESULT_TIME_EST]) + "\n"
    )

    assert content == expected_content, "File content does not match expected output."
