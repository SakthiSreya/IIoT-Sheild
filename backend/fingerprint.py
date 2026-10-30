import numpy as np
DEVICE_REGISTRY={
'PLC-001':{'device_type':'PLC','os':'RTOS','firmware':'v2.4.1','mac_prefix':'AA:10','protocol':'MODBUS','cpu':72,'memory':54,'network_latency':12},
'SENSOR-007':{'device_type':'Sensor','os':'Embedded','firmware':'v1.8.0','mac_prefix':'BB:20','protocol':'MQTT','cpu':31,'memory':38,'network_latency':18},
'ROBOT-003':{'device_type':'Robot','os':'Embedded Linux','firmware':'v3.1.2','mac_prefix':'CC:30','protocol':'MQTT','cpu':64,'memory':61,'network_latency':15}}
def fingerprint_similarity(device_id,incoming):
    enrolled=DEVICE_REGISTRY.get(device_id)
    if not enrolled:return 0.0,['Unknown device ID']
    scores=[]; mismatches=[]
    for k in ['cpu','memory','network_latency']:
        e=float(enrolled[k]); a=float(incoming.get(k,e)); tol=max(abs(e)*.35,10); scores.append(1-min(abs(e-a)/tol,1))
    for k in ['device_type','os','firmware','mac_prefix','protocol']:
        if incoming.get(k,enrolled[k])==enrolled[k]:scores.append(1)
        else:scores.append(0); mismatches.append(f'{k} mismatch')
    return round(float(np.mean(scores)),4),mismatches
