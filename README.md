# Air Alerms Predicting

## Description
This repository houses a collection of scripts tailored for a data science workflow, emphasizing the collection, processing, and storage of datasets related to Ukraine, insights from the Institute for the Study of War (ISW), and other relevant data sources. The project streamlines the data science pipeline by automating data acquisition, cleaning, and structuring, enabling real-time updates and efficient storage for downstream analysis.

Additionally, it serves as a practical example of applying machine learning in data science, specifically for predictive modeling. The repository is designed to predict air alerts using machine learning techniques such as RandomForestClassifier and Logistic Regression, showcasing the end-to-end process of data preparation, model training, and evaluation.

# Project Structure and File Overview

## Directory Structure

- **config/**: Contains environment setup files.

- **data/**: A dedicated directory for storing datasets. Users are required to acquire air alert and weather data for at least two years.

- **src/**: The core of the project, containing scripts and Jupyter notebooks for data processing and modeling.

- **templates/**: Holds HTML templates for rendering web pages via Flask, suggesting a web interface for visualizing predictions or results.

---

## File Breakdown and Functionality

### Data Collection Scripts

- **ISW_everyday_update.py**: Automates daily updates of ISW data to keep the dataset current for real-time analysis.

- **ISW_history.py**: Collects historical ISW data, likely used to build a baseline dataset for training models.

- **weather_scrap.py**: Scrapes weather data from Visual Crossing, providing features like temperature or precipitation that may correlate with air alerts.

- **alerts_in_ua.py**: Fetches real-time air raid alerts in Ukraine.

---

### Data Processing Scripts/Notebooks

- **vectorizer.ipynb**: Converts ISW reports into numerical vectors (e.g., using TF-IDF and PCA) for use in machine learning models, handling unstructured text data.

- **prepare_final_dataset.ipynb**: Merges all data sources (ISW, weather, air alerts) into a unified dataset, ensuring alignment for modeling.

---

### Machine Learning Notebooks

- **logistic_regression.ipynb**: Implements a Logistic Regression model for air alert prediction, suitable for binary classification (alert vs. no alert).

- **random_forest.ipynb**: Implements a RandomForestClassifier, which can capture non-linear relationships in the data for potentially better prediction accuracy.

- **linear_regression.ipynb**: Its purpose is unclear since air alert prediction is typically a classification task, which is shown in it.

---

### Utility Scripts

- **\_\_init\_\_.py**: Makes the `src/` directory a Python package for modular imports.

- **db_loader.py**: Designed to load data into a database but is currently unused.

- **main.py**: Launches a Flask-based microservice website to display predictions or visualizations using the `templates/` folder.



## Requirements
To run this project, ensure you have the following:

- **Python 3.x** installed on your system
- Required dependencies (listed in `requirements.txt`)

*Recomendations:*
- at least 32GB of RAM
## Installation
Follow these steps to set up the project:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/HliebOcheretianyi/H2_python_structure_and_data.git
   cd H2_python_structure_and_data
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Run the Jupyter notebooks in sequence:

__vectorizer.ipynb → prepare_final_dataset.ipynb → Logistic_regression.ipynb / RandomForestClassifier.ipynb__

Ensure datasets (ISW.csv, alarms.csv, weather_by_hour.csv, regions.csv) are available in the working directory.


Depending on the specific functionality required, you can also run other scripts individually.

## Contributing
Contributions are welcome! If you want to improve the project, follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them with a descriptive message.
4. Push your branch to your forked repository.
5. Submit a pull request with a detailed description of your modifications.

