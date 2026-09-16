/* NightOwl frontend helpers */

async function api(path, options = {}) {
  const res = await fetch(path, {
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
    ...options
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || JSON.stringify(err));
  }
  return res.json();
}

function showLoader(id, show = true) {
  const el = document.getElementById(id);
  if (el) el.classList.toggle("show", show);
}

function showResult(id, decision, html) {
  const box = document.getElementById(id);
  if (!box) return;
  box.className = "result-box show " + (decision || "").toLowerCase();
  box.innerHTML = html;
}

function decisionBadge(decision) {
  const cls = decision === "ACCEPTED" ? "ok" : decision === "FLAGGED" ? "warn" : "bad";
  const icon = decision === "ACCEPTED" ? "✅" : decision === "FLAGGED" ? "⚠️" : "🚨";
  return `<div class="decision ${cls}">${icon} ${decision}</div>`;
}

function renderSteps(steps) {
  if (!steps || !steps.length) return "";
  let html = '<ul class="steps">';
  steps.forEach(s => {
    const badge = s.status === "PASS" ? "pass" : s.status === "WARN" ? "warn" : "fail";
    html += `<li><span class="badge ${badge}">${s.status}</span> <strong>${s.step}</strong> — ${s.detail || ""}</li>`;
  });
  html += "</ul>";
  return html;
}

function pretty(obj) {
  return `<pre class="code">${JSON.stringify(obj, null, 2)}</pre>`;
}
