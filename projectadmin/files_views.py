
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.http import FileResponse


import os
from .models import FileUpload, Project, Task
from .forms import UploadProjectFileForm

def files(request):
    # Your logic to fetch projects, tasks, and file uploads
    projects = Project.objects.all()
    tasks = Task.objects.all()
    file_uploads = FileUpload.objects.all()

    return render(request, 'projectadmin/project_files.html', {'projects': projects, 'file_uploads': file_uploads})

def file_management(request):
    projects = Project.objects.all()
    tasks = Task.objects.all()

    # Create a structure to hold project details, tasks, and file uploads
    project_details = []
    for project in projects:
        project_files = FileUpload.objects.filter(project=project)
        tasks = project.tasks.all()  # Assuming you have a related name 'project_tasks' in Task model

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

    return render(request, 'projectadmin/project_files.html', {'project_details': project_details})

def upload_project_file(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == 'POST':
        form = UploadProjectFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data['file']

            # Create a custom file name
            file_name = f"{project.name} ProjectFile"
            
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
                form.instance.project = project
                form.save()

            return redirect('project_files')
    else:
        form = UploadProjectFileForm()

    return render(request, 'projectadmin/project_files.html', {'form': form, 'project': project})

def delete_files(request, file_upload_id):
    file_upload = get_object_or_404(FileUpload, id=file_upload_id)

    # Get the associated project
    project = file_upload.project

    # Get the file path
    file_path = file_upload.file.path

    # Delete the file upload entry
    file_upload.delete()

    # Delete the file from the filesystem
    try:
        os.remove(file_path)
    except OSError:
        return HttpResponseBadRequest("Failed to delete file from the filesystem.")

    # Redirect to the appropriate location (project files list)
    return redirect('project_files')

def download_files(request, file_upload_id):
    file_upload = get_object_or_404(FileUpload, id=file_upload_id)
    file_path = file_upload.file.path

    if file_path:
        # Use FileResponse instead of FileWrapper
        response = FileResponse(open(file_path, 'rb'), as_attachment=True)
        response['Content-Disposition'] = f'attachment; filename={file_upload.file.name}'
        return response
    else:
        return render(request, 'file_not_found.html') 
