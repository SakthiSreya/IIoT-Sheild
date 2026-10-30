from pathlib import Path
import numpy as np,pandas as pd
ROOT=Path(__file__).resolve().parent.parent; OUT=ROOT/'data'/'iiot_behavior.csv'; rng=np.random.default_rng(42); rows=[]
for did in ['PLC-001','SENSOR-007','ROBOT-003']:
  for sid in range(300):
    anomaly=sid>=240
    for t in range(10):
      if not anomaly:
        vals=[rng.normal(55,8),rng.normal(50,7),rng.normal(80,12),rng.poisson(.2),rng.normal(20,4),rng.normal(15,3),abs(rng.normal(.12,.04))]
      else:
        vals=[rng.normal(88,7),rng.normal(78,9),rng.normal(220,35),rng.poisson(5),rng.normal(60,12),rng.normal(55,12),abs(rng.normal(.65,.15))]
      rows.append([did,f'{did}_{sid}',t,*[max(float(x),0) for x in vals],int(anomaly)])
pd.DataFrame(rows,columns=['device_id','sequence_id','timestamp','cpu','memory','packets_per_second','failed_logins','command_rate','network_latency','sensor_variance','label']).to_csv(OUT,index=False)
print('Generated',OUT)
