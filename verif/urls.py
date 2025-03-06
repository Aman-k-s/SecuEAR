from django.urls import path
from .views import authenticate_ear, verify_image

urlpatterns = [
    path("authenticate/", authenticate_ear, name="authenticate_ear"),
    path("verify/", verify_image, name="verify_image")
]
