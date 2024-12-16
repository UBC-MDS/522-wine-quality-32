# CHANGELOG

This file describes the improvements made to the "Wine Quality Prediction" project based on reviewer feedback. Each improvement is documented with references to specific evidence in the repository, including relevant code changes, commit messages, and pull requests.

---

## **Version 2.0.0
### **Date:** [15 Dec 2024]

### **Improvements**
1. **Documentation:**
   - Added detailed docstrings to all functions, describing their purpose, inputs, and outputs.
     - **Evidence:** [Commit](URL)
   - Included references for computational tools and libraries in the `References` section of the report.
     - **Evidence:** [Pull Request](URL)

2. **Reproducibility:**
   - Fixed the missing dependency issue for the `deepchecks` package by updating the `Dockerfile`, `environment.yml` and `conda-linux.lock` files.
     - **Evidence:** [https://github.com/UBC-MDS/522-wine-quality-32/pull/61](https://github.com/UBC-MDS/522-wine-quality-32/pull/61)
   - Replaced manually written tables (e.g., classification report) with programmatically generated tables.
     - **Evidence:** [Commit](URL)

3. **Figures and Tables:**
   - Corrected mismatched figure titles and numbering in the report (e.g., "Figure 3" labeled as "Figure 1").
     - **Evidence:** [Pull Request](URL)
   - Removed redundancy by including only Python code or resulting images for figures (e.g., Figures 2 and 4).
     - **Evidence:** [Commit](URL)

4. **Clarity and Detail:**
   - Elaborated on the target variable (`wine quality`) and clarified what the different classes represent.
     - **Evidence:** [Commit](URL)
   - Added detailed descriptions of dataset features to help non-expert readers understand their significance.
     - **Evidence:** [Pull Request](URL)

5. **EDA:**
   - Conducted a more thorough exploration of the training dataset's characteristics during the EDA phase.
     - **Evidence:** [Pull Request](URL)

6. **Formatting and Readability:**
   - Standardized figure and table generation using code for consistency and reproducibility.
     - **Evidence:** [Commit](URL)

---

### **Narrative Summary**

These improvements address reviewer feedback to enhance documentation, reproducibility, and clarity of the project. The updated documentation and references make the project more accessible to new users. Reproducibility is ensured with dependency fixes and automated table generation. The report now provides clearer explanations of the target variable and dataset features. EDA has been expanded, and formatting issues in the figures and tables have been resolved.
