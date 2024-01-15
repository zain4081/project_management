# myapp/user_views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import CustomUser
from django.contrib import messages
from .forms import EditUserForm, AddUserForm

def manage_users_view(request):
    users = CustomUser.objects.all()
    return render(request, 'projectadmin/manage_users.html', {'users': users})

def edit_user_view(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User updated successfully.')
            return redirect('users')
    else:
        form = EditUserForm(instance=user)

    return render(request, 'projectadmin/edit_user.html', {'form': form, 'user': user})

def delete_user_view(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'User deleted successfully.')
        return redirect('users')

    return render(request, 'projectadmin/delete_user.html', {'user': user})

def add_role_view(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'POST':
        role = request.POST.get('role')
        user.role = role
        user.save()
        messages.success(request, f'Role "{role}" added to user {user.username} successfully.')
        return redirect('users')

    return render(request, 'projectadmin/add_role.html', {'user': user})


def add_user(request):
    if request.method == 'POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('users')
    else:
        form = AddUserForm()

    return render(request, 'projectadmin/add_user.html', {'form': form})
