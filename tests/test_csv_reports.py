from unittest.mock import MagicMock

import aiofiles

from reporter_lib.csv_reporters.csv_report_base import CSVReportFormatter


async def test_csv_report_base(mock_logger: MagicMock) -> None:
    reporter = CSVReportFormatter(
        "Test Report",
        "Test Description",
        "tests/resources/test.json",
        logger=mock_logger,
    )

    reporter._get_output_file_name = (
        lambda: "tests/resources/test_output.csv"
    )  # Mock method

    await reporter.execute()

    # Read and verify file content
    async with aiofiles.open("tests/resources/test_output.csv", mode="r") as file:
        content = await file.read()
    expected_content = (
        "\n".join([";".join(map(str, row)) for row in reporter._rows]) + "\n"
    )

    assert content == expected_content, "File content does not match expected output."
