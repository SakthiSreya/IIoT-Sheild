const d = document.getElementById('device'),
      s = document.getElementById('scenario'),
      btn = document.getElementById('testBtn');

const base = {
  "PLC-001":   {device_type:'PLC',    os:'RTOS',           firmware:'v2.4.1', mac_prefix:'AA:10', protocol:'MODBUS', cpu:72, memory:54, network_latency:12},
  "SENSOR-007":{device_type:'Sensor', os:'Embedded',       firmware:'v1.8.0', mac_prefix:'BB:20', protocol:'MQTT',   cpu:31, memory:38, network_latency:18},
  "ROBOT-003": {device_type:'Robot',  os:'Embedded Linux', firmware:'v3.1.2', mac_prefix:'CC:30', protocol:'MQTT',   cpu:64, memory:61, network_latency:15}
};

function seq(bad) {
  return Array.from({length: 10}, () => bad ? {
    cpu: 82 + Math.random()*15, memory: 70 + Math.random()*18,
    packets_per_second: 190 + Math.random()*80, failed_logins: 3 + Math.floor(Math.random()*6),
    command_rate: 45 + Math.random()*35, network_latency: 40 + Math.random()*35,
    sensor_variance: .45 + Math.random()*.45
  } : {
    cpu: 55 + Math.random()*8, memory: 50 + Math.random()*7,
    packets_per_second: 80 + Math.random()*12, failed_logins: Math.random() < .2 ? 1 : 0,
    command_rate: 20 + Math.random()*4, network_latency: 15 + Math.random()*3,
    sensor_variance: .08 + Math.random()*.08
  });
}

function fp(id, changed) {
  let x = {...base[id]};
  if (changed) { x.firmware = 'unknown-v9'; x.mac_prefix = 'ZZ:99'; x.cpu += 30; x.memory += 20; }
  return x;
}

async function load() {
  try {
    let r = await fetch('/api/devices'), a = await r.json();
    d.innerHTML = a.map(x => `<option value="${x.device_id}">${x.device_id} (${x.device_type})</option>`).join('');
    put('modelStatus', '● LSTM model ready'); preview();
  } catch (e) {
    put('modelStatus', 'Backend not reachable'); preview();
  }
}

const ICONS={
  PLC:'<svg viewBox="0 0 64 64"><rect x="8" y="16" width="48" height="32" rx="5"/><circle cx="20" cy="28" r="2.5"/><circle cx="30" cy="28" r="2.5"/><circle cx="40" cy="28" r="2.5"/><path d="M16 39h32"/></svg>',
  Sensor:'<svg viewBox="0 0 64 64"><circle cx="32" cy="32" r="6"/><circle cx="32" cy="32" r="16"/><path d="M12 32a20 20 0 0 1 4-12M52 32a20 20 0 0 0-4-12"/></svg>',
  Robot:'<svg viewBox="0 0 64 64"><rect x="12" y="50" width="30" height="8" rx="2"/><path d="M27 50L18 30l24-12"/><circle cx="42" cy="18" r="5"/><path d="M47 18h8"/></svg>',
  Unknown:'<svg viewBox="0 0 64 64"><circle cx="32" cy="32" r="22"/><path d="M26 26a6 6 0 1 1 8 5.6c-1.5.7-2 1.8-2 3.4M32 43v1"/></svg>'
};
function preview(){
  const el=document.getElementById('devicePreview'), unk=s.value==='unknown', id=d.value, b=base[id];
  if(unk||!b){el.innerHTML=`<div class="pv-ic">${ICONS.Unknown}</div><div><div class="pv-t">${unk?'UNKNOWN-999':(id||'No device')}</div><div class="pv-s"><span>Status</span><b>${unk?'Not registered':'No profile'}</b></div></div>`;return;}
  el.innerHTML=`<div class="pv-ic">${ICONS[b.device_type]||ICONS.PLC}</div><div><div class="pv-t">${id}</div><div class="pv-s"><span>Type</span><b>${b.device_type}</b><span>OS</span><b>${b.os}</b><span>Firmware</span><b>${b.firmware}</b><span>Protocol</span><b>${b.protocol}</b></div></div>`;
}
d.onchange=preview; s.onchange=preview;
function put(id, v) { document.getElementById(id).textContent = v; }

function bar(id, v, invert) {
  const el = document.getElementById(id);
  el.style.width = Math.min(100, Math.max(0, v * 100)) + '%';
  // risk and anomaly: high is bad. fingerprint: low is bad.
  const bad = invert ? v < .6 : v > .6, mid = invert ? v < .85 : v > .35;
  el.style.background = bad ? 'var(--bad)' : mid ? '#d98a00' : 'var(--ok)';
}

function signal(id, text) {
  put(id, text);
  const box = document.getElementById(id).closest('.sig');
  const bad = /fail|unknown|mismatch|anomal|suspic|chang|high|block|invalid|untrusted/i.test(String(text));
  box.className = 'sig ' + (bad ? 'bad' : 'good');
}

function addLog(scenarioText, deviceId, decision) {
  const log = document.getElementById('log');
  const empty = log.querySelector('.empty'); if (empty) empty.remove();
  const li = document.createElement('li');
  const cls = decision === 'ALLOW' ? 'allow' : decision === 'STEP-UP' ? 'step-up' : 'block';
  li.innerHTML = `<span class="t">${new Date().toLocaleTimeString([], {hour:'2-digit',minute:'2-digit',second:'2-digit'})}</span>
                  <span><b>${deviceId}</b><small>${scenarioText}</small></span><span></span><span class="tag ${cls}">${decision}</span>`;
  log.prepend(li);
  while (log.children.length > 6) log.lastChild.remove();
}

btn.onclick = async () => {
  btn.disabled = true; btn.textContent = 'Verifying…';
  const scenario = s.value, known = scenario !== 'unknown', id = known ? d.value : 'UNKNOWN-999';
  const payload = {
    device_id: id, authenticated: true,
    fingerprint: fp(known ? id : 'PLC-001', scenario === 'fingerprint'),
    behavior: {sequence: seq(scenario === 'behavior')}
  };
  try {
    const r = await fetch('/api/authenticate', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(payload)});
    const x = await r.json();
    const el = document.getElementById('decision');
    const cls = x.decision === 'ALLOW' ? 'allow' : x.decision === 'STEP-UP' ? 'step-up' : 'block';
    el.textContent = x.decision; el.className = 'chip ' + cls;
    document.getElementById('decisionCard').dataset.state = cls;

    put('reason', x.reason);
    put('risk', (x.risk_score*100).toFixed(1) + '%');
    put('fingerprint', (x.fingerprint_similarity*100).toFixed(1) + '%');
    put('anomaly', (x.anomaly_score*100).toFixed(1) + '%');
    bar('riskBar', x.risk_score); bar('fpBar', x.fingerprint_similarity, true); bar('anBar', x.anomaly_score);

    signal('identity', x.signals.identity);
    signal('fpSignal', x.signals.fingerprint);
    signal('behaviorSignal', x.signals.behavior);

    addLog(s.options[s.selectedIndex].text, id, x.decision);
  } catch (e) {
    put('reason', 'Backend connection failed. Start the server with app.py and try again.');
  } finally {
    btn.disabled = false; btn.textContent = 'Verify device';
  }
};

load();