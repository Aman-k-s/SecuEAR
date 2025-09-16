from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    dummy_field = models.CharField(max_length=64, blank=True)
    def __str__(self):
        return self.username
    
class Login(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    scan_input = models.ImageField(upload_to="input")