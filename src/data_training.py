"""This script does the training and saving of our model as a pickle file"""

import sys
import warnings

from sklearn.tree import DecisionTreeClassifier
import sklearn
import pandas as pd
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.metrics import classification_report, accuracy_score
import joblib
import click

from data_download import create_data_folder


warnings.filterwarnings("ignore", category=sklearn.exceptions.UndefinedMetricWarning)
sys.path.append("src")

FEATS_DATA_PATH = "data/processed/feature_importance.csv"
REPORT_DATA_PATH = "data/processed/classification_report.csv"

MODEL_PATH = "data/model"


def read_data(data_path: str) -> pd.DataFrame:
    """Reads the training data for trainig

    Args:
        train_data_path (str): Path of the training data

    Returns:
        pd.DataFrame: Dataframe is returned
    """
    data = pd.read_csv(data_path)

    return data


def train_model(train_df: pd.DataFrame):
    """
    Train a Decision Tree model using GridSearchCV for hyperparameter tuning.

    Args:
        train_df (pd.DataFrame): Training DataFrame with features and target.

    Returns:
        str: Path to the saved model file.
    """
    X_train = train_df.drop(columns="quality")
    y_train = train_df["quality"]
    # Define the hyperparameter grid
    param_grid = {
        "max_depth": [3, 5, 10, None],
        "min_samples_split": [2, 5, 10],
        "min_samples_leaf": [1, 2, 5],
        "max_features": [None, "sqrt", "log2"],
    }
    tree_model = DecisionTreeClassifier(random_state=16)

    # Set up GridSearchCV
    grid_search = GridSearchCV(
        estimator=tree_model,
        param_grid=param_grid,
        cv=5,
        scoring="accuracy",
        n_jobs=-1,
        verbose=1,
    )
    grid_search.fit(X_train, y_train)

    # Get the best model
    best_tree_model = grid_search.best_estimator_

    feature_importances = pd.DataFrame(
        {"Feature": X_train.columns, "Importance": best_tree_model.feature_importances_}
    ).sort_values(by="Importance", ascending=False)

    feature_importances.to_csv(FEATS_DATA_PATH, index=False)

    joblib.dump(best_tree_model, f"{MODEL_PATH}/model.pkl")

    return f"{MODEL_PATH}/model.pkl"


def load_model(model_path: str):
    """
    Load a saved machine learning model.

    Args:
        model_path (str): Path to the saved model file.

    Returns:
        object: Loaded machine learning model.
    """
    model = joblib.load(model_path)

    return model


def perform_test(test_df, model):
    """
    Evaluate the model on test data and generate performance metrics.

    Args:
        test_df (pd.DataFrame): Test DataFrame with features and target.
        model (object): Trained machine learning model.

    Returns:
        pd.DataFrame: Classification report as a DataFrame.
    """
    X_test = test_df.drop(columns="quality")
    y_test = test_df["quality"]
    # Predictions on the test set
    y_test_pred = model.predict(X_test)

    # Accuracy score
    test_accuracy = accuracy_score(y_test, y_test_pred)
    print(f"Test Accuracy: {test_accuracy:.4f}\n")

    # Classification report
    print("Table 1: Classification report:")
    report_dict = classification_report(y_test, y_test_pred, output_dict=True)

    report_df = pd.DataFrame(report_dict).transpose()
    report_df.to_csv(REPORT_DATA_PATH, index=False)
    return report_df


@click.command()
@click.option(
    "--model_path",
    type=str,
    help="Model folder path",
)
@click.option(
    "--train_data",
    type=str,
    help="training data path",
)
@click.option(
    "--test_data",
    type=str,
    help="training data path",
)
def main(model_path, train_data, test_data):
    """
    Main function to orchestrate model training and evaluation.

    Args:
        model_path (str): Path to save the model.
        train_data (str): Path to training data.
        test_data (str): Path to test data.
    """
    model_path = create_data_folder(model_path)
    train_data = read_data(train_data)
    test_data = read_data(test_data)

    model_path = train_model(train_data)

    model = load_model(model_path)

    perform_test(test_data, model)


if __name__ == "__main__":
    main()
