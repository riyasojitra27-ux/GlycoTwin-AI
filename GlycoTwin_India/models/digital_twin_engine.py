"""
GlycoTwin-AI: Core Digital Twin Inference & What-If Simulation Engine
Provides:
1. Multi-modal state evaluation (EHR + CGM + Wearables)
2. 2-Hour Ahead Predictive Trajectory & Adverse Event Risk
3. Counterfactual In-Silico "What-If" Simulation for Clinicians
"""

import os
import json
import joblib
import numpy as np
import pandas as pd

class GlycoTwinEngine:
    def __init__(self, models_dir="models/saved_models"):
        self.models_dir = models_dir
        self.regressor = joblib.load(os.path.join(models_dir, "glucose_regressor.joblib"))
        self.classifier = joblib.load(os.path.join(models_dir, "adverse_classifier.joblib"))
        with open(os.path.join(models_dir, "model_metadata.json"), "r") as f:
            self.metadata = json.load(f)
        self.features = self.metadata["features"]

    def construct_feature_vector(self, ehr_dict, telemetry_window):
        """
        telemetry_window: DataFrame of the last 12-24 steps (1-2 hours) of 5-min readings
        Must contain: cgm_glucose_mg_dl, heart_rate_bpm, hrv_rmssd_ms, steps_5min, meal_carbs_g, is_sleep, hour_of_day
        """
        curr = telemetry_window.iloc[-1]
        
        # Lags
        lag_15m = telemetry_window.iloc[-4]["cgm_glucose_mg_dl"] if len(telemetry_window) >= 4 else curr["cgm_glucose_mg_dl"]
        lag_30m = telemetry_window.iloc[-7]["cgm_glucose_mg_dl"] if len(telemetry_window) >= 7 else lag_15m
        lag_60m = telemetry_window.iloc[-13]["cgm_glucose_mg_dl"] if len(telemetry_window) >= 13 else lag_30m
        
        roc_15m = (curr["cgm_glucose_mg_dl"] - lag_15m) / 15.0
        roc_30m = (curr["cgm_glucose_mg_dl"] - lag_30m) / 30.0
        
        prev_roc = (telemetry_window.iloc[-4]["cgm_glucose_mg_dl"] - telemetry_window.iloc[-7]["cgm_glucose_mg_dl"]) / 15.0 if len(telemetry_window) >= 7 else roc_15m
        accel = roc_15m - prev_roc
        
        roll_mean_1h = telemetry_window["cgm_glucose_mg_dl"].tail(12).mean()
        roll_std_1h = telemetry_window["cgm_glucose_mg_dl"].tail(12).std()
        if pd.isna(roll_std_1h): roll_std_1h = 0.0
        cv_1h = roll_std_1h / (roll_mean_1h + 1e-5)
        
        autonomic_stress = curr["heart_rate_bpm"] / (curr["hrv_rmssd_ms"] + 1e-4)
        hr_lag_30m = telemetry_window.iloc[-7]["heart_rate_bpm"] if len(telemetry_window) >= 7 else curr["heart_rate_bpm"]
        delta_hr_30m = curr["heart_rate_bpm"] - hr_lag_30m
        
        steps_1h = telemetry_window["steps_5min"].tail(12).sum()
        carbs_2h = telemetry_window["meal_carbs_g"].tail(24).sum()
        
        circ_sin = np.sin(2 * np.pi * curr["hour_of_day"] / 24.0)
        circ_cos = np.cos(2 * np.pi * curr["hour_of_day"] / 24.0)
        
        feature_dict = {
            "cgm_glucose_mg_dl": curr["cgm_glucose_mg_dl"],
            "glucose_lag_15m": lag_15m,
            "glucose_lag_30m": lag_30m,
            "glucose_lag_60m": lag_60m,
            "glucose_roc_15m": roc_15m,
            "glucose_roc_30m": roc_30m,
            "glucose_accel": accel,
            "glucose_roll_mean_1h": roll_mean_1h,
            "glucose_roll_std_1h": roll_std_1h,
            "glucose_cv_1h": cv_1h,
            "heart_rate_bpm": curr["heart_rate_bpm"],
            "hrv_rmssd_ms": curr["hrv_rmssd_ms"],
            "autonomic_stress_index": autonomic_stress,
            "delta_hr_30m": delta_hr_30m,
            "steps_5min": curr["steps_5min"],
            "steps_roll_1h": steps_1h,
            "carbs_roll_2h": carbs_2h,
            "is_sleep": curr["is_sleep"],
            "circadian_sin": circ_sin,
            "circadian_cos": circ_cos,
            
            # Static EHR
            "age": ehr_dict["age"],
            "bmi": ehr_dict["bmi"],
            "waist_hip_ratio": ehr_dict["waist_hip_ratio"],
            "diabetes_duration_years": ehr_dict["diabetes_duration_years"],
            "hba1c_pct": ehr_dict["hba1c_pct"],
            "fasting_glucose_mg_dl": ehr_dict["fasting_glucose_mg_dl"],
            "egfr_ml_min": ehr_dict["egfr_ml_min"],
            "serum_creatinine_mg_dl": ehr_dict["serum_creatinine_mg_dl"],
            "triglycerides_mg_dl": ehr_dict["triglycerides_mg_dl"],
            "hdl_mg_dl": ehr_dict["hdl_mg_dl"],
            "ldl_mg_dl": ehr_dict["ldl_mg_dl"],
            "hypertension": ehr_dict["hypertension"],
            "diabetic_retinopathy": ehr_dict["diabetic_retinopathy"],
            "diabetic_neuropathy": ehr_dict["diabetic_neuropathy"],
            "cvd_history": ehr_dict["cvd_history"],
            "tcf7l2_risk_allele_count": ehr_dict["tcf7l2_risk_allele_count"],
            "daily_metformin_mg": ehr_dict["daily_metformin_mg"],
            "daily_sglt2i_mg": ehr_dict["daily_sglt2i_mg"],
            "daily_dpp4i_mg": ehr_dict["daily_dpp4i_mg"],
            "daily_sulfonylurea_mg": ehr_dict["daily_sulfonylurea_mg"],
            "insulin_user": ehr_dict["insulin_user"],
            "basal_insulin_units": ehr_dict["basal_insulin_units"]
        }
        
        vec = pd.DataFrame([feature_dict])[self.features]
        return vec

    def evaluate_twin_status(self, ehr_dict, telemetry_window):
        X = self.construct_feature_vector(ehr_dict, telemetry_window)
        pred_glucose_2h = float(self.regressor.predict(X)[0])
        pred_probs = self.classifier.predict_proba(X)[0]
        
        # Clinical risk calibrated decision rule
        if len(pred_probs) > 2 and pred_probs[2] >= 0.18:
            pred_event_class = 2 # Impending Nocturnal Hypoglycemia
        else:
            pred_event_class = int(np.argmax(pred_probs))
        
        # Event labels
        event_names = ["In-Range / Stable", "Impending Hyperglycemia Spike (>200 mg/dL)", "Impending Nocturnal Hypoglycemia (<70 mg/dL)"]
        risk_level = "LOW" if pred_event_class == 0 else ("HIGH" if pred_event_class == 1 else "CRITICAL")
        
        # Clinical Explainability
        explanations = []
        curr_g = float(X["cgm_glucose_mg_dl"].iloc[0])
        roc = float(X["glucose_roc_15m"].iloc[0])
        carbs = float(X["carbs_roll_2h"].iloc[0])
        hrv = float(X["hrv_rmssd_ms"].iloc[0])
        hba1c = float(ehr_dict["hba1c_pct"])
        
        if carbs > 60:
            explanations.append(f"Significant recent carbohydrate ingestion ({carbs:.0f}g) driving rapid postprandial absorption.")
        if roc > 1.2:
            explanations.append(f"Steep positive glycemic velocity (+{roc:.2f} mg/dL/min) indicates insufficient early-phase insulin response.")
        if hrv < 22 and curr_g < 95:
            explanations.append(f"Autonomic sympathetic hyperactivity (HRV RMSSD {hrv:.1f}ms) flagged preceding nocturnal glycemic crash.")
        if hba1c > 8.5:
            explanations.append(f"High baseline HbA1c ({hba1c:.1f}%) impairs beta-cell clearance rate.")
        if not explanations:
            explanations.append("Glycemic homeostasis maintained within target physiological boundaries.")
            
        return {
            "predicted_glucose_2h": round(pred_glucose_2h, 1),
            "predicted_event_code": pred_event_class,
            "predicted_event_name": event_names[pred_event_class],
            "risk_level": risk_level,
            "probabilities": {
                "in_range": round(float(pred_probs[0]), 3),
                "hyper_spike": round(float(pred_probs[1]), 3) if len(pred_probs) > 1 else 0.0,
                "hypoglycemia": round(float(pred_probs[2]), 3) if len(pred_probs) > 2 else 0.0
            },
            "clinical_explanations": explanations
        }

    def simulate_what_if(self, ehr_dict, telemetry_window, walk_minutes=0, carb_reduction_grams=0, insulin_adjustment_units=0):
        """
        In-silico counterfactual simulation:
        Allows physicians to simulate behavioral and medical adjustments:
        - walk_minutes: 0 - 45 mins post-prandial walk
        - carb_reduction_grams: 0 - 60 grams carbohydrate substitution (e.g., swapping white rice for millets)
        - insulin_adjustment_units: -6 to +6 units adjustment
        """
        # Baseline projection
        base_status = self.evaluate_twin_status(ehr_dict, telemetry_window)
        
        # Copy telemetry & EHR for simulation
        sim_telem = telemetry_window.copy()
        sim_ehr = ehr_dict.copy()
        
        # Apply simulated interventions
        # 1. Post-prandial walk increases steps
        added_steps = int(walk_minutes * 95) # ~95 steps/min brisk walk
        sim_telem.loc[sim_telem.index[-1], "steps_5min"] += int(added_steps / 4) # recent burst
        
        # 2. Carb reduction mitigates recent meal carbs
        sim_telem["meal_carbs_g"] = (sim_telem["meal_carbs_g"] - (carb_reduction_grams / 24.0)).clip(lower=0.0)
        
        # 3. Medication adjustment
        sim_ehr["basal_insulin_units"] = max(0, sim_ehr["basal_insulin_units"] + insulin_adjustment_units)
        
        # Re-evaluate simulated state
        sim_status = self.evaluate_twin_status(sim_ehr, sim_telem)
        
        delta_glucose = sim_status["predicted_glucose_2h"] - base_status["predicted_glucose_2h"]
        
        return {
            "baseline": base_status,
            "simulated": sim_status,
            "delta_glucose_mg_dl": round(delta_glucose, 1),
            "intervention_summary": f"Walk: +{walk_minutes} mins | Carb Swap: -{carb_reduction_grams}g | Insulin: {insulin_adjustment_units:+d}U",
            "clinical_recommendation": (
                "Intervention successfully mitigated hyperglycemic spike into target range (70-180 mg/dL)."
                if base_status["predicted_event_code"] == 1 and sim_status["predicted_event_code"] == 0
                else (
                    "Intervention successfully prevented impending nocturnal hypoglycemia."
                    if base_status["predicted_event_code"] == 2 and sim_status["predicted_event_code"] == 0
                    else "Intervention modulated glycemic trajectory as projected."
                )
            )
        }
