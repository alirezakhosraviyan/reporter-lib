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
    """
    Test the base CSV report formatter.

    Args:
        mock_logger (MagicMock): Mocked logger to capture log messages.
    """
    # Initialize the reporter with test parameters
    reporter = CSVReportFormatter(
        "tests/resources/test.json",
        mock_logger,
    )

    # Mock method to return the output file name
    reporter._get_output_file_name = lambda: "tests/resources/test_output.csv"

    # Execute the report generation
    await reporter.execute()

    # Read and verify the content of the generated CSV file
    async with aiofiles.open("tests/resources/test_output.csv", mode="r") as file:
        content = await file.read()

    expected_content = (
        "\n".join([";".join(str(item) for item in row) for row in EXPECTED_RESULT_BASE])
        + "\n"
    )

    # Assert that the content matches the expected result
    assert content == expected_content, "File content does not match expected output."


async def test_csv_report_attention_plies(mock_logger: MagicMock) -> None:
    """
    Test the CSV report formatter for attention plies.

    Args:
        mock_logger (MagicMock): Mocked logger to capture log messages.
    """
    reporter = CSVAttentionPliesFormatter(
        "tests/resources/test.json",
        mock_logger,
    )

    reporter._get_output_file_name = (
        lambda: "tests/resources/test_output.csv"
    )  # Mock method

    await reporter.execute()

    async with aiofiles.open("tests/resources/test_output.csv", mode="r") as file:
        content = await file.read()

    expected_content = (
        "\n".join(
            [
                ";".join(str(item) for item in row)
                for row in EXPECTED_RESULT_ATTENTION_PLIES
            ]
        )
        + "\n"
    )

    assert content == expected_content, "File content does not match expected output."


async def test_csv_report_unprocessed_plies(mock_logger: MagicMock) -> None:
    """
    Test the CSV report formatter for unprocessed plies.

    Args:
        mock_logger (MagicMock): Mocked logger to capture log messages.
    """
    reporter = CSVUnprocessedPliesFormatter(
        "tests/resources/test.json",
        mock_logger,
    )

    reporter._get_output_file_name = (
        lambda: "tests/resources/test_output.csv"
    )  # Mock method

    await reporter.execute()

    async with aiofiles.open("tests/resources/test_output.csv", mode="r") as file:
        content = await file.read()

    expected_content = (
        "\n".join(
            [
                ";".join(str(item) for item in row)
                for row in EXPECTED_RESULT_UNPROCESSED_PLIES
            ]
        )
        + "\n"
    )

    assert content == expected_content, "File content does not match expected output."


async def test_csv_report_bounding_box(mock_logger: MagicMock) -> None:
    """
    Test the CSV report formatter for bounding box data.

    Args:
        mock_logger (MagicMock): Mocked logger to capture log messages.
    """
    reporter = CSVBoundingBoxFormatter(
        "tests/resources/test.json",
        mock_logger,
    )

    reporter._get_output_file_name = (
        lambda: "tests/resources/test_output.csv"
    )  # Mock method

    await reporter.execute()

    async with aiofiles.open("tests/resources/test_output.csv", mode="r") as file:
        content = await file.read()

    expected_content = (
        "\n".join(
            [
                ";".join(str(item) for item in row)
                for row in EXPECTED_RESULT_BOUNDING_BOX
            ]
        )
        + "\n"
    )

    assert content == expected_content, "File content does not match expected output."


async def test_csv_report_single_phi(mock_logger: MagicMock) -> None:
    """
    Test the CSV report formatter for single Phi data.

    Args:
        mock_logger (MagicMock): Mocked logger to capture log messages.
    """
    reporter = CSVSinglePhiFormatter(
        "tests/resources/test.json",
        mock_logger,
    )

    reporter._get_output_file_name = (
        lambda: "tests/resources/test_output.csv"
    )  # Mock method

    await reporter.execute()

    async with aiofiles.open("tests/resources/test_output.csv", mode="r") as file:
        content = await file.read()

    expected_content = (
        "\n".join(
            [";".join(str(item) for item in row) for row in EXPECTED_RESULT_SINGLE_PHI]
        )
        + "\n"
    )

    assert content == expected_content, "File content does not match expected output."


async def test_csv_report_time_est(mock_logger: MagicMock) -> None:
    """
    Test the CSV report formatter for time estimation data.

    Args:
        mock_logger (MagicMock): Mocked logger to capture log messages.
    """
    reporter = CSVTimeEstFormatter(
        "tests/resources/test.json",
        mock_logger,
    )

    reporter._get_output_file_name = (
        lambda: "tests/resources/test_output.csv"
    )  # Mock method

    await reporter.execute()

    async with aiofiles.open("tests/resources/test_output.csv", mode="r") as file:
        content = await file.read()

    expected_content = (
        "\n".join(
            [";".join(str(item) for item in row) for row in EXPECTED_RESULT_TIME_EST]
        )
        + "\n"
    )

    assert content == expected_content, "File content does not match expected output."
