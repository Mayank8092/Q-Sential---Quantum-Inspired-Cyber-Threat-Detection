# 🦉 NightOwl — Quantum Digital Signature (QDS) Verification + Cyber-Threat Detection

**SIH Prototype** — Simulated Transaction + Teleportation-based QDS Environment

NightOwl is **not** a real payment interceptor. It is a complete demonstration system that shows how a future real Quantum Digital Signature system would protect transactions.

---

## What the normal user sees

```
┌─────────────────────────────────┐
│            NIGHTOWL              │
│       Secure QDS Transaction     │
│                                  │
│ Amount                           │
│ ₹ [ 1000                    ]    │
│                                  │
│ Receiver                         │
│ [ Maya                      ]    │
│                                  │
│        [ SEND SECURELY ]         │
└─────────────────────────────────┘
```

User only enters **Amount** + **Receiver** (and Sender).  
Everything else (Transaction ID, Nonce, Hash, Bell state, Teleportation, Pauli, Measurement, Signature) is generated automatically.

---

## Pages

| Route            | Purpose                                      |
|------------------|----------------------------------------------|
| `/`              | Dashboard – stats + latest verifications     |
| `/generate`      | Generate a secure transaction + QDS package  |
| `/verify`        | Paste/upload a QDS package and verify it     |
| `/attacks`       | Attack Simulator (Forgery, Replay, etc.)     |
| `/history`       | Full verification history                    |
| `/reports`       | Security / threat reports                    |
| `/api/docs`      | Interactive Swagger API documentation        |

---

## Architecture

```
Next.js / React style UI (Jinja2 + vanilla JS)
            │
            ▼
     Python FastAPI
            │
   ┌────────┼────────┐
   ▼        ▼        ▼
Input    Security   QDS Module
Validator Validator     │
                        ▼
                  Qiskit Engine
                  (Bell → Teleport → Pauli → Measure)
                        │
                        ▼
                 Statistics Engine
                        │
                        ▼
                  Decision Engine → ACCEPT / FLAG / REJECT
```

---

## Quick Start (VS Code)

### 1. Open the project
```bash
cd NightOwl
code .
```

### 2. Create virtual environment & install
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Run the server
```bash
# From the backend folder
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Open in browser
```
http://127.0.0.1:8000/
```

API docs: `http://127.0.0.1:8000/api/docs`

---

## Recommended Demo Flow for Judges

1. **Dashboard** → show empty stats  
2. **Generate Transaction** → Alice → Maya → ₹1000 → SEND SECURELY  
3. Copy the generated package JSON  
4. **Verify QDS** → paste → VERIFY → see ✅ ACCEPTED  
5. **Attack Simulator**  
   - Run **Normal** → ACCEPTED  
   - Run **Forgery** → 🚨 REJECTED (FORGERY)  
   - Run **Replay** → 🚨 REPLAY ATTACK  
   - Run **Impersonation** → 🚨 IMPERSONATION  
   - Run **Channel** → 🚨 CHANNEL ANOMALY  
6. **History** & **Security Reports** → show all results

---

## Project Structure

```
NightOwl/
├── backend/
│   ├── main.py                 # FastAPI entry + page routes
│   ├── requirements.txt
│   ├── api/
│   │   ├── transactions.py     # POST /api/transactions
│   │   ├── verification.py     # POST /api/verify
│   │   ├── attacks.py          # POST /api/simulate-attack
│   │   └── dashboard.py
│   ├── qds/
│   │   ├── protocol.py         # Full QDS generate + verify
│   │   ├── bell_state.py
│   │   ├── teleportation.py
│   │   ├── pauli.py
│   │   └── measurement.py
│   ├── security/
│   │   ├── validation.py
│   │   ├── identity.py
│   │   ├── replay.py
│   │   └── timestamp.py
│   ├── analysis/
│   │   ├── statistics.py
│   │   └── threshold.py
│   ├── attacks/
│   │   └── simulator.py
│   └── database/
│       └── db.py               # Simple JSON persistence
│
├── frontend/
│   ├── templates/              # Jinja2 pages
│   └── static/
│       ├── css/style.css
│       └── js/app.js
│
└── README.md
```

---

## Tech Stack

- **Backend**: Python 3.10+, FastAPI, Uvicorn
- **Quantum**: Qiskit + Qiskit Aer (simulator)
- **Frontend**: Jinja2 templates + modern CSS + vanilla JS
- **Storage**: JSON file (no external DB needed for prototype)

---

## Notes for SIH

- This is a **simulated** QDS environment.
- The exact mathematical form of the QDS signature follows a teleportation-based protocol implemented with Qiskit.
- NightOwl never intercepts real Google Pay / UPI traffic.
- All quantum operations run on the classical AerSimulator for demonstration.

Built for Smart India Hackathon.
