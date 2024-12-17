import os

import click
import pandas as pd
from ucimlrepo import fetch_ucirepo


def create_data_folder(data_dir: str) -> str:
    """This is a helper function that creates the data directory for the csv file

    Args:
        data_dir (str): The data directory for the data, typically the data directory

    Raises:
        OsError: When the directory was not created succcessfully

    Returns:
        str: the fule file_path for the data that will be downloaded
    """

    csv_file_path = os.path.join(data_dir, "wine_quality_combined.csv")

    try:
        # Ensure the directory exists
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
            print(f"Directory '{data_dir}' created successfully.")
        else:
            print(f"Directory '{data_dir}' already exists.")
    except OSError as e:
        print(f"Error creating directory '{data_dir}': {e}")
        raise

    return csv_file_path

def download_data(file_path: str, data_id: int = 186):
    """Downloads the data from UCI and saves the csv data in the data folder

    Args:
        file_path (str): File path to save the file
        data_id (int, optional): Data Id for the dataset we are using. Defaults to 186.
    """
    if isinstance(data_id, str):
        data_id = int(data_id)
    try:
        print("CSV file not found. Fetching dataset...")

        # Fetch the dataset
        wine_quality = fetch_ucirepo(id=data_id)

        # Features (X) and Targets (y)
        X = wine_quality.data.features
        y = wine_quality.data.targets

        # Combine features and targets into a single DataFrame
        wine_df = pd.concat([X, y], axis=1)

        # Save the DataFrame to a CSV file
        wine_df.to_csv(file_path, index=False)
        print(f"Dataset saved as '{file_path}'.")

        return wine_df
    except Exception as e:
        print(f"Error fetching or saving the dataset: {e}")
        raise

@click.command()
@click.option(
    "--folder_path",
    type=str,
    help="Path to directory where raw data will be written to",
)
@click.option("--data_id", type=str, help="ID of dataset to be downloaded")

def main(folder_path: str, data_id: int):
    """
    Main function to create a data folder and download the dataset.

    Args:
        folder_path (str): Path to the directory for saving raw data.
        data_id (int): ID of the dataset to be downloaded from UCI ML Repository.
    """
    #create the analysis folder
    csv_path = create_data_folder(folder_path)
    print("Folder path has been created")

    #Download the data
    download_data(csv_path, data_id)

if __name__ == "__main__":
    main()
