"""
GlycoTwin-AI: Synthetic Data Generator for Indian Diabetic Patient Cohort
Compliant with DPDP Act 2023 & HIPAA Sandbox Requirements.
Simulates:
1. Static/Historical EHR: Demographics, Lab Biomarkers, Indian Phenotype Risk, Comorbidities, Medications.
2. Dynamic/Wearable IoT Telemetry: CGM (5-min intervals), Heart Rate, HRV (RMSSD), Steps, Sleep Stages, Meals & Medications.
"""

import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def generate_ehr_cohort(n_patients=1000, random_seed=42):
    np.random.seed(random_seed)
    patient_ids = [f"IND-PT-{10000 + i}" for i in range(n_patients)]
    
    # Demographics representative of Indian Diabetic Population (ICMR-INDIAB epidemiology)
    ages = np.random.normal(52, 11, n_patients).clip(28, 82).astype(int)
    genders = np.random.choice(["Male", "Female"], size=n_patients, p=[0.54, 0.46])
    
    # Asian Indian Phenotype: High visceral adiposity at lower BMI
    # Indian BMI cutoff for overweight is >= 23 kg/m², obesity >= 25 kg/m²
    bmis = np.random.normal(26.4, 3.8, n_patients).clip(18.5, 38.5).round(1)
    waist_hip_ratio = np.random.normal(0.93, 0.06, n_patients).clip(0.78, 1.15).round(2)
    
    # Duration of Diabetes (years)
    t2d_duration_years = np.random.exponential(6.5, n_patients).clip(0.5, 30.0).round(1)
    
    # Baseline Laboratory Biomarkers
    # Indian diabetic mean HbA1c typically sits between 7.5% - 9.8% in clinical cohorts
    hba1c = np.random.normal(8.4, 1.4, n_patients).clip(5.7, 14.2).round(1)
    fasting_glucose = (hba1c * 18.5 + np.random.normal(20, 15, n_patients)).clip(85, 320).round(1)
    
    # Renal function (eGFR in mL/min/1.73m²) & Microalbuminuria
    egfr = np.random.normal(82, 18, n_patients).clip(25, 120).round(1)
    creatinine = (110 / egfr + np.random.normal(0, 0.1, n_patients)).clip(0.6, 3.8).round(2)
    
    # Lipid Profile (Indian dyslipidemia: high triglycerides, low HDL)
    triglycerides = np.random.normal(195, 65, n_patients).clip(80, 520).round(1)
    hdl = np.random.normal(38, 7, n_patients).clip(22, 65).round(1)
    ldl = np.random.normal(118, 30, n_patients).clip(55, 210).round(1)
    
    # Comorbidities & Risk Markers
    hypertension = np.random.binomial(1, p=np.clip(0.40 + (ages - 40)*0.008, 0.2, 0.8), size=n_patients)
    diabetic_retinopathy = np.random.binomial(1, p=np.clip(t2d_duration_years * 0.025 + (hba1c - 7)*0.04, 0.05, 0.65), size=n_patients)
    diabetic_neuropathy = np.random.binomial(1, p=np.clip(t2d_duration_years * 0.03 + (hba1c - 7)*0.03, 0.05, 0.60), size=n_patients)
    cvd_history = np.random.binomial(1, p=np.clip(0.12 + (ages - 45)*0.005 + hypertension*0.1, 0.05, 0.45), size=n_patients)
    
    # Genetic/Epigenetic markers prevalent in South Asian T2DM (TCF7L2, KCNQ1 risk alleles)
    tcf7l2_risk_allele = np.random.choice([0, 1, 2], size=n_patients, p=[0.35, 0.48, 0.17])
    
    # Current Pharmacotherapy
    med_regimen = []
    daily_metformin_mg = []
    daily_sglt2i_mg = []
    daily_dpp4i_mg = []
    daily_sulfonylurea_mg = []
    insulin_user = []
    basal_insulin_units = []
    
    for i in range(n_patients):
        hb = hba1c[i]
        dur = t2d_duration_years[i]
        
        # Indian clinical practice algorithm (RSSDI / ICMR guidelines)
        met = 1000 if hb < 8.0 else (1500 if hb < 9.5 else 2000)
        daily_metformin_mg.append(met)
        
        # Second-line: SGLT2i (Empagliflozin/Dapagliflozin) or DPP-4i (Teneligliptin/Sitagliptin)
        sglt2 = 10 if (hb > 7.5 and egfr[i] > 45 and np.random.rand() > 0.4) else 0
        dpp4 = 20 if (hb > 7.8 and np.random.rand() > 0.35) else 0
        su = 2 if (hb > 8.5 and np.random.rand() > 0.5) else 0 # Glimepiride
        
        # Basal Insulin for decompensated glycemic control
        ins = 1 if (hb >= 9.0 or (dur > 10 and np.random.rand() > 0.5)) else 0
        ins_units = int(np.random.normal(18, 6)) if ins else 0
        
        daily_sglt2i_mg.append(sglt2)
        daily_dpp4i_mg.append(dpp4)
        daily_sulfonylurea_mg.append(su)
        insulin_user.append(ins)
        basal_insulin_units.append(max(0, ins_units))
        
        reg_names = ["Metformin"]
        if sglt2 > 0: reg_names.append("SGLT2i")
        if dpp4 > 0: reg_names.append("DPP4i")
        if su > 0: reg_names.append("Sulfonylurea")
        if ins > 0: reg_names.append(f"Basal Insulin ({ins_units}U)")
        med_regimen.append(" + ".join(reg_names))
        
    ehr_df = pd.DataFrame({
        "patient_id": patient_ids,
        "age": ages,
        "gender": genders,
        "bmi": bmis,
        "waist_hip_ratio": waist_hip_ratio,
        "diabetes_duration_years": t2d_duration_years,
        "hba1c_pct": hba1c,
        "fasting_glucose_mg_dl": fasting_glucose,
        "egfr_ml_min": egfr,
        "serum_creatinine_mg_dl": creatinine,
        "triglycerides_mg_dl": triglycerides,
        "hdl_mg_dl": hdl,
        "ldl_mg_dl": ldl,
        "hypertension": hypertension,
        "diabetic_retinopathy": diabetic_retinopathy,
        "diabetic_neuropathy": diabetic_neuropathy,
        "cvd_history": cvd_history,
        "tcf7l2_risk_allele_count": tcf7l2_risk_allele,
        "daily_metformin_mg": daily_metformin_mg,
        "daily_sglt2i_mg": daily_sglt2i_mg,
        "daily_dpp4i_mg": daily_dpp4i_mg,
        "daily_sulfonylurea_mg": daily_sulfonylurea_mg,
        "insulin_user": insulin_user,
        "basal_insulin_units": basal_insulin_units,
        "medication_regimen": med_regimen,
        "dietary_pattern": np.random.choice(["High-Carb Rice Staple (South/East)", "Wheat/Roti Staple (North/West)", "Mixed Urban Balanced"], size=n_patients, p=[0.45, 0.40, 0.15])
    })
    
    return ehr_df

def generate_telemetry_stream(ehr_df, num_patients=20, days_per_patient=14, random_seed=42):
    """
    Simulates high-resolution dynamic telemetry (5-min intervals = 288 points/day)
    Fuses CGM interstitial glucose, HR, HRV (RMSSD), steps, sleep states, Indian meals.
    """
    np.random.seed(random_seed)
    telemetry_records = []
    
    selected_patients = ehr_df.head(num_patients).to_dict(orient="records")
    start_date = datetime(2026, 10, 1, 0, 0, 0)
    total_steps = days_per_patient * 288
    
    for pt in selected_patients:
        pid = pt["patient_id"]
        base_hba1c = pt["hba1c_pct"]
        base_glucose = pt["fasting_glucose_mg_dl"]
        is_insulin = pt["insulin_user"]
        is_su = pt["daily_sulfonylurea_mg"] > 0
        diet_type = pt["dietary_pattern"]
        
        # Baseline insulin sensitivity factor (lower with higher HbA1c / BMI)
        insulin_sensitivity = np.clip(1.0 - (pt["bmi"] - 22)*0.02 - (base_hba1c - 6.5)*0.05, 0.35, 1.1)
        
        current_glucose = base_glucose
        current_hr = 72.0
        current_hrv = 42.0
        
        for step in range(total_steps):
            timestamp = start_date + timedelta(minutes=step * 5)
            hour = timestamp.hour + timestamp.minute / 60.0
            
            # Circadian Sleep / Awake Cycle
            is_sleep = 1 if (hour >= 23.0 or hour < 6.5) else 0
            sleep_stage = "Awake"
            if is_sleep:
                if hour >= 23.5 and hour < 2.5:
                    sleep_stage = "Deep"
                elif hour >= 2.5 and hour < 4.5:
                    sleep_stage = "Light"
                else:
                    sleep_stage = "REM"
            
            # Indian Meal Timing & Carbohydrate load
            # Breakfast: 8:00 - 9:00 (Idli/Dosa/Paratha ~ 50-70g carbs)
            # Lunch: 13:00 - 14:00 (Rice/Roti + Dal/Curry ~ 70-110g carbs)
            # Evening Chai/Snack: 17:00 - 17:30 (Samosa/Biscuits ~ 25-45g carbs)
            # Dinner: 20:30 - 21:30 (Heavy Indian Dinner ~ 80-120g carbs)
            meal_carbs = 0.0
            meal_type = "None"
            
            if timestamp.minute == 0:
                if timestamp.hour == 8:
                    meal_carbs = np.random.normal(60, 10)
                    meal_type = "Breakfast"
                elif timestamp.hour == 13:
                    meal_carbs = np.random.normal(85, 15) if "Rice" in diet_type else np.random.normal(70, 12)
                    meal_type = "Lunch"
                elif timestamp.hour == 17:
                    meal_carbs = np.random.normal(30, 8) if np.random.rand() > 0.4 else 0.0
                    meal_type = "Evening Snack" if meal_carbs > 0 else "None"
                elif timestamp.hour == 21:
                    meal_carbs = np.random.normal(90, 18)
                    meal_type = "Dinner"
            
            # Physical Activity: Steps per 5-min window
            if is_sleep:
                steps = np.random.poisson(2)
            else:
                # Post-meal walk or work commute
                if (hour >= 9.5 and hour < 10.5) or (hour >= 18.0 and hour < 19.5):
                    steps = np.random.poisson(180) # Commute / brisk movement
                elif (hour >= 14.0 and hour < 14.5 and np.random.rand() > 0.6):
                    steps = np.random.poisson(120) # Post-lunch walk
                else:
                    steps = np.random.poisson(25) # Sedentary
            
            # Physiological Simulation Dynamics (Bergman minimal model inspired)
            # Glucose drift towards baseline
            drift = (base_glucose - current_glucose) * 0.015
            
            # Meal absorption (steeper and delayed for Indian high-glycemic carbs)
            meal_impact = (meal_carbs * 1.85 * (1.0 / insulin_sensitivity)) * 0.12
            
            # Exercise effect: Muscular glucose uptake lowers blood sugar
            exercise_impact = -(steps / 100.0) * 1.8 * insulin_sensitivity
            
            # Nocturnal Hypoglycemia Trigger:
            # Sulfonylurea / evening basal insulin combined with missed dinner snack causes 2 AM - 4 AM crash
            hypo_driver = 0.0
            if is_sleep and (is_insulin or is_su) and (hour >= 1.5 and hour <= 4.5):
                if np.random.rand() < 0.08: # Occasional acute nocturnal plunge
                    hypo_driver = -np.random.uniform(14.0, 28.0)
            
            # Autonomic Nervous System Telemetry (HR & HRV)
            # Sympathetic surge occurs prior to and during hypoglycemia or acute stress
            noise_glucose = np.random.normal(0, 1.8)
            current_glucose = float(np.clip(current_glucose + drift + meal_impact + exercise_impact + hypo_driver + noise_glucose, 45.0, 380.0))
            
            # Heart rate dynamics
            base_hr = 62.0 if is_sleep else 76.0
            if steps > 100:
                target_hr = base_hr + (steps / 100.0) * 22.0
            elif current_glucose < 75.0: # Adrenergic counter-regulatory response to hypoglycemia
                target_hr = base_hr + 24.0 # Tachycardia
            elif current_glucose > 220.0:
                target_hr = base_hr + 8.0
            else:
                target_hr = base_hr
                
            current_hr = float(0.85 * current_hr + 0.15 * target_hr + np.random.normal(0, 1.2))
            
            # HRV (RMSSD in ms): Parasympathetic tone. Plummets during nocturnal hypoglycemia, rises in deep sleep
            if current_glucose < 75.0:
                target_hrv = 16.0 # Severe sympathetic dominance / stress
            elif is_sleep and sleep_stage == "Deep":
                target_hrv = 55.0
            else:
                target_hrv = 36.0
            current_hrv = float(0.88 * current_hrv + 0.12 * target_hrv + np.random.normal(0, 1.5))
            
            telemetry_records.append({
                "patient_id": pid,
                "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "cgm_glucose_mg_dl": round(current_glucose, 1),
                "heart_rate_bpm": round(current_hr, 1),
                "hrv_rmssd_ms": round(max(8.0, current_hrv), 1),
                "steps_5min": int(steps),
                "is_sleep": is_sleep,
                "sleep_stage": sleep_stage,
                "meal_carbs_g": round(meal_carbs, 1),
                "meal_type": meal_type,
                "hour_of_day": round(hour, 2)
            })
            
    df_telem = pd.DataFrame(telemetry_records)
    
    # Calculate 2-hour ahead Target (24 steps of 5 mins = 120 mins)
    df_telem["target_glucose_2h"] = df_telem.groupby("patient_id")["cgm_glucose_mg_dl"].shift(-24)
    
    # Adverse Event Labeling:
    # 0 = Normal / Controlled
    # 1 = Severe Postprandial Hyperglycemia Spike (> 200 mg/dL)
    # 2 = Impending Hypoglycemia (< 70 mg/dL)
    def label_adverse_event(val):
        if pd.isna(val):
            return np.nan
        if val < 70.0:
            return 2 # Hypoglycemia
        elif val > 200.0:
            return 1 # Hyperglycemia Spike
        return 0 # In-Range
        
    df_telem["adverse_event_2h"] = df_telem["target_glucose_2h"].apply(label_adverse_event)
    
    # Drop lookahead NaN rows for model training validity
    df_telem_clean = df_telem.dropna(subset=["target_glucose_2h", "adverse_event_2h"]).copy()
    df_telem_clean["adverse_event_2h"] = df_telem_clean["adverse_event_2h"].astype(int)
    
    return df_telem_clean

if __name__ == "__main__":
    print("[1/2] Generating Synthea-grade Indian EHR Patient Cohort...")
    ehr = generate_ehr_cohort(n_patients=1000, random_seed=42)
    os.makedirs("data", exist_ok=True)
    ehr.to_csv("data/ehr_patients.csv", index=False)
    print(f"  ✓ Saved 1,000 synthetic patient records to data/ehr_patients.csv")
    
    print("[2/2] Generating High-Resolution Wearable & CGM Telemetry Streams...")
    # Generate 15 patients x 14 days of 5-min resolution data (~60,000 timepoints)
    telemetry = generate_telemetry_stream(ehr, num_patients=15, days_per_patient=14, random_seed=42)
    telemetry.to_csv("data/wearable_cgm_telemetry.csv", index=False)
    print(f"  ✓ Saved {len(telemetry)} telemetry records to data/wearable_cgm_telemetry.csv")
    print(f"  ✓ Distribution of 2-Hour Adverse Events:")
    print(telemetry["adverse_event_2h"].value_counts(normalize=True).round(3))
