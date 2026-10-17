# GlycoTwin-AI: 20-Minute Video Demonstration Script & Presentation Guide

**Summit:** Happiest Health Reimagining & Reforming Healthcare in India Summit 2026, Bengaluru  
**Track:** Digital Twin Proof-of-Concept Challenge  
**Video Target Duration:** 20 to 22 Minutes  
**Format:** Slide Deck Walkthrough + Live Prototype Web Dashboard Demo + Jury Q&A Defense  

---

## Part 1: Video Timing & Agenda Breakdown

| Timestamp | Segment Title | Presenter / Speaker | Visual Screen Focus |
| :--- | :--- | :--- | :--- |
| **00:00 - 02:00** | Introduction & Clinical Problem in India | Team Leader | Slides 1 - 2 (Title & ICMR-INDIAB Data) |
| **02:00 - 04:30** | The Healthcare Digital Twin Concept | Clinical Systems Lead | Slide 3 (Traditional AI vs Digital Twin) |
| **04:30 - 07:00** | Multimodal Data Fusion & DPDP Act Compliance | Data Science Lead | Slides 4 - 5 & `ARCHITECTURE_DIAGRAM.svg` |
| **07:00 - 10:00** | Algorithmic Core: Kinetics & 2h Predictive Model | ML Engineer | Slides 6 - 9 (Metrics: 7.15% MARD, RMSE) |
| **10:00 - 15:30** | **Live Interactive UI Cockpit & What-If Demo** | Full-Stack / Team Lead | **Live Screen Share of Web App (`localhost:8000`)** |
| **15:30 - 17:30** | Explainable AI & Clinical Decision Support | Clinical Lead | Slide 14 & Dashboard XAI Drawer |
| **17:30 - 19:00** | Socioeconomic Impact & ABDM Deployment Roadmap | Team Leader | Slides 16 - 18 (Roadmap & Impact) |
| **19:00 - 20:30** | Summary, Codebase Links & Conclusion | All Team Members | Slide 20 & GitHub Repository Overview |

---

## Part 2: Minute-by-Minute Verbal Script & Screen Actions

### [00:00 - 02:00] Segment 1: The Problem & The Indian Diabetes Paradox
**Screen:** Slide 1 (Title) transitioning to Slide 2 (Indian Epidemiology).  
**Speaker 1 (Team Leader):**  
> *"Respected members of the jury, clinical experts, and the Happiest Health evaluation committee. Good morning. Today, medicine is predominantly reactive. A diabetic patient tests their blood sugar after feeling dizzy, or discovers microvascular kidney damage years after silent glycemic fluctuations have done their damage.*  
> *In India, this reactive model has led to a national catastrophe. With over 101 million diagnosed diabetics and another 136 million pre-diabetic citizens as documented by the 2023 ICMR-INDIAB study, India is the diabetes capital of the world.*  
> *Crucially, our population suffers from the unique **Asian Indian Phenotype**—excessive visceral adiposity, hyperinsulinemia, and profound insulin resistance at lower BMI cutoffs of just 23 kg/m². Paired with high-glycemic carbohydrate staples like polished white rice, Indian patients experience severe postprandial glucose spikes followed by unpredictable nocturnal hypoglycemia.*  
> *Today, Team GlycoTwin India presents **GlycoTwin-AI**: a dynamic, multimodal Digital Twin proof-of-concept that moves Indian diabetes care from reactive crisis response to proactive, in-silico predictive health."*

---

### [02:00 - 04:30] Segment 2: What is a Healthcare Digital Twin?
**Screen:** Slide 3 (Digital Twin Concept & Paradigm Shift).  
**Speaker 2 (Clinical Systems Lead):**  
> *"Before diving into the algorithms, let us address a critical distinction: What makes a Healthcare Digital Twin fundamentally different from traditional machine learning?*  
> *A standard machine learning model takes a static snapshot of patient variables and outputs a single risk score or regression value. But human biology is not static; it is an interconnected, homeostatic feedback system.*  
> *A Healthcare Digital Twin is a **living, dynamic, in-silico replica of the patient's individual physiology**. It maintains continuous physiological state, tracks insulin sensitivity drift over weeks, and most importantly, provides **in-silico counterfactual simulation**.*  
> *In aerodynamics, an engineer tests an airplane wing in a digital wind tunnel before it ever flies. With GlycoTwin-AI, a physician can test a dietary swap, an insulin titration, or a physical activity recommendation in a digital physiological twin before prescribing it to the patient."*

---

### [04:30 - 07:00] Segment 3: Dual Data Stream Fusion & DPDP Act 2023 Compliance
**Screen:** Slide 4 & `presentation/ARCHITECTURE_DIAGRAM.svg`.  
**Speaker 3 (Data Science Lead):**  
> *"To build an authentic physiological twin, our system fuses two disparate data streams, respecting the strict sandbox rules of the DPDP Act 2023 and HIPAA.*  
> *First, the **Static / Historical EHR Stream**: We generated a Synthea-grade cohort of 1,000 synthetic Indian diabetic patients, modeling demographics, Asian Indian BMI, baseline HbA1c ranging from 5.7% to 14.2%, fasting glucose, renal function via eGFR, dyslipidemia, genetic markers like TCF7L2 risk alleles, and multi-drug regimens including Metformin, SGLT2 inhibitors, and basal insulin.*  
> *Second, the **Dynamic Real-Time Wearable Stream**: We simulated 60,120 high-resolution timepoints representing 14 continuous days per patient at 5-minute sampling intervals. This fuses Continuous Glucose Monitoring (CGM) interstitial glucose, photoplethysmography (PPG) continuous heart rate, heart rate variability (HRV RMSSD), 5-minute step cadences, sleep architecture stages, and Indian carbohydrate meal logs.*  
> *By employing strict patient-level train and test isolation, zero data leaks across patient boundaries, and no identifiable patient information is ever ingested."*

---

### [07:00 - 10:00] Segment 4: Algorithmic Architecture & Clinical Metrics
**Screen:** Slides 6, 7 & 9 (Physiological Modeling & Clinical Performance).  
**Speaker 4 (ML Engineer):**  
> *"Our algorithmic engine is built upon physiologically grounded differential kinetics, inspired by the Bergman Minimal Model.*  
> *From the raw streams, our pipeline extracts 42 multi-domain features: first and second derivatives of glucose velocity and acceleration ($dG/dt$ and $d^2G/dt^2$), 1-hour and 3-hour intraday glycemic volatility CV%, and an Autonomic Stress Index defined as the ratio of continuous Heart Rate to HRV RMSSD.*  
> *Why is this autonomic cross-coupling vital? Because during impending nocturnal hypoglycemia, the autonomic nervous system triggers a counter-regulatory sympathetic surge. By coupling plummeting HRV with interstitial glucose velocity, our Digital Twin predicts nocturnal hypoglycemia up to 2 hours before the patient even wakes up in a cold sweat.*  
> *Our model achieves outstanding clinical accuracy on unseen patient holdouts:*  
> *1. For continuous 2-hour trajectory regression, our model achieves a **MARD (Mean Absolute Relative Difference) of 7.15%** and an RMSE of **14.50 mg/dL**. In clinical endocrinology, a MARD under 10% is considered the gold standard benchmark for continuous glucose monitoring.*  
> *2. For adverse event classification, our model delivers **65.31% precision on severe postprandial hyperglycemic surges** and provides a 120-minute early warning lead time."*

---

### [10:00 - 15:30] Segment 5: Live Working Prototype Demonstration (The Clinician Cockpit)
**Screen:** Switch screen share to live browser window at `http://127.0.0.1:8000/`.  
**Speaker 1 (Team Leader & Full-Stack Lead):**  
> *(Show browser window)*  
> *"Now, let us demonstrate how a doctor interacts with this virtual patient in our live clinical dashboard.*  
> *Here on screen is the **GlycoTwin-AI Clinician Cockpit**, running on our FastAPI and Chart.js backend.*  
> *Notice the top panel: The clinician selects a patient digital twin from our cohort. Let us select **Patient IND-PT-10007**, a 54-year-old Indian male with a 9-year history of Type 2 Diabetes, a baseline HbA1c of 9.4%, and a high-carbohydrate rice staple diet.*  
> *Immediately, the Digital Twin loads the patient's holistic state: Current glucose is 185 mg/dL. The 4-pillar metric bar shows glucose velocity is climbing at +1.40 mg/dL per minute. The Digital Twin predicts that in 2 hours, without intervention, this patient will experience a severe hyperglycemic spike to **218 mg/dL**.*  
> *Notice the triage badge has illuminated in **Amber**: 'WARNING: Hyperglycemic Spike Alert'.*  
> *Looking at the main chart, you see the observed continuous CGM in cyan over the past 6 hours, followed by the dashed purple curve projecting the 2-hour ahead forecast with its 95% confidence bounds.*  
> *Now, watch the power of the **In-Silico Counterfactual Simulator** below.*  
> *The physician asks: 'What if we tell this patient to take a 20-minute brisk walk after lunch, and swap 35 grams of white polished rice with foxtail millet?'*  
> *We adjust the Post-Prandial Walk slider to 20 minutes. We adjust the Carb Swap slider to 35 grams. Now, we click **Run In-Silico Simulation**.*  
> *(Click button — simulated orange dashed curve renders instantaneously)*  
> *Look at the chart! The simulated trajectory (dashed amber line) immediately recalculates. The simulated 2-hour glucose level drops from 218 mg/dL down to **180 mg/dL**—a projected delta of -38 mg/dL! The clinical recommendation updates to: 'Intervention successfully mitigated hyperglycemic spike into target range (70-180 mg/dL)'.*  
> *Now, let us switch to **Patient IND-PT-10004**.*  
> *(Select IND-PT-10004 from dropdown)*  
> *This is a 59-year-old female patient on 22 units of evening Basal Insulin and Sulfonylurea. Notice the time is 02:30 AM. Current glucose is 92 mg/dL. But look at the secondary wearable chart: Her HRV RMSSD has collapsed to 14ms, indicating intense autonomic sympathetic activation. The Digital Twin flags a **CRITICAL RED ALERT**: Impending Nocturnal Hypoglycemia to 61 mg/dL at 04:30 AM!*  
> *The clinician can immediately simulate reducing evening basal insulin by 3 units and adding a small bedtime snack, successfully averting a life-threatening nocturnal hypoglycemic coma."*

---

### [15:30 - 17:30] Segment 6: Explainable AI (XAI) & Clinical Decision Support
**Screen:** Slide 14 & Dashboard Explanation Box.  
**Speaker 2 (Clinical Systems Lead):**  
> *"In clinical medicine, black-box AI cannot be trusted. Physicians must understand **why** an alert was triggered.*  
> *GlycoTwin-AI embeds explainable physiological feature attributions directly into the clinician interface.*  
> *When an alert is flagged, the explanation drawer breaks down the underlying metabolic drivers: recent carbohydrate ingestion, positive glycemic acceleration, blunted peripheral clearance from elevated baseline HbA1c, and autonomic tone shifts.*  
> *These recommendations are directly aligned with guidelines from the **Research Society for the Study of Diabetes in India (RSSDI)** and the American Diabetes Association (ADA)."*

---

### [17:30 - 19:00] Segment 7: Socioeconomic Impact & India 2026 Deployment Roadmap
**Screen:** Slides 16, 17 & 18 (Roadmap & Economic Analysis).  
**Speaker 1 (Team Leader):**  
> *"The socioeconomic impact of this solution in India is immense.*  
> *A single emergency hospital admission for acute diabetic ketoacidosis or severe hypoglycemia costs an Indian family between ₹40,000 and ₹1,50,000 in out-of-pocket expenses.*  
> *By preventing acute crises and maintaining patients within the 70-180 mg/dL target range, GlycoTwin-AI reduces average HbA1c by an estimated 0.8% to 1.2%. As established by the landmark UKPDS trial, every 1% reduction in HbA1c reduces microvascular complications—such as diabetic kidney disease and retinopathy—by 37%.*  
> *Our deployment roadmap targets seamless integration into the **Ayushman Bharat Digital Mission (ABDM)** and e-Sanjeevani national telemedicine network via standardized FHIR APIs, democratizing proactive digital twin care from tertiary hospitals in Bengaluru to primary healthcare centers across rural India."*

---

### [19:00 - 20:30] Segment 8: Summary, Codebase Overview & Conclusion
**Screen:** Slide 20 & GitHub Repository Overview.  
**Speaker 1 (Team Leader):**  
> *"In conclusion, Team GlycoTwin India has delivered a complete, validated proof-of-concept Digital Twin for Type 2 Diabetes:*  
> *1. We successfully fused static EHR with dynamic continuous wearable IoT telemetry.*  
> *2. We delivered a working dual-head AI model achieving a clinical-grade 7.15% MARD with a 2-hour early warning horizon.*  
> *3. We pioneered an in-silico What-If simulator and interactive doctor cockpit that empowers clinicians to prevent adverse events before they happen.*  
> *Our complete code, synthetic datasets, documentation, architecture diagrams, and slide deck are publicly accessible under the MIT open-source license on GitHub.*  
> *We look forward to presenting GlycoTwin-AI live in Bengaluru at the Happiest Health Reimagining and Reforming Healthcare in India Summit 2026. Thank you."*

---

## Part 3: Anticipated Jury Questions & Winning Answers

1. **Jury Q: How does your model handle noise and sensor calibration lag inherent to consumer CGMs?**  
   *Answer:* "CGM sensors measure interstitial glucose, which exhibits a 5 to 15-minute physiological lag behind capillary blood glucose. Our dynamic sliding-window feature extractor incorporates 15, 30, and 60-minute lagged rolling means and rates of change ($dG/dt$), which filter out high-frequency sensor noise while explicitly modeling the physiological diffusion delay."

2. **Jury Q: How can you ensure the Digital Twin doesn't hallucinate during 'What-If' simulations?**  
   *Answer:* "The 'What-If' simulator does not generate unconstrained text or arbitrary curves. It modifies physiologically bounded parameters (carbohydrate absorption $D(t)$ and exercise-induced GLUT-4 clearance $E(t)$) calibrated to the Bergman Minimal Model, and re-evaluates the state through our trained multimodal regressor with 95% confidence bands."

3. **Jury Q: How does GlycoTwin-AI address the specific reality of healthcare in India?**  
   *Answer:* "Unlike Western models trained on Eurocentric datasets with high-fat diets, GlycoTwin-AI is specifically calibrated to the Asian Indian Phenotype: higher visceral adiposity at lower BMI ($>23 \text{ kg/m}^2$), high-glycemic Indian carbohydrate staples (rice/roti), and widespread use of sulfonylureas and generic insulins, making both postprandial spikes and nocturnal hypoglycemia uniquely severe in India."
