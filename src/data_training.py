from sklearn.model_selection import train_test_split, cross_validate
from sklearn.tree import DecisionTreeClassifier
import pandas as pd
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.metrics import classification_report, accuracy_score
import joblib
import click


from data_download import create_data_folder


FEATS_DATA_PATH = "data/processed/feature_importance.csv"

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
    model = joblib.load(model_path)

    return model


def perform_test(test_df, model):
    X_test = test_df.drop(columns="quality")
    y_test = test_df["quality"]
    # Predictions on the test set
    y_test_pred = model.predict(X_test)

    # Accuracy score
    test_accuracy = accuracy_score(y_test, y_test_pred)
    print(f"Test Accuracy: {test_accuracy:.4f}\n")

    # Classification report
    print("Table 1: Classification report:")
    print(classification_report(y_test, y_test_pred))


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
    model_path = create_data_folder(model_path)
    train_data = read_data(train_data)
    test_data = read_data(test_data)

    model_path = train_model(train_data)

    model = load_model(model_path)

    perform_test(test_data, model)


if __name__ == "__main__":
    main()
