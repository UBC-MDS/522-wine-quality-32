import os
import pytest
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from src.plots import (
    perform_test,
    save_eda_viz,
    make_confusion_matrix,
    save_feature_importance_viz,
)


@pytest.fixture
def train_data():
    """Fixture for sample training data."""
    return pd.DataFrame({
        "feature1": [7.4, 7.8, 7.9, 7.2, 7.3],
        "feature2": [0.7, 0.88, 0.76, 0.65, 0.62],
        "quality": [5, 6, 5, 6, 5],
    })


@pytest.fixture
def test_data():
    """Fixture for sample test data."""
    return pd.DataFrame({
        "feature1": [7.5, 7.3, 7.1, 7.2],
        "feature2": [0.6, 0.8, 0.7, 0.65],
        "quality": [6, 5, 5, 6],
    })


@pytest.fixture
def feature_importances():
    """Fixture for feature importance data."""
    return pd.DataFrame({
        "Feature": ["feature1", "feature2"],
        "Importance": [0.8, 0.2],
    })


def test_perform_test(train_data, test_data):
    """Test the perform_test function."""
    # Train a model
    model = RandomForestClassifier()
    model.fit(train_data.drop(columns="quality"), train_data["quality"])

    predictions = perform_test(test_data, model)

    assert len(predictions) == len(test_data), "Predictions length does not match test data."
    assert set(predictions).issubset(train_data["quality"].unique()), "Predictions contain invalid labels."


def test_save_eda_viz(train_data, tmp_path):
    """Test the save_eda_viz function."""
    img_path = tmp_path / "images"
    os.makedirs(img_path, exist_ok=True)

    save_eda_viz(train_data, img_path)

    # Check if the file was created
    assert os.path.exists(f"{img_path}/eda.png"), "EDA visualization file was not saved."


def test_make_confusion_matrix(test_data, tmp_path):
    """Test the make_confusion_matrix function."""
    img_path = tmp_path / "images"
    os.makedirs(img_path, exist_ok=True)

    predictions = [6, 5, 5, 6]

    make_confusion_matrix(test_data, predictions, img_path)

    # Check if the file was created
    assert os.path.exists(f"{img_path}/confusion.png"), "Confusion matrix file was not saved."


def test_save_feature_importance_viz(feature_importances, tmp_path):
    """Test the save_feature_importance_viz function."""
    img_path = tmp_path / "images"
    os.makedirs(img_path, exist_ok=True)

    save_feature_importance_viz(feature_importances, img_path)

    assert os.path.exists(f"{img_path}/features.png"), "Feature importance visualization file was not saved."


def test_main(monkeypatch, train_data, test_data, feature_importances, tmp_path):
    """Test the main function."""
    img_path = tmp_path / "images"
    os.makedirs(img_path, exist_ok=True)

    # Mock dependencies
    def mock_create_data_folder(path):
        os.makedirs(path, exist_ok=True)

    def mock_load_model(model_path):
        model = RandomForestClassifier()
        model.fit(train_data.drop(columns="quality"), train_data["quality"])
        return model

    monkeypatch.setattr("src.plots.create_data_folder", mock_create_data_folder)
    monkeypatch.setattr("src.plots.load_model", mock_load_model)

    # Save mock data
    train_data_path = tmp_path / "train.csv"
    test_data_path = tmp_path / "test.csv"
    features_path = tmp_path / "features.csv"
    train_data.to_csv(train_data_path, index=False)
    test_data.to_csv(test_data_path, index=False)
    feature_importances.to_csv(features_path, index=False)

    # Mock constants
    monkeypatch.setattr("src.plots.IMAGE_FOLDER", str(img_path))
    monkeypatch.setattr("src.plots.TRAIN_DATA_PATH", str(train_data_path))
    monkeypatch.setattr("src.plots.TEST_DATA_PATH", str(test_data_path))
    monkeypatch.setattr("src.plots.FEATURES_PATH", str(features_path))

    # Call main function
    from src.plots import main
    main.callback(img_path=str(img_path), train_data_path=str(train_data_path), test_data_path=str(test_data_path))

    # Validate outputs
    assert os.path.exists(f"{img_path}/eda.png"), "EDA visualization file was not saved."
    assert os.path.exists(f"{img_path}/confusion.png"), "Confusion matrix file was not saved."
    assert os.path.exists(f"{img_path}/features.png"), "Feature importance visualization file was not saved."