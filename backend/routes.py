from flask import Blueprint,jsonify,request
from backend.fingerprint import DEVICE_REGISTRY,fingerprint_similarity
from backend.policy import make_decision
from ml.predictor import predict_anomaly
api=Blueprint('api',__name__)
@api.get('/health')
def health():return jsonify({'status':'ok','service':'IIoT Zero-Trust Authentication'})
@api.get('/devices')
def devices():return jsonify([{'device_id':k,'device_type':v['device_type'],'protocol':v['protocol'],'firmware':v['firmware']} for k,v in DEVICE_REGISTRY.items()])
@api.post('/authenticate')
def authenticate():
    p=request.get_json(silent=True) or {}; did=p.get('device_id'); known=did in DEVICE_REGISTRY
    fp,mismatches=fingerprint_similarity(did,p.get('fingerprint',{})); pred=predict_anomaly((p.get('behavior') or {}).get('sequence',[]))
    decision,risk,reason=make_decision(pred['anomaly_score'],fp,known,bool(p.get('authenticated',True)))
    return jsonify({'device_id':did,'decision':decision,'risk_score':risk,'reason':reason,'fingerprint_similarity':fp,'fingerprint_mismatches':mismatches,'anomaly_score':pred['anomaly_score'],'behavior_status':pred['status'],'model_available':pred['model_available'],'signals':{'identity':'KNOWN' if known else 'UNKNOWN','fingerprint':'MATCH' if fp>=.85 else 'PARTIAL' if fp>=.65 else 'MISMATCH','behavior':pred['status'].upper()}})
