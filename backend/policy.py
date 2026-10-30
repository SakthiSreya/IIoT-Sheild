from backend.config import STEP_UP_ANOMALY,ALLOW_FINGERPRINT,STEP_UP_FINGERPRINT
def calculate_risk(anomaly,fingerprint,known,authenticated=True):
    risk=.25*(0 if known and authenticated else 1)+.35*(1-fingerprint)+.40*anomaly
    return round(min(max(risk,0),1),4)
def make_decision(anomaly,fingerprint,known,authenticated=True):
    risk=calculate_risk(anomaly,fingerprint,known,authenticated)
    if not known or not authenticated:return 'BLOCK',risk,'Device identity could not be trusted.'
    if fingerprint<STEP_UP_FINGERPRINT or anomaly>STEP_UP_ANOMALY:return 'BLOCK',risk,'High-risk fingerprint or behavioral anomaly detected.'
    if fingerprint<ALLOW_FINGERPRINT or anomaly>.35:return 'STEP-UP',risk,'Additional verification is required.'
    return 'ALLOW',risk,'Identity, fingerprint and behavior satisfy policy.'
