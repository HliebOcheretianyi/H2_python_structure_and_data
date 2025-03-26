# H2 Python Structure and Data

## Description
This repository contains a set of scripts designed for collecting, processing, and storing data related to Ukraine, analytics from the Institute for the Study of War (ISW), and other valuable datasets. The project facilitates automated data gathering and processing, with a focus on real-time updates and structured storage.

In the future, it will be able to predict air alerts

## Features
The repository consists of several key components:

- **`main.py`** – The main script responsible for launching the microservice website.
- **`ISW_everyday_update.py`** – A script that updates ISW data daily.
- **`ISW_history.py`** – Gathers historical ISW data for analysis.
- **`alerts_in_ua.py`** – Fetches real-time air raid alerts and security warnings in Ukraine.
- **`weather_scrap.py`** – Collects and processes weather data from [Visual Crossing](https://www.visualcrossing.com/).
- **`db_loader.py`** – Loads data into a database (currently not in use).
- **`templates/`** – Contains HTML templates used for rendering web pages in Flask.
- **`ISW.parquet`** – A structured Parquet file storing ISW data for efficient querying and analysis.

## Requirements
To run this project, ensure you have the following:

- **Python 3.x** installed on your system
- Required dependencies (listed in `requirements.txt`)

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
To launch the main script and start the microservice:
```bash
python main.py
```

Depending on the specific functionality required, you can also run other scripts individually. For example:

- Update ISW data:
  ```bash
  python ISW_everyday_update.py
  ```
- Fetch current Ukraine security alerts:
  ```bash
  python alerts_in_ua.py
  ```
- Collect weather data:
  ```bash
  python weather_scrap.py
  ```

## Contributing
Contributions are welcome! If you want to improve the project, follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them with a descriptive message.
4. Push your branch to your forked repository.
5. Submit a pull request with a detailed description of your modifications.

