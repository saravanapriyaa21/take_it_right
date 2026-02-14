# Take It Right

**A Deterministic Medication Safety Risk Analyzer with an AI Explanation Layer**

Take It Right is a clinically structured medication safety engine designed to help users evaluate everyday dosing decisions using transparent, rule-based logic.

It combines:

* A deterministic medical safety engine
* A weight-based dosing validator
* A structured risk scoring system
* A clean interactive dashboard
* An optional AI explanation layer for human-friendly interpretation

The system prioritizes clarity, explicit safety rules, and deterministic overrides — not probabilistic guesswork.

---

## 🔗 Live Demo

Try the deployed application here:

👉 **[https://your-render-url.onrender.com](https://your-render-url.onrender.com)**

⚠️ Note: If hosted on a free tier, the backend may take a few seconds to wake up after inactivity.

---

## Why This Project Exists

Many individuals hesitate to consult a doctor for minor medication questions and instead self-medicate. While common medicines such as paracetamol are generally safe, misuse through:

* Overdosing
* Alcohol combination
* Hidden duplicate ingredients
* Incorrect pediatric dosing
* Unsafe stacking with NSAIDs

can create serious health risks.

Take It Right provides structured safety evaluation using deterministic medical logic before any AI explanation is generated.

---

# System Architecture

### Deterministic Safety Engine (Core Logic)

The backend is rule-driven and does **not rely on AI for medical decision-making**.

It evaluates:

* Dose limits
* mg/kg thresholds
* Time spacing validation
* Drug interactions
* Contraindications
* Organ stress scoring

The AI layer is strictly explanatory. It does not influence risk classification.

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
* Alcohol interaction escalation (automatic HIGH RISK override)
* Liver, Kidney, and Stomach load scoring
* Conflict deduplication with severity prioritization
* Deterministic HIGH RISK override for critical violations
* Structured, context-aware guidance generation

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

Critical violations override numeric scoring to ensure safety-first logic.

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

## Backend

* Python
* Flask
* Custom deterministic rule engine
* JSON-configured medication rules

## Frontend

* React
* Vite
* Plotly.js
* CSS design tokens

## AI Layer

* Explanation generator
* Converts structured engine output into human-readable interpretation
* Does not affect risk computation

---

# Local Setup

## Backend

```bash
git clone https://github.com/saravanapriyaa21/take_it_right.git
cd take_it_right

python -m venv venv
source venv/bin/activate   # macOS/Linux
# venv\Scripts\activate    # Windows

pip install -r requirements.txt

python -m api.app
```

Backend runs on:

```
http://127.0.0.1:5050
```

---

## Frontend

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
├── test_engine.py     # Engine validation scenarios
├── requirements.txt
└── README.md
```

---

## Key Design Philosophy

* Deterministic before generative
* Explicit safety overrides over probabilistic inference
* Transparent and auditable risk scoring
* Separation of decision logic and explanation layer

---

# Disclaimer

This tool provides general medication safety analysis based on structured rule logic.
It does not replace professional medical consultation.

For severe symptoms, chronic conditions, pregnancy complications, or emergencies, consult a qualified healthcare professional.

---

# License

MIT License
