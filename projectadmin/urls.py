from django.urls import path
from django.views.generic import RedirectView

from .views import *
from .user_views import *
from .project_views import *


urlpatterns = [
    path('', RedirectView.as_view(url='home/', permanent=True), name='index'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('home/', home_view, name='home'),
    path('logout/', logout_view, name='logout'),
    path('users/', manage_users_view, name='users'),
    path('edit_user/<int:user_id>/', edit_user_view, name='edit_user'),
    path('delete_user/<int:user_id>/', delete_user_view, name='delete_user'),
    path('add_role/<int:user_id>/', add_role_view, name='add_role'),
    path('update_progress/<int:task_id>/', update_progress, name='update_progress'),
    path('update_status/<int:sub_tasks_id>/', update_status, name='update_status'),
    path('create_project/', create_project, name='create_project'),
    path('projects/', project_list, name='projects'),
    path('project/<int:project_id>/', project_detail, name='project_detail'),
    path('projects/<int:project_id>/add_task/', add_task, name='add_task'),
    path('tasks/<int:task_id>/add_sub_task/', add_subtask, name='add_subtask'),
    path('projects/<int:project_id>/edit/', edit_project, name='edit_project'),
    path('projects/<int:project_id>/delete/', delete_project, name='delete_project'),
    path('users/add/', add_user, name='add_user'),
    path('tasks/<int:task_id>/delete/', delete_task, name='delete_task'),
    path('subtasks/<int:subtask_id>/delete/', delete_subtask, name='delete_subtask'),
    path('upload_task_files/<int:task_id>/', upload_task_files, name='upload_task_files'),
    path('upload/project/', upload_project_files, name='upload_project_files'),
    path('upload/task/', upload_task_files, name='upload_task_files'),
    # files
    
    

    path('delete_file/<int:file_upload_id>/', delete_file, name='delete_file'),
    path('download_file/<int:file_upload_id>/', download_file, name='download_file'),
    

]
