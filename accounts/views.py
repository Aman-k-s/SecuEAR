from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

# Create your views here.
def login_view(request):

    if request.user.is_authenticated:
        return redirect(reverse('home'))
    
    if request.method == 'POST':
        form = LoginForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.user
            # confidence = form.confidence

            login(request, user)
        
            return redirect(reverse('home')) 
    else:
        form = LoginForm()

    context = {'form':form}
    return render(request, 'login.html', context)

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