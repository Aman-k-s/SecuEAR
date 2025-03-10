import os
import uuid
import random
import numpy as np
import open3d as o3d
import joblib
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now
from skimage.feature import hog
import cv2
from .models import Enrol, User

# Load the trained SVM model
MODEL_PATH = os.path.join("ml_model", "svm_ear_recognition_model.pkl")
model = joblib.load(MODEL_PATH)

# Function to extract features from a PLY file
def extract_ply_features(ply_path):
    pcd = o3d.io.read_point_cloud(ply_path)
    points = np.asarray(pcd.points)
    mean = np.mean(points, axis=0)
    std = np.std(points, axis=0)
    return np.hstack([mean, std])

def upload_file(request):
    if request.method == "POST" and request.FILES.get("fileInput"):
        file = request.FILES["fileInput"]

        if not file.name.lower().endswith(".ply"):
            return JsonResponse({"success": False, "error": "Only .ply files are allowed!"}, status=400)

        # Generate a 10-character hex filename
        new_filename = f"{uuid.uuid4().hex[:10]}.ply"
        temp_path = f"depth_maps/{new_filename}"
        
        file_path = default_storage.save(temp_path, ContentFile(file.read()))

        return JsonResponse({"success": True, "temp_file_path": file_path})
    
    return JsonResponse({"success": False, "error": "No file uploaded"}, status=400)

def home(request):
    if request.method == "POST":
        user_id = request.POST.get("userID")
        transaction_ref = request.POST.get("transactionRef")
        file_path = request.POST.get("temp_file_path")

        user_instance = User.objects.get(user_id=user_id)

        if not user_id or not transaction_ref or not file_path:
            return JsonResponse({"success": False, "error": "Missing required fields"}, status=400)

        # Extract features from PLY file
        abs_file_path = os.path.join(default_storage.location, file_path)
        features = extract_ply_features(abs_file_path)
        features = np.array(features).reshape(1, -1)  # Reshape for model

        # Predict confidence using the ML model
        confidence = float(model.predict(features)[0])

        # Store in the database
        enrol = Enrol.objects.create(
            enrol_id=uuid.uuid4().hex, 
            user_code=user_instance,
            transaction_ref=transaction_ref,
            uploaded_at=now(),
            depth_map=file_path,
            confidence=confidence,
        )

        return redirect(f"/landing/{enrol.enrol_id}")

    return render(request, "home.html")

def landing(request, enrol_id):
    enrol = get_object_or_404(Enrol, enrol_id=enrol_id)

    status = True if enrol.confidence >= 0.7 else False
    
    return render(request, "landing.html", {"enrol": enrol, "status": status})
