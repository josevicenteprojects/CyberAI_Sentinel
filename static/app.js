async function fetchJSON(url, opts={}) {
  const res = await fetch(url, opts);
  if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
  return await res.json();
}

async function loadHealth() {
  const data = await fetchJSON('/api/v1/system/health');
  document.getElementById('health').textContent = JSON.stringify(data, null, 2);
}

async function loadModels() {
  const data = await fetchJSON('/api/v1/ml/models');
  document.getElementById('models').textContent = JSON.stringify(data, null, 2);
}

async function loadAnomalies(chart) {
  const data = await fetchJSON('/api/v1/security/anomalies?limit=20');
  const anomalies = data.anomalies || [];
  const labels = anomalies.map(a => a.analysis_timestamp?.slice(11,19) || '');
  const scores = anomalies.map(a => Number((a.anomaly_score||0).toFixed(3)));
  chart.data.labels = labels;
  chart.data.datasets[0].data = scores;
  chart.update();
}

async function trainModels() {
  const btn = document.getElementById('btn-train');
  btn.disabled = true; btn.textContent = 'Entrenando...';
  try { await fetchJSON('/api/v1/ml/train', { method: 'POST' }); await loadModels(); }
  finally { btn.disabled = false; btn.textContent = 'Entrenar Modelos'; }
}

async function analyzeEvent() {
  const btn = document.getElementById('btn-analyze');
  btn.disabled = true; btn.textContent = 'Analizando...';
  try {
    const payload = {
      user_id: 'user_demo', ip_address: '192.168.1.100', event_type: 'login',
      success: true, response_time: Math.random()*1.2, bytes_transferred: 1024,
      hour_of_day: new Date().getHours(), day_of_week: new Date().getDay()
    };
    await fetchJSON('/api/v1/security/analyze', { method: 'POST', headers: { 'Content-Type':'application/json' }, body: JSON.stringify(payload) });
    await loadAnomalies(window.anomalyChart);
  } finally { btn.disabled = false; btn.textContent = 'Analizar Evento'; }
}

function createChart() {
  const ctx = document.getElementById('anomalyChart').getContext('2d');
  return new Chart(ctx, {
    type: 'line',
    data: { labels: [], datasets: [{ label: 'Anomaly Score', data: [], borderColor: '#ef4444', fill: false, tension: 0.25 }] },
    options: { scales: { y: { min: 0, max: 1 } } }
  });
}

window.addEventListener('DOMContentLoaded', async () => {
  window.anomalyChart = createChart();
  document.getElementById('btn-train').addEventListener('click', trainModels);
  document.getElementById('btn-analyze').addEventListener('click', analyzeEvent);
  await loadHealth();
  await loadModels();
  await loadAnomalies(window.anomalyChart);
});


