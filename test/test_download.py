# Replace 'your_module' with the module name where your function is defined
import os
import pytest
import tempfile
from unittest.mock import patch, MagicMock
import pandas as pd
from unittest import mock

# Import the function to test
from src.data_download import create_data_folder, download_data


def test_create_data_folder():
    # Create a temporary directory for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        # Define the expected file path
        expected_csv_path = os.path.join(temp_dir, "wine_quality_combined.csv")

        # Ensure the directory does not exist beforehand
        if os.path.exists(temp_dir):
            os.rmdir(temp_dir)

        # Mock os.makedirs to avoid actual directory creation
        with patch("os.makedirs") as mocked_makedirs:
            # Call the function with the temporary directory
            result = create_data_folder(temp_dir)

            # Assert that the result is the expected file path
            assert result == expected_csv_path

            mocked_makedirs.assert_called_once_with(temp_dir)

        # Test the behavior when the directory already exists
        with patch("os.path.exists", return_value=True):
            result = create_data_folder(temp_dir)
            assert result == expected_csv_path


def mock_fetch_ucirepo(id):
    # Mocked dataset structure
    features = pd.DataFrame({"feature1": [1, 2], "feature2": [3, 4]})
    targets = pd.DataFrame({"target": [0, 1]})
    mock_data = MagicMock()
    mock_data.data.features = features
    mock_data.data.targets = targets
    return mock_data


def test_download_data(capsys):
    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as temp_file:
        file_path = temp_file.name
        print(file_path)

    try:
        # Patch the fetch_ucirepo function to use the mock
        with patch("ucimlrepo.fetch_ucirepo", side_effect=mock_fetch_ucirepo):
            # Call the function
            download_data(file_path)

            # Capture the output
            captured = capsys.readouterr()

            # Check the output messages
            assert "CSV file not found. Fetching dataset..." in captured.out
            assert f"Dataset saved as '{file_path}'." in captured.out

    finally:
        # Cleanup the temporary file
        try:
            temp_file.close()
        except Exception:
            pass
        try:
            os.remove(file_path)
        except Exception:
            pass


def test_download_data_invalid_id():
    """
    Test the download_data function with an invalid data_id to ensure it raises an error.
    """
    # Arrange
    file_path = "dummy_path.csv"
    invalid_data_id = "invalid_id"

    # Act and Assert
    with pytest.raises(
        ValueError
    ):  # Assuming fetch_ucirepo will raise a ValueError for invalid id
        download_data(file_path, data_id=invalid_data_id)
