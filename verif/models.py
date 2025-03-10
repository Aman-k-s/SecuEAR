from django.db import models
import uuid

def generate_enrol_id():
    return uuid.uuid4().hex[:10]

def generate_user_code():
    return uuid.uuid4().hex[:10]

class User(models.Model):
    user_id = models.PositiveIntegerField(unique=True)
    user_code = models.CharField(
        primary_key=True,
        max_length=10,
        unique=True,
        default=generate_user_code
    )
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user_id} - {self.name}"


class Enrol(models.Model):
    enrol_id = models.CharField(
        max_length=64,
        primary_key=True,
        default=generate_enrol_id,
        editable=False
    )
    user_code = models.ForeignKey(User, on_delete=models.CASCADE) 
    transaction_ref = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    depth_map = models.FileField(upload_to="depth_maps/")
    confidence = models.FloatField(null=True, blank=True) 

    def __str__(self):
        return f"{self.enrol_id}"
