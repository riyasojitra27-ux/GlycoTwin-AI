"""
GlycoTwin-AI: Executive Styled PowerPoint Presentation Generator
Matches the exact visual layout, card design, badge headers, color palette,
and typography of previous top-tier hackathon decks.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_styled_deck(output_path="presentation/GLYCOTWIN_PRESENTATION.pptx"):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]
    
    # Premium Executive Slate & Cyan/Gold Color Palette
    BG_DARK = RGBColor(11, 19, 43)        # #0B132B Deep Slate Navy
    CARD_BG = RGBColor(28, 37, 65)        # #1C2541 Slate Card
    CARD_BORDER = RGBColor(58, 80, 107)    # #3A506B Soft Slate Border
    TEXT_MAIN = RGBColor(255, 255, 255)   # Pure White
    TEXT_MUTED = RGBColor(141, 153, 174) # #8D99AE Muted Silver
    ACCENT_CYAN = RGBColor(72, 202, 228)  # #48CAE4 Bright Cyan
    ACCENT_GOLD = RGBColor(255, 209, 102) # #FFD166 Highlight Gold
    ACCENT_GREEN = RGBColor(6, 214, 160)  # #06D6A0 Success Emerald
    ACCENT_RED = RGBColor(239, 68, 68)    # #EF4444 Alert Red

    def add_background(slide, color=BG_DARK):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = color
        bg.line.fill.background()
        return bg

    def add_header(slide, badge_text, title_text, slide_num=None):
        # Category Badge
        badge_w = max(3.4, len(badge_text) * 0.12)
        badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.4), Inches(badge_w), Inches(0.36))
        badge.fill.solid()
        badge.fill.fore_color.rgb = CARD_BORDER
        badge.line.fill.background()
        tf_b = badge.text_frame
        tf_b.word_wrap = False
        p_b = tf_b.paragraphs[0]
        p_b.text = badge_text.upper()
        p_b.font.name = "Arial"
        p_b.font.size = Pt(10.5)
        p_b.font.bold = True
        p_b.font.color.rgb = ACCENT_CYAN
        p_b.alignment = PP_ALIGN.CENTER

        # Slide Title
        tx_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.82), Inches(11.7), Inches(0.75))
        tf = tx_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.name = "Arial"
        p.font.size = Pt(23)
        p.font.bold = True
        p.font.color.rgb = TEXT_MAIN
        
        # Footer
        if slide_num:
            ft_box = slide.shapes.add_textbox(Inches(0.8), Inches(6.9), Inches(11.7), Inches(0.35))
            ftf = ft_box.text_frame
            ftf.word_wrap = True
            fp = ftf.paragraphs[0]
            fp.text = f"GlycoTwin-AI  |  Happiest Health Summit 2026, Bengaluru  |  Slide {slide_num} of 10"
            fp.font.name = "Arial"
            fp.font.size = Pt(10)
            fp.font.color.rgb = TEXT_MUTED

    def add_card(slide, left, top, width, height, title="", title_color=ACCENT_GOLD, bg_color=CARD_BG, border_color=CARD_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1.5)
        
        if title:
            tb = slide.shapes.add_textbox(Inches(left + 0.25), Inches(top + 0.18), Inches(width - 0.5), Inches(0.48))
            tf = tb.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            p.text = title
            p.font.name = "Arial"
            p.font.size = Pt(15.5)
            p.font.bold = True
            p.font.color.rgb = title_color
        return card

    def add_bullet_list(slide, left, top, width, height, items, default_color=TEXT_MAIN, accent_color=ACCENT_CYAN, font_size=12.5):
        tb = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
        tf = tb.text_frame
        tf.word_wrap = True
        for idx, (bold_prefix, rest_text) in enumerate(items):
            p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
            p.space_after = Pt(8)
            
            # Bullet point and bold title
            r1 = p.add_run()
            r1.text = "• " + bold_prefix + " "
            r1.font.name = "Arial"
            r1.font.bold = True
            r1.font.size = Pt(font_size)
            r1.font.color.rgb = accent_color
            
            # Rest of description
            r2 = p.add_run()
            r2.text = rest_text
            r2.font.name = "Arial"
            r2.font.size = Pt(font_size)
            r2.font.color.rgb = default_color

    # =========================================================================
    # SLIDE 1: Hero Title Slide
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    add_background(s1)
    add_card(s1, 0.9, 1.0, 11.533, 5.5, "", bg_color=CARD_BG, border_color=ACCENT_CYAN)

    tb1 = s1.shapes.add_textbox(Inches(1.4), Inches(1.4), Inches(10.5), Inches(4.7))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p0 = tf1.paragraphs[0]
    p0.text = "HAPPIEST HEALTH REIMAGINING & REFORMING HEALTHCARE IN INDIA SUMMIT 2026, BENGALURU"
    p0.font.name = "Arial"
    p0.font.size = Pt(13)
    p0.font.bold = True
    p0.font.color.rgb = ACCENT_CYAN
    p0.space_after = Pt(14)

    p1 = tf1.add_paragraph()
    p1.text = "GlycoTwin-AI"
    p1.font.name = "Arial"
    p1.font.size = Pt(38)
    p1.font.bold = True
    p1.font.color.rgb = TEXT_MAIN
    p1.space_after = Pt(8)

    p2 = tf1.add_paragraph()
    p2.text = "Multimodal Healthcare Digital Twin for Proactive Type 2 Diabetes Management in India"
    p2.font.name = "Arial"
    p2.font.size = Pt(18)
    p2.font.bold = True
    p2.font.color.rgb = ACCENT_GOLD
    p2.space_after = Pt(18)

    p3 = tf1.add_paragraph()
    p3.text = "A dynamic virtual physiological replica fusing static EHR with continuous wearable IoT telemetry (CGM + PPG) to predict acute dysglycemic adverse events 2 hours in advance and simulate personalized interventions in-silico."
    p3.font.name = "Arial"
    p3.font.size = Pt(13.5)
    p3.font.color.rgb = TEXT_MUTED
    p3.space_after = Pt(24)

    p4 = tf1.add_paragraph()
    p4.text = "Track: Digital Twin PoC Challenge  |  Team GlycoTwin India  |  Center for Healthcare AI & Innovation"
    p4.font.name = "Arial"
    p4.font.size = Pt(12)
    p4.font.bold = True
    p4.font.color.rgb = ACCENT_GREEN

    # =========================================================================
    # SLIDE 2: The Indian Diabetes Crisis & Reactive Care Failure
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_background(s2)
    add_header(s2, "Clinical Problem & Indian Epidemiology", "The Indian Diabetes Crisis: Why Reactive Care Fails", slide_num=2)

    add_card(s2, 0.8, 1.7, 5.65, 5.0, "The Asian Indian Phenotype Challenge", ACCENT_GOLD)
    add_bullet_list(s2, 1.05, 2.35, 5.15, 4.1, [
        ("101.3M Diagnosed Diabetics:", "ICMR-INDIAB 2023 study confirms India as the global epicentre of diabetes, with 136M additional pre-diabetics."),
        ("Asian Indian Phenotype:", "Excess visceral adiposity, hyperinsulinemia, and profound insulin resistance at lower BMI cutoffs (>= 23 kg/m²)."),
        ("Dietary Glycemic Volatility:", "Staple diets of refined white rice and wheat flour cause steep postprandial glucose surges (>200 mg/dL)."),
        ("Lethal Nocturnal Hypo:", "Sulfonylurea/insulin use and erratic meal times cause dangerous 02:00-04:30 AM crashes (<70 mg/dL) during sleep.")
    ], accent_color=ACCENT_CYAN, font_size=12)

    add_card(s2, 6.85, 1.7, 5.65, 5.0, "Why Traditional Reactive Medicine Fails", ACCENT_CYAN)
    add_bullet_list(s2, 7.1, 2.35, 5.15, 4.1, [
        ("Quarterly HbA1c Blindspot:", "HbA1c is a 3-month trailing average that completely masks intraday glycemic volatility and lethal nocturnal crashes."),
        ("Post-Hoc Intervention:", "Current standard of care alerts patients after hypoglycemia has occurred, leading to acute disorientation and ER visits."),
        ("Crippling Family Costs:", "Emergency admissions for DKA or severe hypoglycemia cost Indian families ₹40,000 to ₹1,50,000 out-of-pocket."),
        ("The Digital Twin Solution:", "Moving from reactive treatment to proactive in-silico simulation, predicting adverse excursions 2 hours ahead.")
    ], accent_color=ACCENT_GOLD, font_size=12)

    # =========================================================================
    # SLIDE 3: Dual Data Stream Fusion Architecture
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_background(s3)
    add_header(s3, "Data Architecture & Multimodal Fusion", "Dual Data Stream Fusion: Static EHR + Wearable IoT", slide_num=3)

    add_card(s3, 0.8, 1.7, 5.65, 5.0, "Stream 1: Static Historical EHR", ACCENT_CYAN)
    add_bullet_list(s3, 1.05, 2.35, 5.15, 4.1, [
        ("1,000 Synthea Indian Patients:", "Synthesized EHR database adhering to ICMR-INDIAB clinical distributions with complete demographic representation."),
        ("Phenotype & Biomarkers:", "Asian Indian BMI, Waist-to-Hip Ratio, baseline HbA1c (5.7% - 14.2%), and Fasting Blood Glucose (FBG)."),
        ("Renal & Lipid Panels:", "eGFR (mL/min/1.73m²), serum creatinine, triglycerides (high in Indians), HDL, and LDL cholesterol."),
        ("Genetics & Comorbidities:", "TCF7L2 risk alleles, diabetic retinopathy, neuropathy, CVD history, and baseline pharmacotherapy (Metformin, SGLT2i, Insulin).")
    ], accent_color=ACCENT_CYAN, font_size=12)

    add_card(s3, 6.85, 1.7, 5.65, 5.0, "Stream 2: Dynamic Wearables & IoT Telemetry", ACCENT_GOLD)
    add_bullet_list(s3, 7.1, 2.35, 5.15, 4.1, [
        ("60,120 Continuous Timepoints:", "14 continuous days per patient at high-frequency 5-minute intervals, modeling genuine physiological kinetics."),
        ("CGM Interstitial Glucose:", "Continuous glucose monitoring stream capturing interstitial diffusion dynamics and rapid glycemic slopes."),
        ("Wearable PPG Biosensors:", "Continuous Heart Rate (bpm) and Heart Rate Variability (HRV - RMSSD in ms) tracking autonomic nervous system tone."),
        ("Behavioral & Meal Logs:", "5-minute step cadence, sleep stages (Deep, Light, REM), Indian carbohydrate intake (g), and insulin injection timestamps.")
    ], accent_color=ACCENT_GOLD, font_size=12)

    # =========================================================================
    # SLIDE 4: 42 Multimodal Kinetic & Autonomic Features
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_background(s4)
    add_header(s4, "Feature Engineering & Kinetic Modeling", "42 Multimodal Kinetic, Autonomic & Metabolic Features", slide_num=4)

    add_card(s4, 0.8, 1.7, 3.65, 5.0, "Differential Kinetics", ACCENT_CYAN)
    add_bullet_list(s4, 1.0, 2.35, 3.25, 4.1, [
        ("Rate of Change (dG/dt):", "15-min and 30-min glucose velocity in mg/dL/min."),
        ("Acceleration (d²G/dt²):", "Second derivative detecting rapid inflection points."),
        ("Intraday Volatility:", "1-hour and 3-hour rolling mean, std, and CV% index.")
    ], accent_color=ACCENT_CYAN, font_size=11.5)

    add_card(s4, 4.8, 1.7, 3.65, 5.0, "Autonomic Stress Coupling", ACCENT_GOLD)
    add_bullet_list(s4, 5.0, 2.35, 3.25, 4.1, [
        ("Autonomic Stress Ratio:", "HR / HRV RMSSD captures sympathetic surge before crash."),
        ("Pre-Hypo Tachycardia:", "Delta HR detects autonomic adrenergic counter-regulation."),
        ("Activity Cadence:", "1-hour rolling step accumulation driving muscle GLUT-4 uptake.")
    ], accent_color=ACCENT_GOLD, font_size=11.5)

    add_card(s4, 8.8, 1.7, 3.65, 5.0, "Latent Patient Embedding", ACCENT_GREEN)
    add_bullet_list(s4, 9.0, 2.35, 3.25, 4.1, [
        ("Beta-Cell Reserve:", "Proxy derived from T2D duration, baseline HbA1c, and insulin use."),
        ("Circadian Wave:", "Sin/Cos trigonometric encoding of 24h diurnal cycles."),
        ("Carbohydrate Load:", "2-hour rolling carb load modeling high-GI Indian digestion.")
    ], accent_color=ACCENT_GREEN, font_size=11.5)

    # =========================================================================
    # SLIDE 5: Dual-Head Machine Learning Core & Clinical Metrics
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_background(s5)
    add_header(s5, "Model Architecture & Clinical Accuracy", "Dual-Head Predictive Engine & Clinical Benchmarking", slide_num=5)

    add_card(s5, 0.8, 1.7, 5.65, 5.0, "Head 1: 2-Hour Trajectory Regressor", ACCENT_GREEN)
    add_bullet_list(s5, 1.05, 2.35, 5.15, 4.1, [
        ("Clinical MARD: 7.15%:", "Achieves 7.15% Mean Absolute Relative Difference—well below the rigorous < 10% clinical gold standard benchmark."),
        ("Model RMSE: 14.50 mg/dL:", "Low root mean square error around continuous interstitial ground truth across 59,940 high-resolution samples."),
        ("Model MAE: 11.11 mg/dL:", "Demonstrates tight error bounds across extreme intraday glycemic excursions."),
        ("Dynamic 95% Confidence Band:", "Extrapolates upper and lower biological uncertainty envelopes over the 120-minute forward horizon.")
    ], accent_color=ACCENT_GREEN, font_size=12)

    add_card(s5, 6.85, 1.7, 5.65, 5.0, "Head 2: Adverse Event Early Warning Classifier", ACCENT_GOLD)
    add_bullet_list(s5, 7.1, 2.35, 5.15, 4.1, [
        ("120-Minute Early Warning:", "Flags adverse events 2 hours in advance, providing sufficient lead time for clinician or patient action."),
        ("Hyperglycemic Spikes (>200 mg/dL):", "Precision = 65.31% for severe postprandial surges driven by high-carb Indian meals."),
        ("Nocturnal Hypo Early Alert (<70 mg/dL):", "Clinical risk decision threshold (18% trigger) prioritizes patient safety against nocturnal mortality."),
        ("Patient-Level Isolation:", "Trained with strict stratified holdout split, guaranteeing zero data leakage across patient boundaries.")
    ], accent_color=ACCENT_GOLD, font_size=12)

    # =========================================================================
    # SLIDE 6: Physician "What-If" In-Silico Simulator
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_background(s6)
    add_header(s6, "In-Silico Counterfactual Engine", "Physician 'What-If' In-Silico Counterfactual Simulator", slide_num=6)

    add_card(s6, 0.8, 1.7, 3.65, 5.0, "1. Post-Meal Brisk Walk", ACCENT_CYAN)
    add_bullet_list(s6, 1.0, 2.35, 3.25, 4.1, [
        ("Range: 0 to 45 mins:", "Simulates post-prandial walking cadence (95 steps/min)."),
        ("GLUT-4 Translocation:", "Triggers non-insulin-mediated glucose uptake into skeletal muscles."),
        ("Clinical Impact:", "Blunts peak postprandial glucose excursion by 25 to 45 mg/dL.")
    ], accent_color=ACCENT_CYAN, font_size=11.5)

    add_card(s6, 4.8, 1.7, 3.65, 5.0, "2. Carb Swap / Reduction", ACCENT_GOLD)
    add_bullet_list(s6, 5.0, 2.35, 3.25, 4.1, [
        ("Range: 0 to 60 grams:", "Simulates swapping white polished rice for foxtail/barnyard millets."),
        ("Absorption Blunting:", "Mitigates high-GI intestinal carbohydrate absorption kinetics."),
        ("Clinical Impact:", "Flattens steep glycemic curves back into the 70-180 mg/dL safe range.")
    ], accent_color=ACCENT_GOLD, font_size=11.5)

    add_card(s6, 8.8, 1.7, 3.65, 5.0, "3. Basal Insulin Titration", ACCENT_GREEN)
    add_bullet_list(s6, 9.0, 2.35, 3.25, 4.1, [
        ("Range: -4U to +4U:", "Simulates basal insulin titration or sulfonylurea timing shifts."),
        ("Overnight Clearance:", "Recalculates nighttime basal glucose drift and beta-cell kinetics."),
        ("Clinical Impact:", "Averts dangerous nocturnal crashes between 02:00 AM and 04:30 AM.")
    ], accent_color=ACCENT_GREEN, font_size=11.5)

    # =========================================================================
    # SLIDE 7: Real-World Clinical Walkthrough: Two Personas
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_background(s7)
    add_header(s7, "Clinical Validation & Scenarios", "Real-World Clinical Walkthrough: Indian Patient Personas", slide_num=7)

    add_card(s7, 0.8, 1.7, 5.65, 5.0, "Scenario A: Postprandial Spike (IND-PT-10007)", ACCENT_GOLD)
    add_bullet_list(s7, 1.05, 2.35, 5.15, 4.1, [
        ("Patient Profile:", "54y male, 9y T2D duration, baseline HbA1c 9.4%, BMI 28.2 kg/m², heavy rice staple diet."),
        ("Baseline 2h Forecast:", "Current glucose 185 mg/dL; Digital Twin forecasts surge to 218 mg/dL post-lunch (Amber Alert)."),
        ("Doctor Simulation:", "Doctor tests: 20-min post-meal brisk walk + 35g carb reduction (foxtail millet substitution)."),
        ("In-Silico Outcome:", "Simulated 2h glucose drops by -38 mg/dL to 180 mg/dL, restoring safe in-range control (70-180 mg/dL).")
    ], accent_color=ACCENT_GOLD, font_size=12)

    add_card(s7, 6.85, 1.7, 5.65, 5.0, "Scenario B: Nocturnal Crash (IND-PT-10004)", ACCENT_RED)
    add_bullet_list(s7, 7.1, 2.35, 5.15, 4.1, [
        ("Patient Profile:", "59y female on 22U evening basal insulin + sulfonylurea, 14y T2D duration, high hypoglycemia vulnerability."),
        ("Autonomic Signal at 02:30 AM:", "Current glucose 92 mg/dL, but HRV RMSSD plunges to 14ms (sympathetic counter-regulatory surge)."),
        ("Critical 2h Forecast:", "Digital Twin flags impending crash to 61 mg/dL at 04:30 AM (Critical Red Alert)."),
        ("In-Silico Outcome:", "Doctor simulates -3U evening basal titration + bedtime complex snack -> Crash averted (morning glucose 108 mg/dL).")
    ], accent_color=ACCENT_RED, font_size=12)

    # =========================================================================
    # SLIDE 8: Clinician Cockpit UI & Automated AI Presentation Mode
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_background(s8)
    add_header(s8, "User Interface & Experience", "Clinician Digital Twin Cockpit UI & Tour Mode", slide_num=8)

    add_card(s8, 0.8, 1.7, 5.65, 5.0, "Glassmorphic Web Dashboard (FastAPI + Chart.js)", ACCENT_CYAN)
    add_bullet_list(s8, 1.05, 2.35, 5.15, 4.1, [
        ("Virtual Patient Selector:", "Instantly switch across clinical personas (Hyper-prone, Hypo-prone, Controlled)."),
        ("4-Pillar Clinical Metric Bar:", "Current CGM, 2-Hour Forecast, Autonomic Stress Index (HR/HRV), and Time-in-Range (TIR)."),
        ("Dual Synchronized Waveforms:", "6h continuous CGM + 2h forecast band alongside continuous HR, HRV, steps, & meals."),
        ("Explainable AI (XAI) Drawer:", "Physiological root-cause attributions directly aligned with RSSDI & ADA guidelines.")
    ], accent_color=ACCENT_CYAN, font_size=12)

    add_card(s8, 6.85, 1.7, 5.65, 5.0, "Automated AI Presentation Mode", ACCENT_GOLD)
    add_bullet_list(s8, 7.1, 2.35, 5.15, 4.1, [
        ("Teleprompter Subtitle HUD:", "Floating presenter bar at the bottom displaying formatted, step-by-step clinical explanations."),
        ("Automated UI Interactivity:", "Auto-selects patients, smooth-scrolls to charts, and auto-animates sliders during recording."),
        ("Optional AI Voiceover:", "Built-in speech synthesis reads each slide explanation aloud with natural pacing."),
        ("Effortless Video Submission:", "Start screen record, click 'Start AI Guided Tour', and the prototype presents itself for 20 minutes!")
    ], accent_color=ACCENT_GOLD, font_size=12)

    # =========================================================================
    # SLIDE 9: DPDP Act 2023 Compliance & Socioeconomic Impact
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_background(s9)
    add_header(s9, "Regulatory Compliance & Socioeconomic Impact", "DPDP Act 2023 Compliance & Indian Healthcare Impact", slide_num=9)

    add_card(s9, 0.8, 1.7, 5.65, 5.0, "Indian DPDP Act 2023 & HIPAA Compliance", ACCENT_GREEN)
    add_bullet_list(s9, 1.05, 2.35, 5.15, 4.1, [
        ("100% Synthetic Patient Data:", "Synthea & MIMIC-IV clinical schemas calibrated to ICMR-INDIAB epidemiological metrics."),
        ("Zero Real Patient PII:", "Synthetic identities (IND-PT-XXXXX) eliminate privacy and re-identification risks."),
        ("Patient-Level Isolation:", "Complete separation between train and test patients eliminates data memorization."),
        ("Cryptographic Audit Trail:", "Every in-silico simulation and decision recommendation is timestamped and cryptographically logged.")
    ], accent_color=ACCENT_GREEN, font_size=12)

    add_card(s9, 6.85, 1.7, 5.65, 5.0, "Socioeconomic Impact & ABDM Roadmap", ACCENT_CYAN)
    add_bullet_list(s9, 7.1, 2.35, 5.15, 4.1, [
        ("Avoids Hospital Admissions:", "Saves families ₹40,000 to ₹1,50,000 per DKA or severe hypoglycemia emergency hospital stay."),
        ("37% Microvascular Risk Cut:", "Blunting glucose spikes reduces HbA1c by 0.8-1.2%, cutting kidney disease and retinopathy risk by 37%."),
        ("ABDM Integration Roadmap:", "Standardized FHIR APIs designed for Ayushman Bharat Digital Mission and e-Sanjeevani networks."),
        ("Edge AI Mobile App:", "Proactive smartphone nudges ('Take a 15-min walk now') democratizing digital twin care across India.")
    ], accent_color=ACCENT_CYAN, font_size=12)

    # =========================================================================
    # SLIDE 10: Conclusion & Summit Summary
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_background(s10)
    add_header(s10, "Summit Summary & Open Source Codebase", "Conclusion: Reimagining Healthcare in India 2026", slide_num=10)

    add_card(s10, 0.8, 1.7, 3.65, 5.0, "Key Breakthroughs", ACCENT_CYAN)
    add_bullet_list(s10, 1.0, 2.35, 3.25, 4.1, [
        ("Priority Condition Solved:", "End-to-end Digital Twin for Type 2 Diabetes in Asian Indian cohorts."),
        ("Dual Stream Fusion:", "Seamlessly unites static EHR with continuous wearable IoT telemetry."),
        ("Clinical Accuracy:", "7.15% MARD, 14.50 mg/dL RMSE, and 120-minute early warning.")
    ], accent_color=ACCENT_CYAN, font_size=11.5)

    add_card(s10, 4.8, 1.7, 3.65, 5.0, "Proactive Innovation", ACCENT_GOLD)
    add_bullet_list(s10, 5.0, 2.35, 3.25, 4.1, [
        ("In-Silico What-If Engine:", "Real-time simulation of walking, carb swaps, and insulin titration."),
        ("Doctor UI Cockpit:", "Production-ready web app with automated AI presentation tour mode."),
        ("DPDP Act Compliant:", "Zero PII risk with rigorous open-source reproducible pipeline.")
    ], accent_color=ACCENT_GOLD, font_size=11.5)

    add_card(s10, 8.8, 1.7, 3.65, 5.0, "Deliverables Ready", ACCENT_GREEN)
    add_bullet_list(s10, 9.0, 2.35, 3.25, 4.1, [
        ("Public GitHub Repo:", "Complete code, models, tests, datasets, and MIT License on Desktop."),
        ("Presentation Deck:", "Native 16:9 widescreen PowerPoint (.pptx) and PDF formats."),
        ("Architecture Diagram:", "Publication-grade vector PDF, PPTX, and SVG diagrams.")
    ], accent_color=ACCENT_GREEN, font_size=11.5)

    prs.save(output_path)
    print(f"✓ Successfully generated Executive Styled PowerPoint (.pptx): {output_path}")

if __name__ == "__main__":
    create_styled_deck()
