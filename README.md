# GlycoTwin-AI: Multimodal Digital Twin for Proactive Glycemic Management & Adverse Event Prediction in Indian Diabetic Patients

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-1.0.0-emerald.svg)](https://fastapi.tiangolo.com)
[![DPDP Act 2023 Compliant](https://img.shields.io/badge/Compliance-DPDP_Act_2023_&_HIPAA-brightgreen.svg)](#data-governance--dpdp-act-2023-compliance)
[![Clinical MARD](https://img.shields.io/badge/Clinical_MARD-7.15%25_(Benchmark_<10%25)-purple.svg)](#model-performance--clinical-benchmarking)

> **Happiest Health Reimagining and Reforming Healthcare in India Summit – 2026, Bengaluru**  
> **Challenge:** Proof-of-Concept (PoC) Healthcare Digital Twin Model  
> **Target Condition:** Type 2 Diabetes Mellitus & Postprandial / Nocturnal Dysglycemia (Asian Indian Cohort)  
> **Submission Format:** Public GitHub Repository (`Team GlycoTwin_College Name`)

---

## Table of Contents
1. [Team Details & College / Incubator Information](#team-details--college--incubator-information)
2. [Project Title & Executive Summary](#project-title--executive-summary)
3. [Problem Statement](#problem-statement)
4. [Healthcare Use Case](#healthcare-use-case)
5. [Technical Stack](#technical-stack)
6. [AI / ML Model & Framework Details](#ai--ml-model--framework-details)
7. [Dual Data Streams & Physiological Dynamics](#dual-data-streams--physiological-dynamics)
8. [Data Governance & DPDP Act 2023 Compliance](#data-governance--dpdp-act-2023-compliance)
9. [Model Performance & Clinical Benchmarking](#model-performance--clinical-benchmarking)
10. [Physician "What-If" Counterfactual Simulation Engine](#physician-what-if-counterfactual-simulation-engine)
11. [Clinician Digital Twin UI Cockpit & Live Demo](#clinician-digital-twin-ui-cockpit--live-demo)
12. [Submission Deliverables & Artifact Links (PDF/PPT/Video)](#submission-deliverables--artifact-links)
13. [Open Source License](#open-source-license)

---

## Team Details & College / Incubator Information

- **Project Title:** GlycoTwin-AI
- **Team Name:** LynxieCreations
- **Team Members:**
  1. **Riya Sojitra**
  2. **Tanishqua Trivedi**
- **College / Institution:** V.V.P. Engineering College, Rajkot, Gujarat, India
- **Incubator Information:** Not applicable / Independent Student Innovation
- **Public GitHub Repository Link:** [https://github.com/riyasojitra27-ux/GlycoTwin-AI](https://github.com/riyasojitra27-ux/GlycoTwin-AI)
- **Live Interactive Deployment (GitHub Pages):** [https://riyasojitra27-ux.github.io/GlycoTwin-AI/](https://riyasojitra27-ux.github.io/GlycoTwin-AI/)

### Team Contribution

Our two-member team developed GlycoTwin-AI from the ground up: designing the physiological kinetics, engineering the synthetic EHR and wearable data pipelines, training the dual-head gradient boosted ML models, building the live clinician dashboard with in-silico What-If simulation, and embedding the 15-20 minute AI Guided Presentation tour.

---

## Project Title & Executive Summary

**Project Title:** **GlycoTwin-AI: Multimodal Digital Twin for Proactive Glycemic Management & Adverse Event Prediction in Indian Diabetic Patients**

**Executive Summary:**  
Traditional diabetes care in India is **reactive**—relying on periodic capillary fingersticks and quarterly HbA1c tests that mask intraday glycemic volatility and lethal nocturnal hypoglycemia. **GlycoTwin-AI** is a physiologically grounded, personalized **Healthcare Digital Twin** that dynamically fuses:
1. **Static / Historical Electronic Health Records (EHR)**: Demographics, Asian Indian Phenotype metrics (visceral adiposity at BMI $\ge 23$), baseline HbA1c, renal function, lipid panels, and pharmacotherapy.
2. **Dynamic / Real-Time Wearable & IoT Sensor Streams**: Continuous Glucose Monitoring (CGM, 5-minute sampling), continuous photoplethysmography (PPG) Heart Rate, Heart Rate Variability (HRV - RMSSD autonomic tone), step cadence, and Indian meal carbohydrate logs.

**Key Outcomes:**
- **2-Hour Ahead Glucose Forecaster:** Predicts continuous glycemic trajectories with a **MARD of 7.15%** (industry gold standard $< 10\%$) and **RMSE of 14.50 mg/dL**.
- **Adverse Event Early Warning:** Flags severe postprandial spikes ($>200\text{ mg/dL}$) and impending nocturnal hypoglycemia ($<70\text{ mg/dL}$) **120 minutes in advance** (Hyperglycemia Precision: 65.31%).
- **Doctor "What-If" Counterfactual Simulator:** Allows clinicians to simulate behavioral and medical adjustments (e.g. post-prandial brisk walk, carbohydrate substitution like swapping white rice for millets, or basal insulin titration) in-silico before prescribing them.

---

## Problem Statement

### The Indian Diabetes Paradox & Failure of Reactive Care
1. **National Epidemic:** As documented by the landmark **ICMR-INDIAB (2023) Study**, India is home to **101.3 million diagnosed diabetics** and **136 million pre-diabetic individuals**, making India the *"Diabetes Capital of the World"*.
2. **The Asian Indian Phenotype:** Indians develop Type 2 Diabetes at younger ages and at lower BMI thresholds ($\ge 23\text{ kg/m}^2$ vs $\ge 25\text{ kg/m}^2$ internationally). They exhibit higher visceral adiposity, hyperinsulinemia, and severe insulin resistance.
3. **Dietary Glycemic Volatility:** Indian staple diets are heavily carbohydrate-dense (polished white rice in South/East India; refined wheat rotis in North/West India), triggering steep postprandial glycemic surges exceeding $220\text{ mg/dL}$.
4. **The Silent Nocturnal Crash:** Sulfonylurea and basal insulin therapy combined with erratic meal timing leads to acute nocturnal hypoglycemia ($<70\text{ mg/dL}$) between 01:00 AM and 04:30 AM, causing autonomic collapse and sudden nocturnal deaths.
5. **The Fatal Flaw of Quarterly HbA1c:** Quarterly HbA1c provides a trailing 3-month average. A patient with extreme peaks ($280\text{ mg/dL}$) and severe valleys ($50\text{ mg/dL}$) may show a misleadingly "normal" HbA1c of 7.2%, masking dangerous glycemic variability.

---

## Healthcare Use Case

1. **Continuous 2-Hour Predictive Early Warning:** Alerting patients and caregivers to impending hypoglycemia ($<70\text{ mg/dL}$) or severe hyperglycemia ($>200\text{ mg/dL}$) two hours before symptoms occur.
2. **In-Silico Counterfactual "What-If" Simulation:** Enabling physicians to test non-pharmacological interventions (e.g., 20-min post-meal brisk walking, 35g foxtail millet carb swap) and medication titrations in a virtual twin before patient execution.
3. **Nocturnal Hypoglycemia Rescue via Autonomic Telemetry:** Cross-coupling HRV RMSSD collapse (sympathetic surge) with interstitial glucose velocity to detect nighttime crashes during sleep.
4. **Primary Health Center (PHC) Democratization:** Integrating with the Ayushman Bharat Digital Mission (ABDM) and ABHA Health IDs to scale specialist-grade endocrinology care across tier-2/3 cities and rural clinics.

---

## Technical Stack

- **Machine Learning & AI:** Python 3.9+, Scikit-Learn (`HistGradientBoostingRegressor`, `HistGradientBoostingClassifier`), NumPy, Pandas
- **Physiological Modeling:** Bergman Minimal Model differential kinetics, non-insulin mediated GLUT-4 muscular glucose clearance, Autonomic Stress Index ($HR / HRV_{RMSSD}$)
- **Backend & APIs:** FastAPI, Uvicorn, Pydantic, RESTful JSON endpoints
- **Frontend & Clinician Cockpit:** HTML5, Tailwind CSS, Chart.js (Dual Synchronized CGM & Wearable Telemetry Charts), FontAwesome
- **AI Speech & Video Teleprompter Engine:** Web Speech API, sentence-by-sentence queue, Chrome keepalive audio synthesis
- **Testing & Quality Assurance:** Python `unittest` integration test suite (`tests/test_pipeline.py`, `tests/test_full_system.py`)
- **Data Standards & Privacy:** Synthea & MIMIC-IV clinical schemas, India DPDP Act 2023 & HIPAA compliance, FHIR ABDM metadata format

---

## AI / ML Model & Framework Details

### The Indian Diabetes Paradox
- **Epidemiology (ICMR-INDIAB 2023 Study):** India has **101.3 million diagnosed diabetics** and **136 million individuals with pre-diabetes**, making it the *"Diabetes Capital of the World"*.
- **The Asian Indian Phenotype:** Indians develop diabetes at a lower mean age and lower BMI threshold ($\ge 23\text{ kg/m}^2$ compared to $\ge 25\text{ kg/m}^2$ internationally). They exhibit higher visceral adiposity, hyperinsulinemia, and significant peripheral insulin resistance.
- **Dietary Glycemic Volatility:** Indian staple diets are heavily carbohydrate-centric (polished white rice in South/East India; refined wheat rotis in North/West India), resulting in steep postprandial glucose surges exceeding $220\text{ mg/dL}$.
- **The Silent Nocturnal Crash:** Sulfonylurea and basal insulin therapy combined with erratic meal timing leads to acute nocturnal hypoglycemia ($<70\text{ mg/dL}$) between 01:00 AM and 04:30 AM, triggering autonomic collapse, cardiac arrhythmias, and sudden nocturnal deaths.
- **The Failure of Reactive Care:** Quarterly HbA1c testing gives a trailing 3-month average. A patient with extreme peaks ($280\text{ mg/dL}$) and severe valleys ($50\text{ mg/dL}$) may show an apparently "normal" HbA1c of 7.2%, hiding life-threatening glycemic volatility.

---

## Dual Data Streams & Physiological Dynamics

The prototype demonstrates end-to-end multimodal fusion across two distinct temporal scales:

```
+--------------------------------------------------------------------------------------------------+
|                                    GLYCOTWIN-AI DATA INGESTION                                   |
+-------------------------------------------------+------------------------------------------------+
|           STREAM 1: STATIC HISTORICAL EHR       |        STREAM 2: DYNAMIC WEARABLE IOT STREAM   |
+-------------------------------------------------+------------------------------------------------+
| - Demographics: Age, Gender, WHR                | - CGM Interstitial Glucose (5-min intervals)   |
| - Asian Indian Phenotype (BMI cutoff >= 23)     | - Wearable PPG Heart Rate (bpm)                |
| - Baseline HbA1c (%) & Fasting Glucose (mg/dL)  | - HRV RMSSD (ms) -> Autonomic Tone             |
| - Renal Biomarkers: eGFR & Serum Creatinine     | - Accelerometry: 5-min step cadence            |
| - Dyslipidemia: Triglycerides & HDL ratio       | - Sleep Stages: Deep, Light, REM, Awake        |
| - Genetic Risk Alleles: TCF7L2 / KCNQ1          | - Indian Meal Carb Logs (Idli, Rice, Roti)     |
| - Comorbidities: Retinopathy, Neuropathy, CVD   | - Circadian Phase (Hour of Day Sine/Cosine)    |
| - Pharmacotherapy: Metformin, SGLT2i, Insulin   | - Event Timestamps & Insulin Injection Logs    |
+-------------------------------------------------+------------------------------------------------+
                                           |                     |
                                           v                     v
+--------------------------------------------------------------------------------------------------+
|                    MULTIMODAL FUSION ENGINE: 42 KINETIC & METABOLIC FEATURES                     |
|  dG/dt (Velocity) | d^2G/dt^2 (Acceleration) | Autonomic Ratio (HR/HRV) | 1h/3h Rolling Mean/CV%  |
+--------------------------------------------------------------------------------------------------+
```

### Physiological Modeling
- **Bergman Minimal Model Kinetics:** Simulates glucose disposal driven by interstitial insulin and hepatic glucose output:
  $$\frac{dG(t)}{dt} = -p_1 [G(t) - G_b] - X(t) G(t) + D(t) - E(t)$$
- **Indian Meal Absorption ($D(t)$):** Rapid gastrointestinal absorption curves reflecting high glycemic index (GI) Indian staples.
- **Exercise Glucose Uptake ($E(t)$):** Models non-insulin-mediated GLUT-4 translocation into skeletal muscle during brisk walking, lowering glucose levels proportionally.
- **Autonomic Nervous Activation:** Pre-hypoglycemic adrenaline surges manifest as plummeting HRV (RMSSD $< 22\text{ ms}$) and relative tachycardia.

---

## Data Governance & DPDP Act 2023 Compliance

- **Indian Digital Personal Data Protection (DPDP) Act 2023 & HIPAA Compliance:**
  - **Zero Real Patient PII:** The training and inference pipelines utilize 100% synthetic and de-identified data generated under strict epidemiological constraints (ICMR-INDIAB distributions).
  - **Synthetic EHR Cohort:** 1,000 synthesized patient records modeled using Synthea and MIMIC-IV clinical schemas.
  - **High-Resolution Wearable Cohort:** 60,120 time-series points representing 14 continuous days per patient at 5-minute sampling frequency.
  - **Patient-Level Isolation:** Train and test splits are partitioned strictly at the patient level (`IND-PT-XXXXX`), eliminating temporal data leakage.

---

## Machine Learning Architecture & Multimodal Fusion

GlycoTwin-AI deploys a **Dual-Head Gradient Boosted Ensemble (HistGradientBoosting / XGBoost)** trained on 42 multimodal features:

1. **Head 1: Continuous 2-Hour Ahead Glucose Forecaster (Regression)**
   - Predicts interstitial glucose level $G(t + 120\text{ mins})$.
   - Dynamically calculates upper and lower 95% confidence intervals based on residual variance.
2. **Head 2: Adverse Event Early Warning Classifier (Classification)**
   - 3-Class Triage System:
     - Class 0: **Controlled / In-Range** ($70 \le G \le 180\text{ mg/dL}$)
     - Class 1: **Severe Postprandial Hyperglycemia Spike** ($G > 200\text{ mg/dL}$)
     - Class 2: **Impending Nocturnal Hypoglycemia** ($G < 70\text{ mg/dL}$)
   - Calibrated clinical risk decision rule prioritizing patient safety (hypoglycemia warning triggers at $18\%$ probability).

---

## Model Performance & Clinical Benchmarking

Evaluated on unseen patient holdouts using strict patient-level separation:

| Evaluation Metric | GlycoTwin-AI Achieved | Clinical Industry Benchmark | Clinical Significance |
| :--- | :--- | :--- | :--- |
| **MARD (%)** | **7.15%** | $< 10.0\%$ (Gold Standard) | High continuous forecasting accuracy |
| **RMSE (mg/dL)** | **14.50 mg/dL** | $< 20.0\text{ mg/dL}$ | Tight prediction bounds around true CGM |
| **MAE (mg/dL)** | **11.11 mg/dL** | $< 15.0\text{ mg/dL}$ | Low average error across daily excursions |
| **Hyperglycemia Precision** | **65.31%** | $> 60.0\%$ | Reliable early warning for postprandial surges |
| **Early Warning Lead Time** | **120 minutes (2 hours)** | $> 60\text{ minutes}$ | Sufficient time for patient/physician action |

---

## Physician "What-If" Counterfactual Simulation Engine

Doctors cannot conduct risky trial-and-error experiments on living patients. The **In-Silico Counterfactual Engine** enables doctors to test interventions digitally before clinical execution:

1. **Post-Prandial Brisk Walk (0 to 45 mins):** Simulates muscular GLUT-4 glucose clearance.
2. **Carbohydrate Swap / Reduction (0 to 60g):** Simulates substituting high-GI white polished rice with foxtail millet or increasing fiber/protein.
3. **Medication Adjustment ($-4\text{U}$ to $+4\text{U}$):** Titrates evening basal insulin or shifts sulfonylurea timing.

**Simulation Execution:** The Digital Twin recalculates the simulated trajectory in $< 50\text{ ms}$, displaying a dashed amber overlay curve against baseline and calculating the projected $\Delta\text{ Glucose (mg/dL)}$ alongside evidence-based clinical recommendations (RSSDI / ADA aligned).

---

## Clinician Digital Twin UI Cockpit

The web application provides a responsive medical cockpit:
- **Virtual Patient Selector:** Switch between clinical phenotypes (`IND-PT-10007` [Hyper-prone], `IND-PT-10004` [Hypo-prone], `IND-PT-10001` [Controlled]).
- **Patient EHR Profile Card:** Displays age, BMI, WHR, baseline HbA1c, eGFR, lipid profile, and current medications.
- **Triage Alert Light:** Pulsing badges (Green = Stable, Amber = Hyperglycemia Alert, Red = Critical Nocturnal Hypoglycemia).
- **Dual Synchronized Charts:**
  - *Main Chart:* 6-hour observed CGM + 2-hour ahead predicted trajectory band + What-If simulated curve.
  - *Wearables Chart:* Heart rate, HRV RMSSD, 5-minute step cadence, and meal carb markers.
- **Interactive Simulation Drawer:** Real-time sliders for walking duration, carb reduction, and insulin titration with instant visual feedback.
- **Explainable AI (XAI) Drawer:** Breaks down physiological root causes triggering alerts.

---

## Submission Deliverables & Artifact Links

In accordance with Phase 1 guidelines, all required summit assets are compiled in this repository:

| Deliverable Required | Format | Location in Repository |
| :--- | :--- | :--- |
| **Complete Source Code** | Python, FastAPI, JS, HTML | [`web_app/`](web_app/), [`models/`](models/), [`data/`](data/) |
| **Architecture Diagram (PDF)** | Vector PDF | [presentation/ARCHITECTURE_DIAGRAM.pdf](presentation/ARCHITECTURE_DIAGRAM.pdf) |
| **Architecture Diagram (PPT/PPTX)** | Editable PowerPoint | [presentation/ARCHITECTURE_DIAGRAM.pptx](presentation/ARCHITECTURE_DIAGRAM.pptx) |
| **Architecture Diagram (SVG)** | High-Res Vector SVG | [presentation/ARCHITECTURE_DIAGRAM.svg](presentation/ARCHITECTURE_DIAGRAM.svg) |
| **Summit Presentation (PDF)** | 16:9 Presentation Slides PDF | [presentation/GLYCOTWIN_PRESENTATION.pdf](presentation/GLYCOTWIN_PRESENTATION.pdf) |
| **Summit Presentation (PPT/PPTX)** | Editable PowerPoint Slides | [presentation/GLYCOTWIN_PRESENTATION.pptx](presentation/GLYCOTWIN_PRESENTATION.pptx) |
| **Summit Presentation (Markdown)** | 20 Comprehensive Slides | [presentation/GLYCOTWIN_PRESENTATION.md](presentation/GLYCOTWIN_PRESENTATION.md) |
| **15-20 Min Video Demo Script** | Full Timestamped Teleprompter | [presentation/VIDEO_DEMO_SCRIPT.md](presentation/VIDEO_DEMO_SCRIPT.md) |
| **15-20 Min Video Demo Link** | Unlisted YouTube Video | **[Watch 15-20 Min Unlisted YouTube Demo](https://youtu.be/unlisted-glycotwin-poc-demo)** *(Replace with your unlisted YouTube link)* |
| **Open-Source License** | MIT Open-Source License | [LICENSE](LICENSE) |

---

## Quickstart: Installation & Running the Prototype

Follow these simple steps to run the complete data generation, model training, test suite, and interactive clinician dashboard:

### 1. Clone the Repository
```bash
git clone https://github.com/riyasojitra27-ux/GlycoTwin-AI.git
cd GlycoTwin-AI
```

### 2. Set Up Virtual Environment & Dependencies
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# Or install directly:
pip install pandas numpy scikit-learn fastapi uvicorn pydantic matplotlib
```

### 3. Generate Synthetic EHR & Wearable Telemetry
```bash
python data/generate_synthetic_data.py
```
*Generates 1,000 synthetic Indian EHR patients and 60,120 high-frequency wearable CGM timepoints.*

### 4. Train the Multimodal Digital Twin Models
```bash
python models/train_digital_twin.py
```
*Trains the 2-Hour Ahead Regressor (MARD: 7.15%) and Adverse Event Classifier, saving serialized artifacts to `models/saved_models/`.*

### 5. Run Integration Test Suite
```bash
python -m unittest tests/test_pipeline.py
```

### 6. Launch the Interactive Clinician Dashboard
```bash
python -m uvicorn web_app.app:app --host 127.0.0.1 --port 8000
```
Open your browser at **`http://127.0.0.1:8000/`** to interact with the live Digital Twin Cockpit!

---

## Repository File Structure

```
GlycoTwin_India/
├── README.md                           # Master summit documentation and project report
├── LICENSE                             # MIT Open-Source License
├── requirements.txt                    # Python dependency manifest
├── data/
│   ├── generate_synthetic_data.py      # DPDP/HIPAA compliant synthetic EHR & CGM generator
│   ├── ehr_patients.csv                # 1,000 synthetic Indian diabetic patient records
│   └── wearable_cgm_telemetry.csv      # 60,120 high-res time-series points (CGM, HR, HRV, Steps)
├── models/
│   ├── train_digital_twin.py           # Feature engineering & multimodal model training
│   ├── digital_twin_engine.py          # Core inference & What-If simulation engine
│   └── saved_models/
│       ├── glucose_regressor.joblib    # Trained 2-hour trajectory forecasting model
│       ├── adverse_classifier.joblib   # Trained adverse event triage model
│       └── model_metadata.json         # Clinical metrics, MARD, RMSE, and feature metadata
├── web_app/
│   ├── app.py                          # FastAPI server providing REST APIs & dashboard views
│   ├── templates/
│   │   └── dashboard.html              # Glassmorphic Clinician Cockpit UI (Chart.js & Tailwind)
│   └── static/                         # Assets and stylesheet dependencies
├── presentation/
│   ├── ARCHITECTURE_DIAGRAM.pdf        # Architecture diagram in PDF format (Summit Requirement)
│   ├── ARCHITECTURE_DIAGRAM.svg        # Scalable vector architecture diagram
│   ├── GLYCOTWIN_PRESENTATION.pdf      # Presentation slide deck in PDF format (Summit Requirement)
│   ├── GLYCOTWIN_PRESENTATION.md       # 20-slide presentation deck with comprehensive notes
│   ├── VIDEO_DEMO_SCRIPT.md            # 20-minute video demo script & anticipated jury Q&A
│   ├── generate_deck_pdf.py            # Automated presentation PDF generator
│   └── generate_arch_pdf.py            # Automated architecture PDF generator
└── tests/
    └── test_pipeline.py                # Unit & integration test suite
```

---

## Open Source License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.  
Open for academic, clinical, and open-source innovation at the **Happiest Health Reimagining & Reforming Healthcare in India Summit 2026, Bengaluru**.
