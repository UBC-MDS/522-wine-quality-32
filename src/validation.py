import os
import click
import pandas as pd
import numpy as np
import janitor
import click
import pandera as pa
from pandera import Column, Check
from sklearn.model_selection import train_test_split
from deepchecks.tabular import Dataset
from deepchecks.tabular.checks import FeatureDrift
import sys
sys.path.append("src")

from data_download import create_data_folder

# python src/data_download.py --folder_path="data2/raw" --data_id=186
RAW_DATA_PATH = "data/raw/wine_quality_combined.csv"
PROCESSED_FOLDER_PATH = "data/processed"


def check_corr_feats(df: pd.DataFrame):
    """This is is ahelper function that is called in the validate_processed_data

    Args:
        df (pd.DataFrame): Dataframe that the correlation is checked

    Returns:
        _type_: A correlated Dataframe
    """
    aa = df.corr().abs() < 0.9
    np.fill_diagonal(aa.values, True)
    return aa.all().all()


# Uses janitor to clean column names


def clean_data(data: pd.DataFrame) -> pd.DataFrame:
    """Cleans out the raw dataframe

    Args:
        data (pd.DataFrame): Processes the dataframe to clean out issues

    Returns:
        pd.DataFrame: Cleaned Dataframe
    """
    # clean out the names
    data = data.clean_names()

    # drop duplicate columsn
    data = data.drop_duplicates()

    return data


def validate_processed_data(data: pd.DataFrame) -> pd.DataFrame:
    """Validate the processed data using a predefined schema.

    Args:
        data (pd.DataFrame): The processed data to be validated.

    Returns:
        pd.DataFrame: The input DataFrame, if it passes validation.
    """

    schema = pa.DataFrameSchema(
        {
            "fixed_acidity": Column(pa.Float, Check.ge(0), nullable=False),
            "volatile_acidity": Column(pa.Float, Check.ge(0), nullable=False),
            "citric_acid": Column(pa.Float, Check.ge(0), nullable=False),
            "residual_sugar": Column(pa.Float, Check.ge(0), nullable=False),
            "chlorides": Column(pa.Float, Check.ge(0), nullable=False),
            "free_sulfur_dioxide": Column(pa.Float, Check.ge(0), nullable=False),
            "total_sulfur_dioxide": Column(pa.Float, Check.ge(0), nullable=False),
            "density": Column(pa.Float, Check.ge(0), nullable=False),
            "ph": Column(pa.Float, [Check.ge(0), Check.le(14)], nullable=False),
            "sulphates": Column(pa.Float, Check.ge(0), nullable=False),
            "alcohol": Column(pa.Float, Check.ge(0), nullable=False),
            "quality": Column(
                pa.Int, Check.isin([3, 4, 5, 6, 7, 8, 9]), nullable=False
            ),  # Example: Replace with valid levels
        },
        checks=[
            # Ensure no duplicate rows
            pa.Check(lambda df: ~df.duplicated().any(), error="Duplicate rows found."),
            # Ensure no empty rows
            pa.Check(
                lambda df: ~(df.isna().all(axis=1)).any(), error="Empty rows found."
            ),
            # Check for missingness threshold (e.g., <5%)
            pa.Check(
                lambda df: (df.isna().mean() < 0.05).all(),
                error="Missingness exceeds threshold.",
            ),
            # Ensure the target variable distribution meets expectations
            pa.Check(
                lambda df: df["quality"]
                .value_counts(normalize=True)
                .between(0.0001, 0.5)
                .all(),
                error="Quality distribution is outside expected bounds.",
            ),
            # Check no anomalous correlations between target and features
            pa.Check(
                lambda df: (df.corr()["quality"].abs()[:-1] < 0.9).all(),
                error="Anomalous correlations found between quality and features.",
            ),
            # Check no anomalous correlations between features
            pa.Check(
                lambda df: check_corr_feats(df),
                error="Anomalous correlations found between features.",
            ),
            # pa.Check(
            #     lambda df: df.apply(lambda x: ((x >= x.quantile(0.01)) & (x <= x.quantile(0.99))).all(), axis=0).all(),
            #     error="Outliers detected beyond 1st and 99th percentiles."
            # )
        ],
    )

    try:
        schema.validate(data)
        print("Data is valid!")
    except Exception as e:
        print(f"Validation error: {e}")


def split_data(data: pd.DataFrame):
    """Split the input DataFrame into training and testing sets.

    This function performs a stratified split of the input DataFrame:
    - 80% of the data is used for training
    - 20% of the data is used for testing
    - Uses a fixed random state for reproducibility

    Args:
        data (pd.DataFrame): Input DataFrame to be split.

    Returns:
        tuple: A tuple containing (train_df, test_df)
    """
    
    train_df, test_df = train_test_split(data, test_size=0.2, random_state=123)

    train_df.to_csv(os.path.join(PROCESSED_FOLDER_PATH, "wine_train.csv"), index=False)
    test_df.to_csv(os.path.join(PROCESSED_FOLDER_PATH, "wine_test.csv"), index=False)

    return train_df, test_df


def validate_data_distribution(train_df, test_df, report_path, threshold: int = 0.2):
    """
    Validate the data distribution between the train and test sets.

    Args:
        train_df (pd.DataFrame): The training data.
        test_df (pd.DataFrame): The testing data.
        report_path (str): The path to save the validation report.
        threshold (int, optional): The maximum allowed drift score. Defaults to 0.2.
    """
    
    full_path = f"{report_path}/validation_report.html"
    train_ds = Dataset(train_df, label="quality", cat_features=[])
    test_ds = Dataset(test_df, label="quality", cat_features=[])
    check = FeatureDrift()
    check_cond = check.add_condition_drift_score_less_than(
        max_allowed_numeric_score=threshold
    )
    result = check_cond.run(train_dataset=train_ds, test_dataset=test_ds)

    bool_value = all(
        result.value[key]["Drift score"] < threshold for key in result.value
    )

    if not bool_value:
        raise
    if os.path.exists(full_path):
        os.remove(full_path)
    result.save_as_html(full_path)


@click.command()
@click.option(
    "--raw",
    type=str,
    help="Are you dealing raw data",
)
@click.option(
    "--processed",
    type=str,
    help="Processed data folder path",
)
@click.option(
    "--report_path",
    type=str,
    help="Report path for storing the validation report",
)
def main(raw: str, processed: str, report_path: str):

    print(f"This is a {raw} data path")
    raw_data_data = f"{raw}/wine_quality_combined.csv"
    create_data_folder(processed)
    create_data_folder(report_path)

    wine_df = pd.read_csv(raw_data_data)

    clean_wine = clean_data(wine_df)

    validate_processed_data(clean_wine)

    train_df, test_df = split_data(
        clean_wine,
    )
    validate_data_distribution(
        train_df=train_df, test_df=test_df, report_path=report_path
    )


if __name__ == "__main__":
    main()
