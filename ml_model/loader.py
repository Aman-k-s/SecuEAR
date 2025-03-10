import os
import joblib

# Define path for the model
MODEL_PATH = os.path.join(os.path.dirname(__file__), "svm_ear_recognition_model.pkl")

# Load the model once
model = joblib.load(MODEL_PATH)
