"""
GlycoTwin-AI: Clinician Digital Twin Interactive Web Cockpit
FastAPI Server providing real-time REST endpoints and an interactive physician UI dashboard.
"""

import os
import json
import numpy as np
import pandas as pd
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from models.digital_twin_engine import GlycoTwinEngine

app = FastAPI(title="GlycoTwin-AI Clinician Dashboard", version="1.0.0")

# Load models and synthetic databases
engine = GlycoTwinEngine(models_dir="models/saved_models")
ehr_df = pd.read_csv("data/ehr_patients.csv")
telem_df = pd.read_csv("data/wearable_cgm_telemetry.csv")

class SimulationRequest(BaseModel):
    patient_id: str
    walk_minutes: int = 0
    carb_reduction_grams: int = 0
    insulin_adjustment_units: int = 0

@app.get("/", response_class=HTMLResponse)
async def get_dashboard():
    with open("web_app/templates/dashboard.html", "r", encoding="utf-8") as f:
        html = f.read()
    
    patient_ids = list(telem_df["patient_id"].unique())
    options = []
    for pid in patient_ids:
        if pid == 'IND-PT-10007':
            desc = "High Postprandial Spikes (Rice Staple)"
        elif pid == 'IND-PT-10004':
            desc = "Nocturnal Hypoglycemia Prone (Insulin)"
        elif pid == 'IND-PT-10001':
            desc = "Controlled Baseline (Metformin)"
        else:
            desc = "Type 2 Diabetes Cohort"
        sel = "selected" if pid == 'IND-PT-10007' else ""
        options.append(f'<option value="{pid}" {sel}>{pid} - {desc}</option>')
        
    html = html.replace("{{ PATIENT_OPTIONS }}", "\n".join(options))
    return HTMLResponse(content=html)

@app.get("/api/patient/{patient_id}")
async def get_patient_data(patient_id: str):
    pt_ehr = ehr_df[ehr_df["patient_id"] == patient_id]
    if pt_ehr.empty:
        return JSONResponse({"error": "Patient not found"}, status_code=404)
    
    ehr_dict = pt_ehr.iloc[0].to_dict()
    pt_telem = telem_df[telem_df["patient_id"] == patient_id].tail(72).copy() # Last 6 hours (72 x 5-min intervals)
    
    # Evaluate Twin Status
    twin_status = engine.evaluate_twin_status(ehr_dict, pt_telem)
    
    # Prepare time-series for frontend chart
    timestamps = pt_telem["timestamp"].tolist()
    cgm_values = pt_telem["cgm_glucose_mg_dl"].tolist()
    hr_values = pt_telem["heart_rate_bpm"].tolist()
    hrv_values = pt_telem["hrv_rmssd_ms"].tolist()
    step_values = pt_telem["steps_5min"].tolist()
    meal_carbs = pt_telem["meal_carbs_g"].tolist()
    
    # Build 2-hour forecast points (24 steps of 5 mins)
    last_val = cgm_values[-1]
    pred_val = twin_status["predicted_glucose_2h"]
    # Smooth linear interpolation towards 2h predicted point
    forecast_curve = list(np.linspace(last_val, pred_val, 25)[1:].round(1))
    
    # Upper and lower confidence bounds (95% CI based on model RMSE ~14.5 mg/dL)
    upper_bounds = [round(v + 14.5 * 1.96 * (i/24.0)**0.5, 1) for i, v in enumerate(forecast_curve, 1)]
    lower_bounds = [round(max(40.0, v - 14.5 * 1.96 * (i/24.0)**0.5), 1) for i, v in enumerate(forecast_curve, 1)]
    
    return {
        "ehr": ehr_dict,
        "twin_status": twin_status,
        "telemetry": {
            "timestamps": timestamps,
            "cgm_glucose": cgm_values,
            "heart_rate": hr_values,
            "hrv_rmssd": hrv_values,
            "steps": step_values,
            "meal_carbs": meal_carbs
        },
        "forecast": {
            "points": forecast_curve,
            "upper_bound": upper_bounds,
            "lower_bound": lower_bounds,
            "horizon_minutes": 120
        }
    }

@app.post("/api/simulate")
async def simulate_counterfactual(req: SimulationRequest):
    pt_ehr = ehr_df[ehr_df["patient_id"] == req.patient_id]
    if pt_ehr.empty:
        return JSONResponse({"error": "Patient not found"}, status_code=404)
        
    ehr_dict = pt_ehr.iloc[0].to_dict()
    pt_telem = telem_df[telem_df["patient_id"] == req.patient_id].tail(72).copy()
    
    sim_result = engine.simulate_what_if(
        ehr_dict, 
        pt_telem, 
        walk_minutes=req.walk_minutes, 
        carb_reduction_grams=req.carb_reduction_grams, 
        insulin_adjustment_units=req.insulin_adjustment_units
    )
    
    last_val = pt_telem["cgm_glucose_mg_dl"].iloc[-1]
    sim_pred = sim_result["simulated"]["predicted_glucose_2h"]
    sim_curve = list(np.linspace(last_val, sim_pred, 25)[1:].round(1))
    
    sim_result["simulated_forecast_curve"] = sim_curve
    return sim_result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
