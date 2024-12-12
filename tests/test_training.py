import os
import pytest
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import joblib
from src.data_training import (
    read_data,
    train_model,
    load_model,
    perform_test,
)

@pytest.fixture
def sample_train_data():
    """Fixture for sample training data with sufficient rows."""
    return pd.DataFrame({
        "fixed_acidity": [7.4, 7.8, 7.9, 7.2, 7.3, 7.6, 7.5, 7.1, 7.0, 6.9],
        "volatile_acidity": [0.7, 0.88, 0.76, 0.65, 0.62, 0.69, 0.68, 0.66, 0.7, 0.8],
        "citric_acid": [0.0, 0.0, 0.04, 0.02, 0.01, 0.03, 0.02, 0.01, 0.05, 0.06],
        "residual_sugar": [1.9, 2.6, 2.0, 1.8, 2.1, 2.4, 1.7, 1.6, 1.5, 1.4],
        "chlorides": [0.076, 0.098, 0.084, 0.079, 0.075, 0.074, 0.073, 0.072, 0.071, 0.07],
        "free_sulfur_dioxide": [11.0, 25.0, 15.0, 20.0, 10.0, 12.0, 13.0, 14.0, 16.0, 17.0],
        "total_sulfur_dioxide": [34.0, 67.0, 40.0, 50.0, 45.0, 55.0, 60.0, 65.0, 70.0, 75.0],
        "density": [0.9978, 0.9968, 0.9971, 0.9973, 0.9974, 0.9972, 0.9975, 0.9976, 0.9977, 0.9979],
        "ph": [3.51, 3.20, 3.30, 3.45, 3.50, 3.40, 3.55, 3.60, 3.65, 3.70],
        "sulphates": [0.56, 0.65, 0.57, 0.59, 0.60, 0.62, 0.58, 0.61, 0.63, 0.64],
        "alcohol": [9.4, 9.8, 9.5, 9.6, 9.7, 9.9, 9.3, 9.2, 9.1, 9.0],
        "quality": [5, 6, 5, 6, 5, 6, 5, 6, 5, 6],
    })

@pytest.fixture
def sample_test_data():
    """Fixture for sample test data."""
    return pd.DataFrame({
        "fixed_acidity": [7.5, 7.3, 7.1, 7.2],
        "volatile_acidity": [0.6, 0.8, 0.7, 0.65],
        "citric_acid": [0.01, 0.02, 0.03, 0.02],
        "residual_sugar": [1.7, 2.3, 1.5, 1.9],
        "chlorides": [0.07, 0.09, 0.08, 0.075],
        "free_sulfur_dioxide": [15.0, 18.0, 14.0, 12.0],
        "total_sulfur_dioxide": [40.0, 45.0, 38.0, 42.0],
        "density": [0.9972, 0.9974, 0.9973, 0.9975],
        "ph": [3.40, 3.50, 3.55, 3.45],
        "sulphates": [0.60, 0.62, 0.58, 0.61],
        "alcohol": [9.5, 9.7, 9.3, 9.4],
        "quality": [6, 5, 5, 6],
    })

def test_read_data(tmp_path):
    """Test the read_data function."""
    data_path = tmp_path / "data.csv"
    sample_data = {
        "col1": [1, 2, 3],
        "col2": [4, 5, 6],
    }
    pd.DataFrame(sample_data).to_csv(data_path, index=False)
    df = read_data(str(data_path))
    assert not df.empty
    assert list(df.columns) == ["col1", "col2"]

def test_train_model(sample_train_data, tmp_path):
    """Test the train_model function."""
    model_path = tmp_path / "model"
    os.makedirs(model_path, exist_ok=True)
    trained_model_path = train_model(sample_train_data)
    assert os.path.exists(trained_model_path)
    model = joblib.load(trained_model_path)
    assert isinstance(model, DecisionTreeClassifier)

def test_load_model(tmp_path):
    """Test the load_model function."""
    model_path = tmp_path / "model.pkl"
    tree_model = DecisionTreeClassifier()
    joblib.dump(tree_model, model_path)
    loaded_model = load_model(model_path)
    assert isinstance(loaded_model, DecisionTreeClassifier)

def test_perform_test(sample_test_data, sample_train_data, tmp_path):
    """Test the perform_test function."""
    model_path = tmp_path / "model.pkl"
    tree_model = DecisionTreeClassifier()
    tree_model.fit(sample_train_data.drop(columns="quality"), sample_train_data["quality"])
    joblib.dump(tree_model, model_path)

    model = load_model(model_path)
    report_df = perform_test(sample_test_data, model)
    assert not report_df.empty
    assert "precision" in report_df.columns
    assert "recall" in report_df.columns

def test_end_to_end(sample_train_data, sample_test_data, tmp_path):
    """End-to-end test for training, saving, loading, and testing."""
    model_path = tmp_path / "model"
    os.makedirs(model_path, exist_ok=True)
    trained_model_path = train_model(sample_train_data)

    model = load_model(trained_model_path)
    report_df = perform_test(sample_test_data, model)
    assert not report_df.empty
    assert "f1-score" in report_df.columns