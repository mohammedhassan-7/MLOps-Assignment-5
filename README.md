# MLflow CI/CD Pipeline Assignment

This repository contains a complete CI/CD pipeline for training, validating, and (mock) deploying a PyTorch image classifier using MLflow, DVC, Docker, and GitHub Actions.

## Features
- **MLflow Tracking**: Logs metrics and models to a remote MLflow server 
- **DVC**: Manages and pulls the dataset from Kaggle
- **GitHub Actions**: Two-stage workflow (validate, deploy) with linting, artifact passing, and threshold checks
- **Docker**: Minimal Dockerfile for mock deployment

## Usage

### 1. Prerequisites
- Python 3.10+
- [Kaggle API credentials](https://www.kaggle.com/docs/api)
- MLflow tracking server 

### 2. Environment Setup
```sh
pip install -r requirements.txt
```

### 3. Training Locally
```sh
export KAGGLE_USERNAME=your_kaggle_username
export KAGGLE_KEY=your_kaggle_key
export MLFLOW_TRACKING_URI=your_mlflow_tracking_uri
python train.py
```

### 4. Running the Pipeline on GitHub Actions
- Push to `main` branch triggers the workflow
- Set the following repository secrets:
  - `KAGGLE_USERNAME`
  - `KAGGLE_KEY`
  - `MLFLOW_TRACKING_URI`

### 5. Files
- `train.py` — Trains and logs the model
- `check_threshold.py` — Checks MLflow accuracy for deployment gating
- `.github/workflows/pipeline.yml` — CI/CD workflow
- `Dockerfile` — Minimal mock deployment

---
