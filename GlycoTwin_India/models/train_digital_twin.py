"""
GlycoTwin-AI: Multimodal Digital Twin Fusion & Predictive Training Pipeline
Fuses Static EHR with High-Resolution Wearable/CGM Telemetry to predict:
1. 2-Hour Ahead Glucose Trajectory (Regression, evaluated by clinical MARD & RMSE)
2. Impending Adverse Events (Classification: Severe Postprandial Spike >200 mg/dL, Nocturnal Hypo <70 mg/dL)
"""

import os
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import HistGradientBoostingRegressor, HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.metrics import mean_squared_error, mean_absolute_error, classification_report, f1_score, roc_auc_score, confusion_matrix
from sklearn.preprocessing import StandardScaler

def extract_multimodal_features(ehr_path="data/ehr_patients.csv", telemetry_path="data/wearable_cgm_telemetry.csv"):
    print("[1/5] Loading EHR and Wearable Telemetry streams...")
    ehr_df = pd.read_csv(ehr_path)
    telem_df = pd.read_csv(telemetry_path)
    telem_df["timestamp"] = pd.to_datetime(telem_df["timestamp"])
    
    # Sort for time-series feature engineering
    telem_df = telem_df.sort_values(by=["patient_id", "timestamp"]).reset_index(drop=True)
    
    print("[2/5] Engineering Temporal Dynamic & Inter-Stream Cross Features...")
    grouped = telem_df.groupby("patient_id")
    
    # Rolling glucose dynamics
    telem_df["glucose_lag_15m"] = grouped["cgm_glucose_mg_dl"].shift(3)  # 3 * 5min
    telem_df["glucose_lag_30m"] = grouped["cgm_glucose_mg_dl"].shift(6)
    telem_df["glucose_lag_60m"] = grouped["cgm_glucose_mg_dl"].shift(12)
    
    # Rates of change (First and Second derivatives)
    telem_df["glucose_roc_15m"] = (telem_df["cgm_glucose_mg_dl"] - telem_df["glucose_lag_15m"]) / 15.0
    telem_df["glucose_roc_30m"] = (telem_df["cgm_glucose_mg_dl"] - telem_df["glucose_lag_30m"]) / 30.0
    telem_df["glucose_accel"] = telem_df["glucose_roc_15m"] - grouped["glucose_roc_15m"].shift(3)
    
    # Rolling Statistics over past 1 hour (12 steps) and 3 hours (36 steps)
    telem_df["glucose_roll_mean_1h"] = grouped["cgm_glucose_mg_dl"].transform(lambda x: x.rolling(12, min_periods=3).mean())
    telem_df["glucose_roll_std_1h"] = grouped["cgm_glucose_mg_dl"].transform(lambda x: x.rolling(12, min_periods=3).std().fillna(0))
    telem_df["glucose_cv_1h"] = telem_df["glucose_roll_std_1h"] / (telem_df["glucose_roll_mean_1h"] + 1e-5)
    
    # Autonomic Stress Marker (HR vs HRV cross-coupling)
    telem_df["autonomic_stress_index"] = telem_df["heart_rate_bpm"] / (telem_df["hrv_rmssd_ms"] + 1e-4)
    telem_df["hr_lag_30m"] = grouped["heart_rate_bpm"].shift(6)
    telem_df["delta_hr_30m"] = telem_df["heart_rate_bpm"] - telem_df["hr_lag_30m"]
    
    # Cumulative Activity & Meal Carbs in past 1 hour
    telem_df["steps_roll_1h"] = grouped["steps_5min"].transform(lambda x: x.rolling(12, min_periods=1).sum())
    telem_df["carbs_roll_2h"] = grouped["meal_carbs_g"].transform(lambda x: x.rolling(24, min_periods=1).sum())
    
    # Circadian periodicity
    telem_df["circadian_sin"] = np.sin(2 * np.pi * telem_df["hour_of_day"] / 24.0)
    telem_df["circadian_cos"] = np.cos(2 * np.pi * telem_df["hour_of_day"] / 24.0)
    
    telem_df["meal_type"] = telem_df["meal_type"].fillna("None")
    
    print("[3/5] Fusing Static EHR Biomarkers with Dynamic Telemetry...")
    # Merge static EHR
    fused_df = pd.merge(telem_df, ehr_df, on="patient_id", how="inner")
    
    # Drop rows with NaN strictly from rolling/shift initialization
    feature_cols = [
        "cgm_glucose_mg_dl", "glucose_lag_15m", "glucose_lag_30m", "glucose_lag_60m",
        "glucose_roc_15m", "glucose_roc_30m", "glucose_accel",
        "glucose_roll_mean_1h", "glucose_roll_std_1h", "glucose_cv_1h",
        "heart_rate_bpm", "hrv_rmssd_ms", "autonomic_stress_index", "delta_hr_30m",
        "steps_5min", "steps_roll_1h", "carbs_roll_2h", "is_sleep",
        "circadian_sin", "circadian_cos", "target_glucose_2h", "adverse_event_2h"
    ]
    clean_fused = fused_df.dropna(subset=feature_cols).reset_index(drop=True)
    print(f"  ✓ Total fused multi-modal records ready: {len(clean_fused)}")
    return clean_fused

def train_and_evaluate_models(fused_df):
    dynamic_features = [
        "cgm_glucose_mg_dl", "glucose_lag_15m", "glucose_lag_30m", "glucose_lag_60m",
        "glucose_roc_15m", "glucose_roc_30m", "glucose_accel",
        "glucose_roll_mean_1h", "glucose_roll_std_1h", "glucose_cv_1h",
        "heart_rate_bpm", "hrv_rmssd_ms", "autonomic_stress_index", "delta_hr_30m",
        "steps_5min", "steps_roll_1h", "carbs_roll_2h", "is_sleep",
        "circadian_sin", "circadian_cos"
    ]
    
    static_features = [
        "age", "bmi", "waist_hip_ratio", "diabetes_duration_years",
        "hba1c_pct", "fasting_glucose_mg_dl", "egfr_ml_min", "serum_creatinine_mg_dl",
        "triglycerides_mg_dl", "hdl_mg_dl", "ldl_mg_dl",
        "hypertension", "diabetic_retinopathy", "diabetic_neuropathy", "cvd_history",
        "tcf7l2_risk_allele_count", "daily_metformin_mg", "daily_sglt2i_mg",
        "daily_dpp4i_mg", "daily_sulfonylurea_mg", "insulin_user", "basal_insulin_units"
    ]
    
    all_features = dynamic_features + static_features
    X = fused_df[all_features]
    y_reg = fused_df["target_glucose_2h"]
    y_clf = fused_df["adverse_event_2h"]
    
    # Ensure test set contains all adverse event phenotypes (controlled, hyper, and nocturnal hypo)
    patient_ids = list(fused_df["patient_id"].unique())
    # Selected test cohort with balanced clinical phenotypes:
    # IND-PT-10004 (nocturnal hypo prone), IND-PT-10007 (hyperglycemia spike prone),
    # IND-PT-10001 (controlled baseline), IND-PT-10012 (moderate dysglycemic)
    test_pts = ["IND-PT-10004", "IND-PT-10007", "IND-PT-10001", "IND-PT-10012"]
    train_pts = [p for p in patient_ids if p not in test_pts]
    
    train_mask = fused_df["patient_id"].isin(train_pts)
    test_mask = fused_df["patient_id"].isin(test_pts)
    
    X_train, X_test = X[train_mask], X[test_mask]
    y_reg_train, y_reg_test = y_reg[train_mask], y_reg[test_mask]
    y_clf_train, y_clf_test = y_clf[train_mask], y_clf[test_mask]
    
    print(f"  ✓ Train size: {len(X_train)} samples across {len(train_pts)} patients")
    print(f"  ✓ Test size:  {len(X_test)} samples across {len(test_pts)} patients")
    
    print("\n[4/5] Training 2-Hour Ahead Glucose Trajectory Regressor...")
    regressor = HistGradientBoostingRegressor(
        max_iter=150,
        learning_rate=0.08,
        max_depth=8,
        min_samples_leaf=20,
        l2_regularization=1.5,
        random_state=42
    )
    regressor.fit(X_train, y_reg_train)
    y_reg_pred = regressor.predict(X_test)
    
    # Clinical Metrics
    rmse = np.sqrt(mean_squared_error(y_reg_test, y_reg_pred))
    mae = mean_absolute_error(y_reg_test, y_reg_pred)
    # MARD: Mean Absolute Relative Difference (%)
    mard = np.mean(np.abs((y_reg_test - y_reg_pred) / y_reg_test)) * 100.0
    
    print(f"  ★ Regressor Performance:")
    print(f"    - RMSE: {rmse:.2f} mg/dL")
    print(f"    - MAE:  {mae:.2f} mg/dL")
    print(f"    - MARD: {mard:.2f}% (Industry standard benchmark < 10% for high clinical accuracy)")
    
    print("\n[5/5] Training Adverse Event Early Warning Classifier...")
    # Compute clinical risk class weights: Hypoglycemia is life-critical, so we apply a 4x sensitivity multiplier
    classes = np.unique(y_clf_train)
    class_weights = {c: len(y_clf_train) / (len(classes) * np.sum(y_clf_train == c)) for c in classes}
    if 2 in class_weights:
        class_weights[2] *= 4.0 # High sensitivity to nocturnal hypoglycemia
    sample_weights_train = y_clf_train.map(class_weights)
    
    classifier = HistGradientBoostingClassifier(
        max_iter=150,
        learning_rate=0.07,
        max_depth=8,
        min_samples_leaf=15,
        l2_regularization=1.0,
        random_state=42
    )
    classifier.fit(X_train, y_clf_train, sample_weight=sample_weights_train)
    y_clf_proba = classifier.predict_proba(X_test)
    
    # Clinical decision rule: If hypoglycemia probability > 0.18, prioritize patient safety
    y_clf_pred = np.argmax(y_clf_proba, axis=1)
    if y_clf_proba.shape[1] > 2:
        hypo_alert_mask = y_clf_proba[:, 2] >= 0.18
        y_clf_pred[hypo_alert_mask] = 2
    
    macro_f1 = f1_score(y_clf_test, y_clf_pred, average="macro", zero_division=0)
    target_names = ["Controlled (0)", "Hyper Spike >200 (1)", "Hypoglycemia <70 (2)"]
    present_labels = sorted(list(set(y_clf_test).union(set(y_clf_pred))))
    active_target_names = [target_names[i] for i in present_labels]
    
    clf_report = classification_report(
        y_clf_test, 
        y_clf_pred, 
        labels=present_labels, 
        target_names=active_target_names, 
        output_dict=True,
        zero_division=0
    )
    
    print(f"  ★ Classifier Macro F1: {macro_f1:.4f}")
    if "Hypoglycemia <70 (2)" in clf_report:
        print(f"  ★ Hypoglycemia Recall: {clf_report['Hypoglycemia <70 (2)']['recall']:.2%}")
    if "Hyper Spike >200 (1)" in clf_report:
        print(f"  ★ Hyperglycemia Precision: {clf_report['Hyper Spike >200 (1)']['precision']:.2%}")
    
    # Save artifacts
    os.makedirs("models/saved_models", exist_ok=True)
    joblib.dump(regressor, "models/saved_models/glucose_regressor.joblib")
    joblib.dump(classifier, "models/saved_models/adverse_classifier.joblib")
    
    metadata = {
        "model_version": "1.0.0",
        "target_condition": "Type 2 Diabetes Mellitus (Asian Indian Cohort)",
        "prediction_horizon_minutes": 120,
        "features": all_features,
        "dynamic_features": dynamic_features,
        "static_features": static_features,
        "metrics": {
            "rmse_mg_dl": round(float(rmse), 2),
            "mae_mg_dl": round(float(mae), 2),
            "mard_pct": round(float(mard), 2),
            "macro_f1": round(float(macro_f1), 4),
            "hypo_recall": round(float(clf_report.get('Hypoglycemia <70 (2)', {}).get('recall', 0.0)), 4),
            "hyper_precision": round(float(clf_report.get('Hyper Spike >200 (1)', {}).get('precision', 0.0)), 4)
        }
    }
    with open("models/saved_models/model_metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)
        
    print("\n✓ Models and metadata successfully saved to models/saved_models/")
    return metadata

if __name__ == "__main__":
    fused_df = extract_multimodal_features()
    meta = train_and_evaluate_models(fused_df)
