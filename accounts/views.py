from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from model.match_user import match_user
from model.depth_map import generate_depth_map
from .models import Login, User

def validate_user(ply_file_path, user_profile_data):
    depth_map = generate_depth_map(ply_file_path)
    return match_user(image_path=depth_map)[1]

def login_view(request):
    if request.user.is_authenticated:
        return redirect(reverse('home'))
    
    if request.method == 'POST':
        form = LoginForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            uploaded_file = form.cleaned_data.get('scan')

            try:
                user_to_login = User.objects.get(username=username)
            except User.DoesNotExist:
                form.add_error('username', 'User does not exist.')
                return render(request, 'login.html', {'form': form})
            
            try:
                login_scan = Login(scan_input=uploaded_file, User = user_to_login)
                login_scan.save()
                
                ply_file_path = login_scan.scan_input.path
                
                # Step 3: Use the file path to run your 3D authentication logic.
                # Your `validate_user` function must now accept a file path.
                confidence = validate_user(ply_file_path, user_profile_data=user_to_login)

                if confidence < 0.70: # Use your desired confidence threshold
                    form.add_error('scan', f"Authentication failed (confidence: {confidence:.2f})")
                    # Delete the saved file on failure to save space
                    login_scan.delete() 
                    return render(request, 'login.html', {'form': form})
                
                # Step 4: Authentication is successful. The file is already saved. Log the user in.
                login(request, user_to_login)
                return redirect(reverse('home'))
            
            except Exception as e:
                # Catch any unexpected errors, like file I/O or 3D processing errors.
                form.add_error('scan', f"An error occurred: {e}")
                # Clean up the saved file if an error occurs after saving
                if 'login_scan' in locals():
                    login_scan.delete()
                return render(request, 'login.html', {'form': form})
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')

def register(request):
    if request.user.is_authenticated:
        return redirect(reverse('home'))
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit = False)

            user.set_password(form.cleaned_data['password'])
            user.save()

            login(request, user)

            return redirect(reverse('home'))
    else:
        form = RegisterForm()
    context = {
        'form':form
    }
    return render(request, 'register.html', context)


@login_required(login_url='login')
def home(request):
    context = {
        'user':request.user
    }
    return render(request, 'home.html',context)