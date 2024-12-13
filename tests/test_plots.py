import altair as alt
import pandas as pd
import pandas as pd
from sklearn.metrics import classification_report
from sklearn.metrics import classification_report, accuracy_score
from sklearn.metrics import confusion_matrix
import pandas as pd
import altair as alt
import click


from data_training import load_model
from data_download import create_data_folder

from src.plots import (
    perform_test,
    save_eda_viz,
    make_confusion_matrix,
    save_feature_importance_viz,
)


def test_perform_test():
    # Create a test dataframe
    test_data = pd.DataFrame({
        "feature1": [1, 2, 3],
        "feature2": [4, 5, 6],
        "quality": [1, 0, 1],
    })

    # fit our model
    model = RandomForestClassifier()
    model.fit(test_data.drop(columns="quality"), test_data["quality"])

    predictions = perform_test(test_data, model)

    assert isinstance(predictions, np.ndarray), "Predictions should be a NumPy array."
    assert len(predictions) == len(test_data), "Predictions length should match test data."
    assert set(predictions).issubset([0, 1]), "Predictions should only contain valid labels."
    