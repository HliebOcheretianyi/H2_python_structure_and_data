# Air Alerms Predicting

## Description
This repository houses a collection of scripts tailored for a data science workflow, emphasizing the collection, processing, and storage of datasets related to Ukraine, insights from the Institute for the Study of War (ISW), and other relevant data sources. The project streamlines the data science pipeline by automating data acquisition, cleaning, and structuring, enabling real-time updates and efficient storage for downstream analysis.

Additionally, it serves as a practical example of applying machine learning in data science, specifically for predictive modeling. The repository is designed to predict air alerts using machine learning techniques, specifically using an ensemble of Xgboost, LightGBM, Random Forest models, showcasing the end-to-end process of data preparation, model training, and evaluation.

# Project Structure and File Overview

## Directory Structure

- **data/**: A dedicated directory for storing datasets. Users are required to acquire air alert and weather data for at least two years.

- **src/**: The core of the project, containing scripts and Jupyter notebooks for data processing and modeling.
- model_building/: Building Models below.
- our_models/: Saves trained models, scalers and files that take a long time if the code is restarted (.pkl files).
- predict_data/: everyhour_predict - saves current data for prediction, forecast - saves hourly updated forecast.
- prepar_notebooks/: Keeps Jupyter notebooks with training different models and Data Processing Scripts/Notebooks below.
- preparations/: Data Collection Scripts below.
- templates/: Holds HTML templates for rendering web pages via Flask, suggesting a web interface for visualizing predictions or results.
  
- **app.py**: UI.
  
- **current_data.py**: Collect current data to necessary form for prediction.
  
- **predictions.py**: Generates forecast for next 24 hours and save it to forecast.

---

## File Breakdown and Functionality

### Building Models

- **stacking_models.py**: Defines and configures a stacking ensemble classifier, which combines multiple base models (e.g., Logistic Regression, Random Forest, XGBoost).
  
- **tokenizer.py**: Used to preprocess ISW textual data by splitting it into tokens and reducing words to their base form before vectorization.
  
- **vectorizer.py**:  It transforms new cleaned ISW reports into numerical features suitable for input into machine learning models.

---

### Data Collection Scripts

- **ISW_everyday_update.py**: Automates daily updates of ISW data to keep the dataset current for real-time analysis.

- **ISW_history.py**: Collects historical ISW data, likely used to build a baseline dataset for training models.

- **weather_scrap.py**: Scrapes weather data from Visual Crossing, providing features like temperature or precipitation that may correlate with air alerts.

- **alerts_in_ua.py**: Fetches real-time air raid alerts in Ukraine.

---

### Data Processing Scripts/Notebooks

- **vectorizer.ipynb**: Converts ISW reports into numerical vectors (e.g., using TF-IDF and PCA) for use in machine learning models, handling unstructured text data.
  
- **prepare_final_dataset.ipynb**: Merges all data sources (ISW, weather, air alerts) into a unified dataset, ensuring alignment for modeling.
  
- **stacked.ipynb**: Combines predictions via stacking ensemble.
  
- **current_data.ipynb**: Collect current data to necessary form for prediction.
  
- **feature_2.ipynb**: Adds holidays.
  
- **predict.ipynb**: Generates forecast for next 24 hours and save it to forecast.
---

### Machine Learning Notebooks

- **LightGBM.ipynb**:  Implements a LightGBM classifier optimized for binary classification of air alerts.
  
- **Logistic_regression.ipynb**: Implements a Logistic Regression model for air alert prediction, suitable for binary classification (alert vs. no alert).
  
- **Random_forest.ipynb**:Implements a RandomForestClassifier, which can capture non-linear relationships in the data for potentially better prediction accuracy.
  
- **SGDclassifier.ipynb**: Applies a Stochastic Gradient Descent (SGD)-based linear classifier, suitable for large-scale and sparse data.
  
- **XGboost.ipynb**: Implements an XGBoost classifier, a powerful gradient boosting model often used in structured data competitions due to its performance and handling of imbalanced datasets.
---

### Utility Scripts

- **\_\_init\_\_.py**: Makes the `src/` directory a Python package for modular imports.

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

Run those if you DON`T HAVE TRAINED MODELS
__vectorizer.ipynb → prepare_final_dataset.ipynb →LightGBM.ipynb/Random_forest.ipynb/XGboost.ipynb → stacked.ipynb 
If you done previous step or you HAVE TRAINED MODELS run 
current_data.py → predictions.py

Ensure datasets (ISW.csv, alarms.csv, weather_by_hour.csv, regions.csv) are available in the working directory.

Depending on the specific functionality required, you can also run other scripts individually.

## Contributing
Contributions are welcome! If you want to improve the project, follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them with a descriptive message.
4. Push your branch to your forked repository.
5. Submit a pull request with a detailed description of your modifications.

