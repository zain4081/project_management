# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from pyexpat.errors import messages
from django.db.models import Count
from django.http import HttpResponse


# projects & Task
from .models import Project, CustomUser, Task, SubTask
from .forms import ProjectForm, TaskForm, SubTaskForm

# Files
from .forms import UploadProjectFileForm, UploadTaskFileForm
from .models import  FileUpload
from wsgiref.util import FileWrapper
import os
from django.conf import settings
from django.http import HttpResponseBadRequest


@login_required
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        form.fields['name'].widget.attrs.update({'class': 'form-control'})
        form.fields["description"].widget.attrs.update({'class': 'form-control'})
        form.fields['start_date'].widget.attrs.update({'class': 'form-control'})
        form.fields['end_date'].widget.attrs.update({'class': 'form-control'})
        form.fields['visibility'].widget.attrs.update({'class': 'form-control'})
        form.fields['manager'].widget.attrs.update({'class': 'form-control'})
        form.fields['team_members'].widget.attrs.update({'class': 'form-control'})

        if form.is_valid():
            project = form.save(commit=False)
            project.manager = request.user
            project.save()
            form.save_m2m()  # Save many-to-many relationships (team_members)
            return redirect('projects')  # Redirect to project list page
    else:
        form = ProjectForm()

    return render(request, 'projectadmin/create_project.html', {'form': form})

@login_required
def project_list(request):
    if request.user.is_authenticated:
        if request.user.role in ['Admin', 'Project Manager']:
            # If Admin or Project Manager, show all projects and tasks
            projects = Project.objects.all()
            tasks = Task.objects.all()
            sub_tasks = SubTask.objects.all()
        else:
            # If not Admin or Project Manager, show only assigned projects and tasks
            projects = Project.objects.filter(team_members=request.user)
            tasks = Task.objects.filter(project__team_members=request.user)
            sub_tasks = SubTask.objects.filter(task__project__team_members=request.user)

            
    else:
        projects = []
        tasks = []
        sub_tasks = []

    task_form = TaskForm()
    sub_task_form = SubTaskForm()
    return render(request, 'projectadmin/project_list.html', {'projects': projects, 'task_form': task_form, 'tasks':tasks, 'sub_task_form': sub_task_form, 'sub_tasks':sub_tasks})

@login_required
def add_task(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == 'POST':
        task_form = TaskForm(request.POST)
        if task_form.is_valid():
            task = task_form.save(commit=False)
            task.project = project
            task.save()
            project.tasks.add(task)  # Add the task to the project's tasks

    return redirect('projects')

@login_required
def add_subtask(request, task_id):
    task = get_object_or_404(Task, pk=task_id)

    if request.method == 'POST':
        sub_task_form = SubTaskForm(request.POST)
        if sub_task_form.is_valid():
            sub_task = sub_task_form.save(commit=False)
            sub_task.task = task
            sub_task.save()
            task.subtasks.add(sub_task)  # Add the sub task to the tasks 

    return redirect('projects')

def update_progress(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        progress = request.POST.get('progress')
        task.progress = progress
        if progress == 0:
            task.status ='Not Started'
        elif int(progress) > 0 and int(progress) < 100:
            task.status = "In Progress"
        else:
            task.status = 'Completed'

        task.save()

        return redirect('projects')

    return redirect('projects')

def update_status(request, sub_tasks_id):
    subtask = get_object_or_404(SubTask, id=sub_tasks_id)

    if request.method == 'POST':
        subtask.current_status = 'Completed'
        subtask.save()
        return redirect('projects')
    
    return redirect('projects')


@login_required
def project_detail(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == 'POST':
        task_form = TaskForm(request.POST)
        if task_form.is_valid():
            task = task_form.save(commit=False)
            task.project = project
            task.save()
            project.tasks.add(task)  # Add the task to the project's tasks
            return redirect('projects')
    else:
        task_form = TaskForm()

    return render(request, 'projectadmin/project_details.html', {'project': project, 'task_form': task_form})

@login_required
def edit_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('projects')
    else:
        form = ProjectForm(instance=project)

    return render(request, 'projectadmin/edit_project.html', {'form': form, 'project': project})

@login_required
def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    # Add logic to handle project deletion
    project.delete()
    return redirect('projects')

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    task.delete()
    return redirect('projects')

@login_required
def delete_subtask(request, subtask_id):
    subtask = get_object_or_404(SubTask, pk=subtask_id)
    subtask.delete()
    return redirect('projects')


#-------------------- File Management --------------------------------


def download_file(request, file_upload_id):
    file_upload = get_object_or_404(FileUpload, id=file_upload_id)
    file_path = file_upload.file.path
    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            response = HttpResponse(FileWrapper(file), content_type='application/force-download')
            response['Content-Disposition'] = f'attachment; filename={os.path.basename(file_path)}'
            return response
    else:
        return HttpResponse('File not found', status=404)

def files(request):
    projects = Project.objects.all()
    tasks = Task.objects.all()
    file_uploads = FileUpload.objects.all()

    return render(request, 'projectadmin/project_list.html', {'projects': projects, 'tasks': tasks, 'file_uploads': file_uploads})

def file_management(request):
    projects = Project.objects.all()

    # Create a structure to hold project details, tasks, and file uploads
    project_details = []
    for project in projects:
        project_files = FileUpload.objects.filter(project=project)
        tasks = Task.objects.filter(project=project)

        task_details = []
        for task in tasks:
            task_files = FileUpload.objects.filter(task=task)
            task_details.append({
                'task': task,
                'files': task_files,
            })

        project_details.append({
            'project': project,
            'files': project_files,
            'tasks': task_details,
        })

    return render(request, 'projectadmin/files.html', {'project_details': project_details})

def upload_project_files(request):
    if request.method == 'POST':
        form = UploadProjectFileForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.cleaned_data['project']
            file = form.cleaned_data['file']
            
            _, original_extension = os.path.splitext(file.name)

            # Create a custom file name
            file_name = f"{project.name} ProjectFile{original_extension}"
            
            # Check if a file with the same project already exists
            existing_file_upload = FileUpload.objects.filter(project=project).first()

            if existing_file_upload:
                # Update existing entry
                existing_file_upload.file = file
                existing_file_upload.file.name = file_name
                existing_file_upload.save()
            else:
                # Create new entry
                form.instance.file.name = file_name
                form.save()

            return redirect('projects')
    else:
        form = UploadProjectFileForm()

    return render(request, 'projectadmin/project_list.html', {'form': form})

def upload_task_files(request):
    if request.method == 'POST':
        form = UploadTaskFileForm(request.POST, request.FILES)
        if form.is_valid():
            task = form.cleaned_data['task']
            file = form.cleaned_data['file']

            # Extract the original file extension
            _, original_extension = os.path.splitext(file.name)

            # Create a custom file name with the original extension
            file_name = f"{task.project.name}/{task.title} TaskFile{original_extension}"
            
            # Check if a file with the same task already exists
            existing_file_upload = FileUpload.objects.filter(task=task).first()

            if existing_file_upload:
                # Update existing entry
                existing_file_upload.file = file
                existing_file_upload.file.name = file_name
                existing_file_upload.save()
            else:
                # Create new entry
                form.instance.file.name = file_name
                form.save()

            return redirect('projects')
    else:
        form = UploadTaskFileForm()
    
    return render(request, 'projectadmin/project_list.html', {'form': form})



def delete_file(request, file_upload_id):
    file_upload = get_object_or_404(FileUpload, id=file_upload_id)

    # Get the associated project or task
    project = file_upload.project
    task = file_upload.task

    # Get the file path
    file_path = file_upload.file.path

    # Delete the file upload entry
    file_upload.delete()

    # Delete the file from the filesystem
    try:
        os.remove(file_path)
    except OSError:
        return HttpResponseBadRequest("Failed to delete file from the filesystem.")

    # Redirect to the appropriate location (project or task details)
    return redirect('projects')
