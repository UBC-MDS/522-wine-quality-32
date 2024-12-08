# Wine Quality Prediction 

### Project Board

- [Milestone 1](<https://github.com/orgs/UBC-MDS/projects/177/views/1>)
- [Milestone 2](https://github.com/orgs/UBC-MDS/projects/183)
- [Milestone 3](https://pages.github.ubc.ca/mds-2024-25/DSCI_522_dsci-workflows_students/release/milestone3/milestone3.html)

# Summary
This project explores the relationship between physicochemical properties of wines and their quality ratings, aiming to predict wine quality and identify key factors influencing it using machine learning models such as Decision Trees. Through exploratory data analysis (EDA), we examine patterns, distributions, and correlations, addressing challenges such as class imbalances in wine quality ratings. The Decision Tree model is evaluated using metrics like accuracy, precision, recall, and feature importance to uncover significant predictors, such as density, alcohol, and volatile_acidity. The primary goal is to build an interpretable machine learning pipeline that provides actionable insights for winemakers to optimize production processes and for consumers to make informed choices. Additionally, the project sets the foundation for future work, including incorporating sensory attributes, addressing dataset imbalances, and leveraging more advanced ensemble methods for better predictions.

# Contributors:
- Chukwunonso Ebele-Muolokwu 
- Samuel Adetsi 
- Shashank Hosahalli Shivamurthy
- Ci Xu  

# Reproducible Computational Environment

This project ensures a reproducible computational environment using Conda. Follow the steps below to set up the environment for this project.

## Prerequisites

1. Install Miniconda or Anaconda.
2. Clone this repository:

```bash
git clone https://github.com/UBC-MDS/522-wine-quality-32.git
cd 522-wine-quality-32
```

## Setting Up the Environment

### Option 1: Using `environment.yaml`

This is the recommended method to set up the environment.

1. Create the Conda environment:

```bash
conda env create -f environment.yml
```

2. Activate the environment:

```bash
conda activate 522_milestone_env
```

3. Verify the environment setup:

```bash
python -c "import pandas as pd; print('Environment set up successfully!')"
```

### Option 2: Using Platform-Specific Lock Files

If you want to ensure reproducibility across different operating systems, use platform-specific lock files.

1. Install `conda-lock`:

```bash
pip install conda-lock
```

2. Create the environment using the lock file for your platform:
   - **For Linux/macOS/Windows:**

```bash
conda-lock install --name 522_milestone_env conda-lock.yml
```

3. Activate the environment:

```bash
conda activate 522_milestone_env
```

### Option 3: Using Docker Container
### Running the analysis

1. Navigate to the root of this project on your computer using the
   command line and enter the following command:

```bash
docker compose up
```

2. In the terminal, look for a URL that starts with 
`http://127.0.0.1:8888/lab?token=` 
(for an example, see the highlighted text in the terminal below). 
Copy and paste that URL into your browser.

![Lab Token to copy](img/lab-token.png)

3. To run the analysis,
open `analysis.ipynb` in Jupyter Lab you just launched
and under the "Kernel" menu click "Restart Kernel and Run All Cells...".

# Modular Scripts

The analysis is divided into modular Python scripts, each performing a specific task. These scripts must be executed sequentially to reproduce the results.

## Script 1: Data Download

`Description`: Downloads the dataset from a specified source and saves it in the raw data folder.

```bash
python src/data_download.py --folder_path="data/raw" --data_id=186
```

`Arguments`:
- --folder_path: Path to save the raw data.
- --data_id: ID of the dataset to download.

## Script 2: Data Validation and Processing

`Description`: Validates the raw data and processes it for analysis. Saves processed data and a validation report.

```bash
python src/validation.py --raw="data/raw" --processed="data/processed" --report_path="report"
```

`Arguments`:
- --raw: Path to the folder containing raw data.
- --processed: Path to save the processed data.
- --report_path: Path to save the validation report.

## Script 3: Model Training

`Description`: Trains a machine learning model using the processed data and saves the model.

```bash
python src/data_training.py --model_path="data/model" --train_data="data/processed/wine_train.csv" --test_data="data/processed/wine_test.csv"
```

`Arguments`:
- --model_path: Path to save the trained model.
- --train_data: Path to the processed training dataset.
- --test_data: Path to the processed testing dataset.

## Script 4: Generate Plots

`Description`: Creates visualizations based on the analysis and saves them as images.

```bash
python src/plots.py --img_path="data/img" --train_data_path="data/processed/wine_train.csv" --test_data_path="data/processed/wine_test.csv"
```

`Arguments`:

- --img_path: Path to save the generated plots.
- --train_data_path: Path to the training data file.
- --test_data_path: Path to the testing data file.

# Generating the Report

The final report is created using Quarto and narrates the analysis with no visible code. To generate the report:

## PDF Format

```bash
quarto render report/wine_quality_eda.qmd --to pdf
```

## HTML Format

```bash
quarto render report/wine_quality_eda.qmd --to html
```


# Updating the Environment

If you add new dependencies:
1. Update environment.yaml.
2. Rebuild the environment:

```bash
conda env update -f environment.yaml --prune
```
3. For Docker, rebuild the container:

```bash
docker compose build
```

# Cleaning Up


- Remove the Conda Environment:
```bash
conda env remove -n 522_milestone_env
```

- Remove Docker Resources:
```bash
docker compose down --remove-orphans
```