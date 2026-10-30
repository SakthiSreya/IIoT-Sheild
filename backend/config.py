from pathlib import Path
BASE_DIR=Path(__file__).resolve().parent.parent
MODEL_DIR=BASE_DIR/'models'
RNN_MODEL_PATH=MODEL_DIR/'iiot_lstm.keras'
SCALER_PATH=MODEL_DIR/'scaler.joblib'
ALLOW_ANOMALY=0.35
STEP_UP_ANOMALY=0.65
ALLOW_FINGERPRINT=0.85
STEP_UP_FINGERPRINT=0.65
