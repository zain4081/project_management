from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from .models import CustomUser, Project, Task, SubTask, FileUpload


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'username', 'password1', 'password2']



class UserLoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']


class EditUserForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'name', 'role', 'password']

class AddUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'name', 'role', 'password1', 'password2']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # Add Bootstrap classes to the labels for password fields
            self.fields['password1'].widget.attrs['class'] = 'form-control'
            self.fields['password2'].widget.attrs['class'] = 'form-control'


class ProjectForm(forms.ModelForm):
    manager = forms.ModelChoiceField(queryset=CustomUser.objects.filter(role__in=['Project Manager']), empty_label=None)
    team_members = forms.ModelMultipleChoiceField(
        queryset=CustomUser.objects.exclude(role__in=['Project Manager', 'Admin']),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control select2'})
    )

    class Meta:
        model = Project
        fields = ['name', 'description', 'start_date', 'end_date', 'visibility', 'manager', 'team_members']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control'}),
            'visibility': forms.Select(attrs={'class': 'form-control'}),
            'manager': forms.Select(attrs={'class': 'form-control'}),
            'team_members': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'assigned_to', 'progress', 'status']

class SubTaskForm(forms.ModelForm):
    class Meta:
        model = SubTask
        fields = ['name', 'details', 'current_status']


# File Management
class UploadProjectFileForm(forms.ModelForm):
    class Meta:
        model = FileUpload
        fields = ['project', 'file']

    def __init__(self, *args, **kwargs):
        super(UploadProjectFileForm, self).__init__(*args, **kwargs)
        self.fields['file'].required = False  # Allow clearing the file field

class UploadTaskFileForm(forms.ModelForm):
    class Meta:
        model = FileUpload
        fields = ['task', 'file']

    def __init__(self, *args, **kwargs):
        super(UploadTaskFileForm, self).__init__(*args, **kwargs)
        self.fields['file'].required = False 