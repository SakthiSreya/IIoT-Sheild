from pathlib import Path
import numpy as np,pandas as pd,joblib,tensorflow as tf
from sklearn.preprocessing import StandardScaler
from tensorflow.keras import Sequential
from tensorflow.keras.layers import LSTM,Dense,Dropout
from tensorflow.keras.callbacks import EarlyStopping
ROOT=Path(__file__).resolve().parent.parent; df=pd.read_csv(ROOT/'data'/'iiot_behavior.csv'); FEATURES=['cpu','memory','packets_per_second','failed_logins','command_rate','network_latency','sensor_variance']
X=[]; y=[]
for _,g in df.groupby('sequence_id'):
 g=g.sort_values('timestamp'); X.append(g[FEATURES].values); y.append(int(g.label.iloc[0]))
X=np.asarray(X,dtype='float32'); y=np.asarray(y,dtype='float32'); scaler=StandardScaler(); X=scaler.fit_transform(X.reshape(-1,len(FEATURES))).reshape(X.shape)
rng=np.random.default_rng(42); idx=rng.permutation(len(X)); split=int(.8*len(idx)); tr,te=idx[:split],idx[split:]
model=Sequential([LSTM(32,input_shape=(10,len(FEATURES))),Dropout(.2),Dense(16,activation='relu'),Dense(1,activation='sigmoid')]); model.compile(optimizer='adam',loss='binary_crossentropy',metrics=['accuracy'])
model.fit(X[tr],y[tr],validation_split=.2,epochs=30,batch_size=32,callbacks=[EarlyStopping(monitor='val_loss',patience=5,restore_best_weights=True)],verbose=1)
loss,acc=model.evaluate(X[te],y[te],verbose=0); (ROOT/'models').mkdir(exist_ok=True); model.save(ROOT/'models'/'iiot_lstm.keras'); joblib.dump(scaler,ROOT/'models'/'scaler.joblib'); print('Test accuracy:',round(float(acc),4))
