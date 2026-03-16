from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm, RegisterForm, ProfileForm
from .models import CustomUser
from django.shortcuts import get_object_or_404

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            # Auto-upgrade superuser to admin role
            if user.is_superuser and user.role != 'admin':
                user.role = 'admin'
                user.save()
            login(request, user)
            return redirect('dashboard:home')
        messages.error(request, 'Invalid credentials.')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('accounts:login')

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'accounts/profile.html', {'form': form})


@login_required
def edit_user(request, pk):
    if not request.user.is_admin():
        messages.error(request, 'Access denied.')
        return redirect('dashboard:home')
    target_user = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        target_user.role = request.POST.get('role', target_user.role)
        target_user.is_active = 'is_active' in request.POST
        target_user.save()
        messages.success(request, f'User {target_user.username} updated.')
        return redirect('accounts:user_list')
    return render(request, 'accounts/edit_user.html', {'target_user': target_user})


@login_required
def user_list(request):
    if not request.user.is_admin():
        messages.error(request, 'Access denied.')
        return redirect('dashboard:home')
    users = CustomUser.objects.all().order_by('-created_at')
    return render(request, 'accounts/user_list.html', {'users': users})

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Account created! Welcome, {user.username}.')
            return redirect('dashboard:home')
        messages.error(request, 'Please fix the errors below.')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})
