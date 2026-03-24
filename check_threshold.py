import sys
import os
import mlflow

# Configuration
ACCURACY_THRESHOLD = 0.85
MODEL_INFO_FILE = "model_info.txt"
METRIC_KEY = "accuracy"


def main():
    # 1. Read Run ID from artifact file
    if not os.path.exists(MODEL_INFO_FILE):
        print(f"[ERROR] '{MODEL_INFO_FILE}' not found in current directory.")
        sys.exit(1)

    with open(MODEL_INFO_FILE, "r") as f:
        run_id = f.read().strip()

    if not run_id:
        print("[ERROR] model_info.txt is empty – no Run ID found.")
        sys.exit(1)

    print(f"[INFO] Checking accuracy for MLflow Run ID: {run_id}")

    # 2. Connect to MLflow and fetch the metric
    tracking_uri = os.getenv("MLFLOW_TRACKING_URI")
    if tracking_uri:
        mlflow.set_tracking_uri(tracking_uri)
        print(f"[INFO] Using MLflow Tracking URI: {tracking_uri}")
    else:
        print("[WARNING] MLFLOW_TRACKING_URI not set; using default local store.")

    client = mlflow.tracking.MlflowClient()

    try:
        run_data = client.get_run(run_id)
    except Exception as e:
        print(f"[ERROR] Failed to retrieve run '{run_id}' from MLflow: {e}")
        sys.exit(1)

    metrics = run_data.data.metrics
    if METRIC_KEY not in metrics:
        print(f"[ERROR] Metric '{METRIC_KEY}' not found in run '{run_id}'.")
        print(f"        Available metrics: {list(metrics.keys())}")
        sys.exit(1)

    accuracy = metrics[METRIC_KEY]
    print(f"[INFO] Logged accuracy  : {accuracy:.4f}")
    print(f"[INFO] Required threshold: {ACCURACY_THRESHOLD:.2f}")

    # 3. Gate deployment on threshold
    if accuracy < ACCURACY_THRESHOLD:
        print(
            f"\n[FAIL] Accuracy {accuracy:.4f} is BELOW the threshold of "
            f"{ACCURACY_THRESHOLD}. Deployment blocked."
        )
        sys.exit(1)   # non-zero exit → GitHub Actions marks step as failed

    print(
        f"\n[PASS] Accuracy {accuracy:.4f} meets the threshold of "
        f"{ACCURACY_THRESHOLD}. Proceeding to deployment."
    )
    sys.exit(0)


if __name__ == "__main__":
    main()
