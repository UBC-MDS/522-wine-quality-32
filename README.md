# Wine Quality Prediction 

### Project Board

- [Milestone 1](<https://github.com/orgs/UBC-MDS/projects/177/views/1>)
- [Milestone 2](https://github.com/orgs/UBC-MDS/projects/183)

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
    conda env create -f environment.yaml
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
   - **For Linux Or macOS or Windows:**

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

``` 
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


## Updating the Environment

If the `environment.yaml` file is updated (e.g., new dependencies are added), you can update your existing environment with:

```bash
conda env update -f environment.yaml --prune
```

## Cleaning Up

To remove the Conda environment:

```bash
conda env remove -n 522_milestone_env
```

To shut down the container and clean up the resources, 
type `Cntrl` + `C` in the terminal
where you launched the container, and then type `docker compose rm`


### Files Included for Reproducibility

- `environment.yaml`: Contains the dependencies required for the project.
- **`conda-linux-64.lock`, `conda-osx-64.lock`, `conda-win-64.lock`**: Platform-specific lock files for precise reproducibility.

## Example Workflow

Here’s a typical workflow for setting up and testing the environment:

### Clone the repository

```bash
git clone https://github.com/UBC-MDS/522-wine-quality-32.git
cd 522-wine-quality-32
```

### Create and activate the environment
```bash
conda env create -f environment.yaml
conda activate 522_milestone_env
```

### Test the environment
```bash
python -c "import pandas as pd; print('Environment set up successfully!')"
```

### Remove the environment (if needed)
```bash
conda env remove -n 522_milestone_env
```
