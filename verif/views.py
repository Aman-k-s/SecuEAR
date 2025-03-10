import os
import uuid
import random
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now
from .models import Enrol, User


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

        user_instance=User.objects.get(user_id=user_id)

        if not user_id or not transaction_ref or not file_path:
            return JsonResponse({"success": False, "error": "Missing required fields"}, status=400)



        enrol = Enrol.objects.create(
            enrol_id=uuid.uuid4().hex, 
            user_code=user_instance,
            transaction_ref=transaction_ref,
            uploaded_at=now(),
            depth_map=file_path,
            confidence=None,
        )

        enrol.confidence = round(random.uniform(0.5, 1.0), 2)
        enrol.save()

        return redirect(f"/landing/{enrol.enrol_id}")

    return render(request, "home.html")


def landing(request, enrol_id):
    enrol = get_object_or_404(Enrol, enrol_id=enrol_id)

    status = True if enrol.confidence >= 0.7 else False
    
    return render(request, "landing.html", {"enrol": enrol, "status": status})
