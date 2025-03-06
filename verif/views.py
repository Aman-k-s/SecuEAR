import os
import cv2
import numpy as np
import joblib
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from skimage.feature import local_binary_pattern, hog
from django.core.files.storage import default_storage
from django.conf import settings


# Load the trained model
MODEL_PATH = os.path.join(settings.BASE_DIR, "ml_model", "ear_auth_model.pkl")
svm_model = joblib.load(MODEL_PATH)

# Function to preprocess images
def preprocess_image(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)  # Convert to grayscale
    if img is None:
        return None  # Handle errors later
    
    img = cv2.resize(img, (128, 128))  # Resize
    img = img / 255.0  # Normalize
    return img

# Function to extract features
def extract_features(image):
    lbp_features = local_binary_pattern(image, P=8, R=1, method="uniform").flatten()
    hog_features = hog(image, pixels_per_cell=(8, 8), cells_per_block=(2, 2)).flatten()
    return np.hstack((lbp_features, hog_features))

@csrf_exempt
def verify_image(request):
    if request.method == "POST" and request.FILES.get("file"):
        file = request.FILES["file"]
        img = preprocess_image(file)
        features = extract_features(img).reshape(1, -1)

        result = svm_model.predict(features)
        confidence = svm_model.predict_proba(features)[0][result[0]] * 100  # Convert to percentage

        response = {
            "message": "Authenticated" if result[0] == 1 else "Not Recognized",
            "confidence": round(confidence, 2)
        }
        return JsonResponse(response)

    return JsonResponse({"error": "Invalid request"}, status=400)

# API to authenticate the user
@csrf_exempt
def authenticate_ear(request):
    if request.method == "POST" and request.FILES.get("file"):
        file = request.FILES["file"]
        file_path = default_storage.save("temp_ear.jpg", file)  # Save temp file
        image_path = default_storage.path(file_path)

        # Preprocess the image
        img = preprocess_image(image_path)
        if img is None:
            return JsonResponse({"error": "Invalid image"}, status=400)

        # Extract features
        features = extract_features(img).reshape(1, -1)

        # Predict
        result = svm_model.predict(features)
        confidence = svm_model.predict_proba(features)[0][result[0]]

        # Cleanup temp file
        default_storage.delete(file_path)

        # Return result
        return JsonResponse({
            "message": "Authenticated" if result[0] == 1 else "Not Recognized",
            "confidence": round(confidence * 100, 2)  # Confidence %
        })
    
    return JsonResponse({"error": "Invalid request"}, status=400)
