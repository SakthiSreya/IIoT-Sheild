# Zero-Trust Authentication in Industrial IoT Using RNN and Device Fingerprinting

Complete academic prototype using Flask + TensorFlow LSTM + device fingerprinting + zero-trust policy + clean frontend.

## Run on Windows

```bat
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python ml\generate_dataset.py
python ml\train_rnn.py
python app.py
```

Open `http://127.0.0.1:5000`.

## Main modules
- `ml/generate_dataset.py`: creates synthetic IIoT telemetry.
- `ml/train_rnn.py`: trains the LSTM behavior classifier.
- `ml/predictor.py`: loads the trained model and predicts anomaly probability.
- `backend/fingerprint.py`: compares incoming device characteristics with enrolled fingerprints.
- `backend/policy.py`: combines identity, fingerprint and behavior into ALLOW / STEP-UP / BLOCK.
- `backend/routes.py`: REST API.
- `frontend/`: dashboard UI.

The generated data is synthetic for demonstration. A real deployment should use actual IIoT telemetry and an enterprise identity/access-control system.
