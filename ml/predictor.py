from pathlib import Path
import numpy as np,joblib
ROOT=Path(__file__).resolve().parent.parent; MP=ROOT/'models'/'iiot_lstm.keras'; SP=ROOT/'models'/'scaler.joblib'; FEATURES=['cpu','memory','packets_per_second','failed_logins','command_rate','network_latency','sensor_variance']; model=None; scaler=None
def load():
 global model,scaler
 if model is None and MP.exists() and SP.exists():
  from tensorflow.keras.models import load_model
  model=load_model(MP); scaler=joblib.load(SP)
def fallback(seq):
 if not seq:return 1.0
 s=[]
 for r in seq:s.append(.20*min(float(r.get('cpu',50))/100,1)+.15*min(float(r.get('memory',50))/100,1)+.15*min(float(r.get('packets_per_second',80))/250,1)+.20*min(float(r.get('failed_logins',0))/8,1)+.10*min(float(r.get('command_rate',20))/80,1)+.10*min(float(r.get('network_latency',15))/80,1)+.10*min(float(r.get('sensor_variance',.1)),1))
 return float(np.clip(np.mean(s),0,1))
def predict_anomaly(seq):
 load()
 if not seq:return {'anomaly_score':1.0,'status':'anomalous','model_available':model is not None}
 if model is None:
  score=fallback(seq); return {'anomaly_score':round(score,4),'status':'anomalous' if score>.5 else 'normal','model_available':False}
 seq=(seq+[seq[-1]]*max(0,10-len(seq)))[:10]; mat=np.array([[float(r.get(f,0)) for f in FEATURES] for r in seq],dtype='float32'); scaled=scaler.transform(mat).reshape(1,10,len(FEATURES)); score=float(model.predict(scaled,verbose=0)[0][0]); return {'anomaly_score':round(score,4),'status':'anomalous' if score>=.5 else 'normal','model_available':True}
