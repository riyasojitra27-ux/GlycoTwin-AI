"""
Unit and Integration Tests for GlycoTwin-AI Pipeline
"""

import unittest
import pandas as pd
from models.digital_twin_engine import GlycoTwinEngine

class TestGlycoTwinPipeline(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = GlycoTwinEngine(models_dir="models/saved_models")
        cls.ehr_df = pd.read_csv("data/ehr_patients.csv")
        cls.telem_df = pd.read_csv("data/wearable_cgm_telemetry.csv")

    def test_model_loading(self):
        self.assertIsNotNone(self.engine.regressor)
        self.assertIsNotNone(self.engine.classifier)
        self.assertIn("features", self.engine.metadata)
        self.assertEqual(self.engine.metadata["prediction_horizon_minutes"], 120)

    def test_twin_evaluation(self):
        sample_ehr = self.ehr_df.iloc[0].to_dict()
        pid = sample_ehr["patient_id"]
        pt_telem = self.telem_df[self.telem_df["patient_id"] == pid].head(24)
        
        status = self.engine.evaluate_twin_status(sample_ehr, pt_telem)
        self.assertIn("predicted_glucose_2h", status)
        self.assertIn("predicted_event_code", status)
        self.assertIn("probabilities", status)
        self.assertIn("clinical_explanations", status)
        self.assertGreater(status["predicted_glucose_2h"], 30.0)
        self.assertLess(status["predicted_glucose_2h"], 450.0)

    def test_what_if_simulation(self):
        sample_ehr = self.ehr_df.iloc[7].to_dict() # Hyperglycemia prone
        pid = sample_ehr["patient_id"]
        pt_telem = self.telem_df[self.telem_df["patient_id"] == pid].head(24)
        
        # Test counterfactual walk + carb reduction
        sim = self.engine.simulate_what_if(
            sample_ehr, 
            pt_telem, 
            walk_minutes=20, 
            carb_reduction_grams=35, 
            insulin_adjustment_units=0
        )
        self.assertIn("baseline", sim)
        self.assertIn("simulated", sim)
        self.assertIn("delta_glucose_mg_dl", sim)
        self.assertIn("clinical_recommendation", sim)

if __name__ == "__main__":
    unittest.main()
