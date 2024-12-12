import os
import pandas as pd
import numpy as np
import tempfile

from src.validation import clean_data, split_data

def test_clean_data():
    """
    Test the clean_data function to ensure it properly cleans the dataframe.
    """
    # Create a sample dataframe with some issues
    data = pd.DataFrame({
        'Fixed Acidity': [7.0, 7.0, 8.1, 7.2, 7.2],
        'Volatile Acidity': [0.27, 0.27, 0.28, 0.23, 0.23],
        'Citric Acid': [0.36, 0.36, 0.34, 0.32, 0.32]
    })
    
    # Apply clean_data
    cleaned_data = clean_data(data)
    
    # Check column names are cleaned
    assert list(cleaned_data.columns) == ['fixed_acidity', 'volatile_acidity', 'citric_acid']
    
    # Check for duplicate removal
    assert len(cleaned_data) == 3


def test_split_data():
    """
    Test the split_data function to ensure proper data splitting.
    """
    # Create a sample dataframe
    data = pd.DataFrame({
        'feature1': range(100),
        'feature2': range(100, 200),
        'quality': [np.random.randint(3, 9) for _ in range(100)]
    })
    
    # Create a temporary directory for test outputs
    with tempfile.TemporaryDirectory() as tmpdir:
        # Mock the PROCESSED_FOLDER_PATH to use temporary directory
        original_processed_folder = split_data.__globals__['PROCESSED_FOLDER_PATH']
        split_data.__globals__['PROCESSED_FOLDER_PATH'] = tmpdir
        
        try:
            # Split the data
            train_df, test_df = split_data(data)
            
            # Assertions
            assert len(train_df) == 80  # 80% of original data
            assert len(test_df) == 20   # 20% of original data
            
            # Check if CSV files were created
            assert os.path.exists(os.path.join(tmpdir, 'wine_train.csv'))
            assert os.path.exists(os.path.join(tmpdir, 'wine_test.csv'))
            
        finally:
            # Restore the original PROCESSED_FOLDER_PATH
            split_data.__globals__['PROCESSED_FOLDER_PATH'] = original_processed_folder