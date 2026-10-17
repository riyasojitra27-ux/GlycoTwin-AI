"""
Generate PDF version of Architecture Diagram using matplotlib
"""

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

def generate_arch_pdf(output_pdf="presentation/ARCHITECTURE_DIAGRAM.pdf"):
    fig = plt.figure(figsize=(14, 8), dpi=200)
    ax = fig.add_subplot(111)
    ax.set_facecolor('#0b1120')
    fig.patch.set_facecolor('#0b1120')
    
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
        
    # Title
    ax.text(0.04, 0.93, "GlycoTwin-AI: End-to-End Multimodal Digital Twin Architecture", fontsize=16, fontweight='bold', color='#f8fafc', family='sans-serif', transform=ax.transAxes)
    ax.text(0.04, 0.88, "Happiest Health Reimagining & Reforming Healthcare Summit 2026 • Proactive Diabetes Management in India", fontsize=10.5, color='#94a3b8', family='sans-serif', transform=ax.transAxes)
    
    # 4 Columns / Pillars
    pillars = [
        {
            "x": 0.04, "w": 0.21,
            "title": "1. DUAL DATA STREAMS", "subtitle": "DPDP Act 2023 & HIPAA Sandbox",
            "accent": "#38bdf8",
            "items": [
                "Static Historical EHR:",
                "• 1,000 Synthea Indian Profiles",
                "• Asian Indian BMI (>=23 kg/m²)",
                "• Baseline HbA1c (5.7 - 14.2%)",
                "• Fasting Blood Glucose (FBG)",
                "• eGFR & Serum Creatinine",
                "• Triglycerides / HDL Profile",
                "• Comorbidities & TCF7L2 allele",
                "• Baseline Pharmacotherapy",
                "",
                "Dynamic IoT Telemetry:",
                "• 60,120 Timepoints (5-min)",
                "• Interstitial Glucose (CGM)",
                "• Continuous Heart Rate (PPG)",
                "• HRV (RMSSD Autonomic tone)",
                "• Step Cadence & Sleep Stages",
                "• Indian Meal Carbs & Insulins"
            ]
        },
        {
            "x": 0.28, "w": 0.21,
            "title": "2. MULTIMODAL FUSION", "subtitle": "Cross-Domain Feature Synthesis",
            "accent": "#a855f7",
            "items": [
                "Temporal Dynamic Kinetics:",
                "• Glucose Velocity dG/dt (15/30m)",
                "• Glycemic Acceleration d²G/dt²",
                "• Rolling Mean & Std (1h / 3h)",
                "• Intraday CV% Volatility",
                "",
                "Autonomic Coupling:",
                "• Autonomic Stress: HR / HRV",
                "• Pre-hypo Sympathetic Surge",
                "• 1-Hour Step Accumulation",
                "• 2-Hour Carbohydrate Load",
                "",
                "Latent Patient Embedding:",
                "• Asian Indian Metabolic Profile",
                "• Trigonometric Circadian Wave",
                "• Beta-Cell Reserve Proxy",
                "★ 42 Multimodal Features"
            ]
        },
        {
            "x": 0.52, "w": 0.21,
            "title": "3. DUAL-HEAD AI CORE", "subtitle": "Prediction & In-Silico Engine",
            "accent": "#34d399",
            "items": [
                "Head 1: 2h Glucose Forecaster",
                "• HistGBM Multi-Tree Regressor",
                "• 2-Hour Horizon (+120 mins)",
                "★ MARD: 7.15% (Gold Std <10%)",
                "★ RMSE: 14.50 mg/dL",
                "• Dynamic 95% Confidence Band",
                "",
                "Head 2: Adverse Classifier",
                "• Severe Postprandial Hyper (>200)",
                "  Precision = 65.31%",
                "• Nocturnal Hypoglycemia (<70)",
                "  Early Warning: 120 mins",
                "",
                "In-Silico What-If Simulator",
                "• Post-Meal Walk (0-45 mins)",
                "• Carb Swap (-10 to -60g)",
                "• Basal Titration (-4U to +4U)"
            ]
        },
        {
            "x": 0.76, "w": 0.20,
            "title": "4. CLINICIAN COCKPIT", "subtitle": "Interactive Doctor Dashboard",
            "accent": "#fbbf24",
            "items": [
                "Clinical Web Interface:",
                "• Virtual Patient Selector",
                "• Static EHR Profile Cards",
                "• 6h Multi-stream Waveforms",
                "• 2h Forward Projection Band",
                "• Dynamic Triage Risk Light",
                "",
                "Physician Interactivity:",
                "• Real-time What-If Sliders",
                "• Dynamic Delta Metric Output",
                "• In-Silico Trajectory Overlay",
                "• RSSDI & ADA Decision Support",
                "",
                "Explainable AI (XAI):",
                "• Physiological Root-Cause XAI",
                "• Autonomic Crash Alerts",
                "★ FastAPI + Chart.js Web App"
            ]
        }
    ]
    
    for p in pillars:
        # Background card
        box = FancyBboxPatch((p["x"], 0.10), p["w"], 0.74, boxstyle="round,pad=0.015", facecolor='#1e293b', edgecolor=p["accent"], linewidth=1.5, transform=ax.transAxes)
        ax.add_patch(box)
        
        # Header bar
        header_bar = FancyBboxPatch((p["x"], 0.825), p["w"], 0.015, boxstyle="round,pad=0.005", facecolor=p["accent"], edgecolor=p["accent"], transform=ax.transAxes)
        ax.add_patch(header_bar)
        
        ax.text(p["x"] + 0.015, 0.795, p["title"], fontsize=11, fontweight='bold', color=p["accent"], family='sans-serif', transform=ax.transAxes)
        ax.text(p["x"] + 0.015, 0.77, p["subtitle"], fontsize=8.5, color='#94a3b8', family='sans-serif', transform=ax.transAxes)
        
        # Divider
        ax.plot([p["x"] + 0.015, p["x"] + p["w"] - 0.015], [0.75, 0.75], color='#334155', linewidth=1, transform=ax.transAxes)
        
        y_text = 0.72
        for line in p["items"]:
            if line.startswith("★"):
                ax.text(p["x"] + 0.015, y_text, line, fontsize=8.8, fontweight='bold', color='#6ee7b7', family='sans-serif', transform=ax.transAxes)
            elif line.startswith("Head") or line.startswith("Static") or line.startswith("Dynamic") or line.startswith("Temporal") or line.startswith("Autonomic") or line.startswith("Latent") or line.startswith("In-Silico") or line.startswith("Clinical") or line.startswith("Physician") or line.startswith("Explainable"):
                ax.text(p["x"] + 0.015, y_text, line, fontsize=9.2, fontweight='bold', color='#f1f5f9', family='sans-serif', transform=ax.transAxes)
            else:
                ax.text(p["x"] + 0.015, y_text, line, fontsize=8.2, color='#cbd5e1', family='sans-serif', transform=ax.transAxes)
            y_text -= 0.033
            
    # Connecting Arrows
    for arrow_x in [0.255, 0.495, 0.735]:
        ax.annotate('', xy=(arrow_x + 0.02, 0.48), xytext=(arrow_x - 0.005, 0.48),
                    xycoords='axes fraction', textcoords='axes fraction',
                    arrowprops=dict(arrowstyle="->", color="#38bdf8", lw=2.5))
                    
    # Regulatory Footer
    foot = FancyBboxPatch((0.04, 0.03), 0.92, 0.05, boxstyle="round,pad=0.01", facecolor='#0f172a', edgecolor='#334155', linewidth=1, transform=ax.transAxes)
    ax.add_patch(foot)
    ax.text(0.06, 0.045, "DPDP ACT 2023 & HIPAA COMPLIANT: 100% Synthetic & De-identified Data • Zero Real Patient PII • In-Silico Testing Validated", fontsize=8.5, color='#94a3b8', family='sans-serif', transform=ax.transAxes)
    
    plt.tight_layout()
    plt.savefig(output_pdf, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close(fig)
    print(f"✓ Saved Architecture Diagram PDF: {output_pdf}")

if __name__ == "__main__":
    generate_arch_pdf()
