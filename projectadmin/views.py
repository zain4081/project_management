from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate, logout
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm

def login_view(request):
    message = ""
    if request.method == 'POST':
        form = UserLoginForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            if user.role:
                messages.success(request, 'You have successfully logged in.')
                return redirect('home')
            else:
                message = "Your account is pending verification. Please contact Admin"
                return render(request, 'projectadmin/login.html', {'form': form, 'msg':message})
    else:
        form = UserLoginForm()
    return render(request, 'projectadmin/login.html', {'form': form, 'msg':message})

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            auth_login(request, user)
            messages.success(request, 'You have successfully registered and logged in.')
            return redirect('login')
    else:
        form = UserRegistrationForm(initial=request.POST)
    return render(request, 'projectadmin/register.html', {'form': form})

def home_view(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Please log in to access the home page.')
        return redirect('login')
    user_info = {
        'username': request.user.username,
        'email': request.user.email,
        'name': request.user.name,
        'role': request.user.role,
    }
    return render(request, 'projectadmin/home.html',{'user_info': user_info})

def logout_view(request):
    logout(request)
    return redirect('login')
