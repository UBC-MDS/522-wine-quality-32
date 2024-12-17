# CHANGELOG

This file describes the improvements made to the "Wine Quality Prediction" project based on reviewer feedback. Each improvement is documented with references to specific evidence in the repository, including relevant code changes, commit messages, and pull requests.

---

## Parent Issues that we used to track

#### [Milestone 1 feedback](https://github.com/UBC-MDS/522-wine-quality-32/issues/37)
#### [Milestone 2 feedback](https://github.com/UBC-MDS/522-wine-quality-32/issues/50)
#### [Peer Review Feedback](https://github.com/UBC-MDS/522-wine-quality-32/issues/66)


# Improvements Based on Reviewer Feedback

This document highlights the improvements made to the project based on the feedback provided by reviewers. It includes references to specific changes, supported by URLs pointing to the evidence in the codebase, commits, or pull requests (PRs).

---




## Documentation

### Task 1: Add detailed documentation for functions in the script
**Feedback**: Functions in the script lacked detailed documentation regarding their purpose, inputs, and outputs.

**Action**: Added detailed docstrings to all functions in the script.
- **Evidence**: [Commit](https://github.com/UBC-MDS/522-wine-quality-32/pull/68/commits/f81818d44895cba228adbb2e39feaa2d98a0e9c7) includes comprehensive function-level documentation.

### Task 2: Include references for computational tools and libraries
**Feedback**: The references section did not mention the computational tools and libraries used (e.g., Altair, NumPy).

**Action**: Added references to all computational tools and libraries used in the project.
- **Evidence**: See [PR #70](https://github.com/UBC-MDS/522-wine-quality-32/pull/70), which updates the references section in the report.

---

## Reproducibility

### Task 3: Fix missing dependency issue for the deepchecks package
**Feedback**: The environment setup in docker had a missing dependency for the `deepchecks` package.

**Action**: Updated the `Dockerfile` file to include the `deepchecks` package.
- **Evidence**: [Commit](https://github.com/UBC-MDS/522-wine-quality-32/pull/61/commits/584fad09b3ecda9bb4b5d48f14135ccc68607f79) shows the updated environment file.

### Task 4: Replace manually created tables with programmatically generated tables
**Feedback**: Tables (e.g., classification report) were created manually instead of being generated programmatically.

**Action**: Updated the scripts to generate all tables programmatically.
- **Evidence**: [PR #72](https://github.com/UBC-MDS/522-wine-quality-32/pull/72) demonstrates the implementation of dynamic table generation for reproducibility.

---

## Figures and Tables

### Task 5: Fix mismatched figure titles and numbering
**Feedback**: Figures in the report had mismatched titles and numbers (e.g., "Figure 3" labeled as "Figure 1").

**Action**: Corrected the figure titles and numbering in the report.
- **Evidence**: [PR #73](https://github.com/UBC-MDS/522-wine-quality-32/pull/73) includes the fixed titles and updated numbering.

### Task 6: Remove redundancy in figures
**Feedback**: Figures 2 and 4 included both Python code and resulting images, leading to redundancy.

**Action**: Removed redundancy by including either the code or the images, not both.
- **Evidence**: [PR #71](https://github.com/UBC-MDS/522-wine-quality-32/pull/71) simplifies the figures section.

### Task 7: Dynamically generate all tables and figures
**Feedback**: Tables and figures should be dynamically generated using code for reproducibility.

**Action**: Ensured all tables and figures in the report are generated dynamically.
- **Evidence**: [PR #74](https://github.com/UBC-MDS/522-wine-quality-32/pull/74) provides updated scripts for dynamic generation.

---

## Clarity and Detail

### Task 8: Elaborate on the target variable (wine quality)
**Feedback**: The target variable needed more explanation, including what the classes represent.

**Action**: Added detailed descriptions of the target variable and the meaning of the quality classes.
- **Evidence**: [Commit](https://github.com/UBC-MDS/522-wine-quality-32/commit/b1a11706f2fc4945afccc7d89e173a39bb3b7c8c#diff-bd371140c0e71a5a16d763add8283c2b82ee8ae744a60e6b1ae24274365f8afeR48) updates the dataset description in the report.

### Task 9: Provide descriptions of dataset features
**Feedback**: Dataset features were not well-described, making it difficult for readers unfamiliar with wine to understand their importance.

**Action**: Added a detailed description of each dataset feature.
- **Evidence**: [PR #85](https://github.com/UBC-MDS/522-wine-quality-32/pull/85) provides the updated feature descriptions.

---

## Milestone 1

### Update `contributing.md`
**Feedback**: The `contributing.md` file lacked details on how to make a contribution.

**Action**: Updated the file to include detailed contribution instructions.
- **Evidence**: [PR #79](https://github.com/UBC-MDS/522-wine-quality-32/pull/79) contains the revised `contributing.md`.

### Create new directory for `analysis.ipynb`
**Feedback**: A dedicated directory for `analysis.ipynb` was missing.

**Action**: Created a new directory for analysis files.
- **Evidence**: [Commit](https://github.com/UBC-MDS/522-wine-quality-32/commit/89efa49f27388f12cddf8b12c6c70a6b8bf33c66).

### Specify Creative Commons license
**Feedback**: The report did not specify a Creative Commons license.

**Action**: Added a Creative Commons license to the project.
- **Evidence**: [PR #81](https://github.com/UBC-MDS/522-wine-quality-32/pull/81) introduces the license.

---

## Milestone 2

### Pin the version for `mamba`
**Feedback**: The `mamba` package version was not specified in the `environment.yml` file.

**Action**: Updated the `environment.yml` file to pin the `mamba` version.
- **Evidence**: [Commit](https://github.com/UBC-MDS/522-wine-quality-32/commit/19776e90a78a157ce6f052e28b77b160b203219f).

### Use specific tags for Docker
**Feedback**: The latest tag was used for Docker images instead of a specific version.

**Action**: Updated the Docker configuration to use specific image tags.
- **Evidence**: [PR #76](https://github.com/UBC-MDS/522-wine-quality-32/pull/76).

---

These improvements address all feedback provided by reviewers and ensure the project is more robust, reproducible, and user-friendly.