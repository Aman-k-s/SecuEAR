import cv2
import numpy as np
from skimage.feature import hog
import joblib

# Function to extract HOG features from a test image
def extract_hog(image):
    features = hog(image, orientations=8, pixels_per_cell=(16, 16),
                   cells_per_block=(1, 1), visualize=False)
    return features

# Function to call from backend
def match_user(image_path, model_path="svm_model_hog.pkl"):
    # Load trained model and label encoder
    model, label_encoder = joblib.load(model_path)

    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError(f"Image not found: {image_path}")

    img = cv2.resize(img, (224, 224))
    features = extract_hog(img).reshape(1, -1)

    # Prediction
    prediction = model.predict(features)[0]
    confidence = model.predict_proba(features)[0].max()
    user_name = label_encoder.inverse_transform([prediction])[0]
    return user_name, round(confidence, 2)
