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