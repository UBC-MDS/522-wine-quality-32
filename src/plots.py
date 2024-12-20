"""This script plots all the needed visualization being used in the final function"""

import sys

import altair as alt
import pandas as pd
import pandas as pd
from sklearn.metrics import confusion_matrix
import pandas as pd
import altair as alt
import click

from data_training import load_model
from data_download import create_data_folder

sys.path.append("src")

TEST_DATA_PATH = "data/processed/wine_test.csv"
TRAIN_DATA_PATH = "data/processed/wine_train.csv"
IMAGE_FOLDER = "data/img"
MODEL_PATH = "data/model/model.pkl"
FEATURES_PATH = "data/processed/feature_importance.csv"


def perform_test(test_df, model):
    """
    Generate predictions on the test set using the given model.

    Args:
        test_df (pd.DataFrame): Test dataset with features and labels.
        model: Trained machine learning model.

    Returns:
        np.ndarray: Predicted labels for the test set.
    """
    X_test = test_df.drop(columns="quality")
    y_test = test_df["quality"]
    # Predictions on the test set
    y_test_pred = model.predict(X_test)

    return y_test_pred


def save_eda_viz(train_data: pd.DataFrame, img_path):
    """
    Create and save an EDA visualization showing distributions of features.

    Args:
        train_data (pd.DataFrame): Training dataset.
        img_path (str): Path to save the visualization.
    """
    columns = train_data.columns.to_list()

    chart = (
        alt.Chart(train_data)
        .mark_bar()
        .encode(
            x=alt.X(alt.repeat("repeat"), bin=alt.Bin(maxbins=40)), y=alt.Y("count()")
        )
        .repeat(repeat=columns, columns=3)
    )
    chart.save(f"{img_path}/eda.png")


def make_confusion_matrix(y_test_df, y_pred, img_path):
    """
    Generate and save a confusion matrix visualization.

    Args:
        y_test_df (pd.DataFrame): Test dataset containing true labels.
        y_pred (np.ndarray): Predicted labels from the model.
        img_path (str): Path to save the confusion matrix visualization.
    """
    y_test = y_test_df["quality"]
    # Dynamically determine class labels from both y_test and y_test_pred
    class_labels = sorted(set(y_test).union(set(y_pred)))

    # Compute confusion matrix
    cm = confusion_matrix(y_test, y_pred, labels=class_labels)

    # Create a DataFrame with dynamic labels for multi-class
    cm_df = pd.DataFrame(
        cm,
        columns=[f"Predicted {label}" for label in class_labels],
        index=[f"Actual {label}" for label in class_labels],
    ).reset_index()

    # Convert to long format for Altair
    cm_melted = cm_df.melt(id_vars="index", var_name="Predicted", value_name="Count")

    # Plot confusion matrix using Altair
    confusion_chart = (
        alt.Chart(cm_melted)
        .mark_rect()
        .encode(
            x=alt.X("Predicted:N", title="Predicted Label"),
            y=alt.Y("index:N", title="Actual Label"),
            color=alt.Color("Count:Q", scale=alt.Scale(scheme="blues"), title="Count"),
            tooltip=["index:N", "Predicted:N", "Count:Q"],
        )
        .properties(title="Confusion Matrix", width=400, height=400)
    )

    text = confusion_chart.mark_text(baseline="middle", fontSize=12).encode(
        text=alt.Text("Count:Q", format=".0f")
    )
    final = confusion_chart + text

    final.save(f"{img_path}/confusion.png")


def save_feature_importance_viz(feature_importances: pd.DataFrame, img_path: str):
    """
    Create and save a feature importance visualization.

    Args:
        feature_importances (pd.DataFrame): DataFrame containing feature names and their importance values.
        img_path (str): Path to save the feature importance visualization.
    """
    # Plot feature importance using Altair
    importance_chart = (
        alt.Chart(feature_importances)
        .mark_bar()
        .encode(
            x=alt.X("Importance:Q", title="Importance"),
            y=alt.Y("Feature:N", sort="-x", title="Feature"),
            tooltip=["Feature", "Importance"],
        )
        .properties(title="Feature Importances", width=600, height=400)
    )

    importance_chart.save(f"{img_path}/features.png")


@click.command()
@click.option(
    "--img_path",
    type=str,
    help="Path to store the images",
)
@click.option(
    "--train_data_path",
    type=str,
    help="Path to read the train data",
)
@click.option(
    "--test_data_path",
    type=str,
    help="Path to read the test data",
)
def main(img_path, train_data_path, test_data_path):
    """
    Main function to run the data visualization and analysis pipeline.

    Args:
        img_path (str): Path to save generated images.
        train_data_path (str): Path to load the training data.
        test_data_path (str): Path to load the test data.
    """
    # Loading the files needed
    _ = create_data_folder(img_path)
    model = load_model(MODEL_PATH)
    test_data = pd.read_csv(test_data_path)
    train_data = pd.read_csv(train_data_path)
    features_df = pd.read_csv(FEATURES_PATH)

    # make test pred
    test_pred = perform_test(test_data, model)

    save_eda_viz(train_data, IMAGE_FOLDER)

    make_confusion_matrix(test_data, test_pred, IMAGE_FOLDER)

    save_feature_importance_viz(features_df, IMAGE_FOLDER)


if __name__ == "__main__":
    main()
