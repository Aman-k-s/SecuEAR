from django import forms
from accounts.models import User
import numpy as np
import cv2 

# forms.py
class LoginForm(forms.Form):
    username = forms.CharField(max_length=64)
    scan = forms.FileField()

class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        label="Password",
        max_length=128,  # optional, just for clarity
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput,
        label="Confirm Password"
    )

    class Meta:
        model = User
        fields = ['username']  # just username, don't include password

    def clean(self):
        cleaned_data = super().clean()
        pw = cleaned_data.get('password')
        cpw = cleaned_data.get('confirm_password')
        if pw and cpw and pw != cpw:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # hash password
        if commit:
            user.save()
        return user
