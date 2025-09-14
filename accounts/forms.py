from django import forms
from accounts.models import User
from django.contrib.auth import authenticate
from model.match_user import match_user

class LoginForm(forms.Form):
    username = forms.CharField(max_length=64)
    scan = forms.FileField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None  # initialize here

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        scan = cleaned_data.get('scan')

        if username and scan:
            confidence = match_user(scan)

            if confidence < 70:
                raise forms.ValidationError(f"Authentication failed (confidence: {confidence})")
            
            self.user = User.objects.filter(username=username).first()
            self.confidence = round(confidence, 2)

            if not self.user:
                raise forms.ValidationError("User does not exist")
        return cleaned_data

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
