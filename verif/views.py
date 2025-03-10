import os
import uuid
import random
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now
from .models import Enrol


def upload_file(request):
    if request.method == "POST" and request.FILES.get("fileInput"):
        file = request.FILES["fileInput"]

        if not file.name.lower().endswith(".ply"):
            return JsonResponse({"success": False, "error": "Only .ply files are allowed!"}, status=400)

        temp_path = f"temp/{file.name}"
        file_path = default_storage.save(temp_path, ContentFile(file.read()))

        return JsonResponse({"success": True, "temp_file_path": file_path})
    
    return JsonResponse({"success": False, "error": "No file uploaded"}, status=400)


def home(request):
    if request.method == "POST":
        user_id = request.POST.get("userID")
        transaction_ref = request.POST.get("transactionRef")
        temp_file_path = request.POST.get("temp_file_path")

        if not user_id or not transaction_ref or not temp_file_path:
            return redirect("/")

        new_filename = f"{uuid.uuid4().hex}.ply"
        new_file_path = f"depth_maps/{new_filename}"
        
        temp_full_path = os.path.join(default_storage.location, temp_file_path)
        new_full_path = os.path.join(default_storage.location, new_file_path)

        if os.path.exists(temp_full_path):
            os.rename(temp_full_path, new_full_path)
        else:
            return redirect("landing", status="failed")

        enrol = Enrol.objects.create(
            enrol_id=uuid.uuid4().hex,
            user_id=user_id,
            transaction_ref=transaction_ref,
            uploaded_at=now(),
            depth_map=new_file_path,
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
