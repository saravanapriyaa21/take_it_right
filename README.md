# Take It Right

**A Deterministic Medication Safety Risk Analyzer with AI Explanation Layer**

Take It Right is a clinically structured medication safety engine designed to help users evaluate everyday dosing decisions using rule-based logic.

It combines:

* A **deterministic medical safety engine**
* A **weight-based dosing validator**
* A **risk scoring system**
* A clean **interactive dashboard**
* An optional **AI explanation layer** for human-friendly interpretation

The goal is clarity, safety, and structured reasoning — not guesswork.

---

## Why This Project Exists

Many people hesitate to consult a doctor for minor medication questions and instead self-medicate. While common medicines like paracetamol are generally safe, misuse through:

* Overdosing
* Alcohol combination
* Hidden duplicate ingredients
* Incorrect pediatric dosing
* Unsafe stacking with NSAIDs

can create real harm.

Take It Right provides structured risk analysis using deterministic rules before any AI explanation is generated.

---

# System Architecture

### Deterministic Safety Engine (Core Logic)

The backend is rule-driven and does **not rely on AI for medical decisions**.

It evaluates:

* Dose limits
* mg/kg thresholds
* Time spacing
* Drug interactions
* Contraindications
* Organ stress scoring

AI is only used to convert structured results into readable explanations.

---

# Safety Logic Coverage

The deterministic engine includes:

* Weight-based pediatric dosing (mg/kg validation)
* Age-based restriction checks
* Pregnancy contraindication detection
* Daily dose accumulation logic
* Single-dose maximum enforcement
* Brand → ingredient expansion (e.g., Crocin → Paracetamol)
* Hidden duplicate ingredient detection
* NSAID stacking detection
* Alcohol interaction escalation (automatic HIGH RISK)
* Liver, Kidney, and Stomach load scoring
* Conflict deduplication with severity prioritization
* Deterministic HIGH RISK override for critical conditions
* Structured guidance generation

---

# Risk Model

The system produces:

* **Risk Score (0–100)**
* **Risk Level**

  * SAFE
  * CAUTION
  * HIGH RISK
* Organ load metrics
* Structured conflicts
* Actionable guidance

Critical violations automatically override scoring logic.

---

# Frontend Dashboard

The frontend provides:

* Circular risk gauge visualization
* Liver / Kidney / Stomach metric bars
* Conflict cards with severity indicators
* Actionable guidance panel
* Optional AI explanation panel
* Dose spacing timeline visualization
* Quick demo scenarios
* Clean medical-themed UI

Built with:

* React
* Vite
* Plotly.js
* Lucide Icons

---

# Example Scenarios Covered

* Safe adult dosing
* Pediatric mg/kg overdose
* Alcohol + Paracetamol toxicity
* NSAID stacking
* Hidden duplicate brand stacking
* Pregnancy contraindication
* Age restriction violations
* Midnight dose spacing
* Daily accumulation overdose
* Organ load escalation

---

# Tech Stack

**Backend**

* Python
* Flask
* Custom rule engine
* JSON configuration for medication rules

**Frontend**

* React
* Vite
* Plotly.js
* CSS-based design tokens

**AI Layer**

* Optional explanation generator
* Converts deterministic output into human-readable language
* Does not influence risk calculation

---

# Local Setup

## Backend Setup

```bash
# Clone repository
git clone https://github.com/your-username/take_it_right.git
cd take_it_right

# Create virtual environment
python -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Run backend
python -m api.app
```

Backend runs on:

```
http://127.0.0.1:5050
```

---

## Frontend Setup

```bash
cd frontend

npm install
npm run dev
```

Frontend runs on:

```
http://localhost:5173
```

---

# Project Structure

```
take_it_right/
│
├── engine/            # Deterministic safety logic
├── api/               # Flask API
├── ai/                # Explanation generator
├── frontend/          # React dashboard
├── test_engine.py     # Engine test scenarios
├── requirements.txt
└── README.md
```

---
## Key Design Philosophy

- Deterministic before generative
- Explicit safety overrides over probabilistic inference
- Transparent risk scoring

---

# Disclaimer

This tool provides general medication safety analysis based on structured rule logic.
It does not replace professional medical consultation.

For severe symptoms, chronic conditions, pregnancy complications, or emergencies, consult a qualified healthcare professional.

---

# License

MIT License
