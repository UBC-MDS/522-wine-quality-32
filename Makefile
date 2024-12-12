# Makefile
# Wine Quality Prediction Project

.PHONY: all data process train plot report clean retrain

# Run the entire pipeline
all: report

# Download the dataset
data: data/raw/wine_data.csv

data/raw/wine_data.csv: src/data_download.py
	@echo "Checking and downloading dataset..."
	[ -f data/raw/wine_data.csv ] || python src/data_download.py --folder_path="data/raw" --data_id=186

# Process and validate the data
process: data/processed/wine_train.csv data/processed/wine_test.csv

data/processed/wine_train.csv data/processed/wine_test.csv: data/raw/wine_data.csv src/validation.py
	@echo "Checking and processing data..."
	[ -f data/processed/wine_train.csv ] && [ -f data/processed/wine_test.csv ] || \
	python src/validation.py \
		--raw="data/raw" \
		--processed="data/processed" \
		--report_path="report"

# Train the machine learning model
train: data/model/model.pkl data/processed/feature_importance.csv

data/model/model.pkl data/processed/feature_importance.csv: data/processed/wine_train.csv data/processed/wine_test.csv src/data_training.py
	@echo "Checking and training model..."
	[ -f data/model/model.pkl ] && [ -f data/processed/feature_importance.csv ] || mkdir -p data/model && \
	python src/data_training.py \
		--model_path="data/model" \
		--train_data="data/processed/wine_train.csv" \
		--test_data="data/processed/wine_test.csv"

# Generate plots
plot: data/img/feature_importance.png data/img/quality_distribution.png

data/img/feature_importance.png data/img/quality_distribution.png: data/processed/feature_importance.csv data/processed/wine_train.csv src/plots.py
	@echo "Checking and generating plots..."
	[ -f data/img/feature_importance.png ] && [ -f data/img/quality_distribution.png ] || mkdir -p data/img && \
	python src/plots.py \
		--img_path="data/img" \
		--train_data_path="data/processed/wine_train.csv" \
		--test_data_path="data/processed/wine_test.csv"

# Generate the final report
report: report/wine_quality_eda.html

report/wine_quality_eda.html: data/img/feature_importance.png data/img/quality_distribution.png report/wine_quality_eda.qmd
	@echo "Checking and generating report..."
	[ -f report/wine_quality_eda.html ] || \
	quarto render report/wine_quality_eda.qmd --to html
	quarto render report/wine_quality_eda.qmd --to pdf

# Clean up all generated files
clean:
	@echo "Cleaning up all generated files..."
	rm -f data/raw/* data/processed/* data/model/* data/img/* \
	      report/validation_report.html report/wine_quality_eda.html report/wine_quality_eda.pdf

# Retrain the model and regenerate everything
retrain: clean train plot report