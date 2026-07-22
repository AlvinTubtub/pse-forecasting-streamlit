# PSE Forecasting Streamlit Dashboard

A Streamlit-based web application for forecasting Philippine Stock Exchange (PSE) stock prices using multiple forecasting models. The dashboard enables users to upload historical stock data, generate forecasts, compare model performance, and visualize prediction results through an interactive interface.

## Features

* Interactive Streamlit dashboard
* Upload historical stock price datasets (CSV)
* Generate stock price forecasts
* Compare multiple forecasting models
* View performance metrics
* Interactive charts and visualizations
* Download prediction results

---

# Project Structure

```text
pse-forecasting-streamlit/
│
├── app.py
├── requirements.txt
├── services/
├── pages/
├── assets/
├── models/
├── utils/
└── README.md
```

---

# Prerequisites

Before running the application, install:

* Python 3.11 or Python 3.12 (recommended)
* Git
* Visual Studio Code (recommended)

> **Note:** Python 3.13 may cause compatibility issues with some scientific libraries such as `statsmodels`.

---

# Installation

## 1. Clone the repository

```bash
git clone https://github.com/AlvinTubtub/pse-forecasting-streamlit.git
```

## 2. Navigate to the project

```bash
cd pse-forecasting-streamlit
```

## 3. Create a virtual environment

### macOS / Linux

```bash
python3 -m venv .venv
```

### Windows

```powershell
python -m venv .venv
```

---

## 4. Activate the virtual environment

### macOS / Linux

```bash
source .venv/bin/activate
```

### Windows Command Prompt

```cmd
.venv\Scripts\activate
```

### Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

---

## 5. Upgrade pip

```bash
python -m pip install --upgrade pip
```

---

## 6. Install project dependencies

```bash
pip install -r requirements.txt
```

---

# Running the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

After a few seconds, Streamlit will display a local URL similar to:

```text
http://localhost:8501
```

Open the URL in your web browser.

---

# How to Use

1. Launch the application.
2. Navigate through the dashboard pages.
3. Upload a CSV file containing historical stock price data.
4. Configure the forecasting options (if applicable).
5. Click the prediction or forecast button.
6. Review the generated forecasts.
7. Compare model performance metrics.
8. Download prediction results if supported.

---

# Installing Additional Dependencies

If new packages are added during development:

```bash
pip install package_name
```

Update the requirements file:

```bash
pip freeze > requirements.txt
```

---

# Common Issues

## ModuleNotFoundError

Install all required dependencies:

```bash
pip install -r requirements.txt
```

---

## Streamlit command not found

Run:

```bash
python -m streamlit run app.py
```

---

## Port already in use

Run Streamlit on another port:

```bash
streamlit run app.py --server.port 8502
```

---

## Python Version Compatibility

Recommended versions:

* Python 3.11
* Python 3.12

Some forecasting libraries may not yet fully support Python 3.13.

---

# Updating the Repository

After making changes:

```bash
git add .
git commit -m "Describe your changes"
git push origin main
```

---

# Technologies Used

* Python
* Streamlit
* Pandas
* NumPy
* Scikit-learn
* Statsmodels
* PyTorch

---

# License

This project is intended for educational and academic purposes.
