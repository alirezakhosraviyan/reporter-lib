from unittest.mock import MagicMock

import aiofiles

from reporter_lib.csv_reporters import CSVAttentionPliesFormatter, CSVReportFormatter
from tests.resources.expected_results import (
    EXPECTED_RESULT_ATTENTION_PLIES,
    EXPECTED_RESULT_BASE,
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
