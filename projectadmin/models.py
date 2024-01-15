# myapp/models.py
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator
from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver


class CustomUser(AbstractUser):
    USER_ROLE_CHOICES = [
        ('Project Manager', 'Project Manager'),
        ('Team Lead', 'Team Lead'),
        ('Developer', 'Developer'),
        ('Designer', 'Designer'),
        ('Quality Assurance Specialist', 'Quality Assurance Specialist'),
    ]
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=50, blank=True, choices=USER_ROLE_CHOICES)

    def __str__(self):
        return self.name
class SubTask(models.Model):
    TASK_STATUS_CHOICES = [
        ('Not Started', 'Not Started'),
        ('Completed', 'Completed'),
    ]
    task = models.ForeignKey('Task', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    details = models.CharField(max_length=255)
    current_status = models.CharField(max_length=20, choices=TASK_STATUS_CHOICES, default='Not Started')
    

    
    


class Task(models.Model):
    TASK_STATUS_CHOICES = [
        ('Not Started', 'Not Started'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]

    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    progress = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(100)])
    status = models.CharField(max_length=20, choices=TASK_STATUS_CHOICES, default='Not Started')
    subtasks  = models.ManyToManyField(SubTask, blank=True, related_name='task_subtask')
    complete = models.PositiveBigIntegerField(default=0)
    total = models.PositiveSmallIntegerField(default=0)


    

class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    manager = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='managed_projects')
    team_members = models.ManyToManyField(CustomUser, related_name='assigned_projects')
    visibility = models.CharField(max_length=20, choices=[('public', 'Public'), ('private', 'Private')])
    tasks = models.ManyToManyField(Task, related_name='project_tasks', blank=True)
    complete = models.PositiveBigIntegerField(default=0)
    total = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.name

class FileUpload(models.Model):
    project = models.ForeignKey(Project, null=True, blank=True, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, null=True, blank=True, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

# Task table updation from subtasks
@receiver(post_save, sender=SubTask)
def update_task_progress_on_subtask_save(sender, instance, **kwargs):
    if instance.current_status == 'Completed':
        instance.task.complete += 1
        instance.task.save()

@receiver(pre_delete, sender=SubTask)
def update_task_progress_on_subtask_delete(sender, instance, **kwargs):
    if instance.current_status == 'Completed':
        instance.task.complete -= 1
        instance.task.save()

@receiver(post_save, sender=SubTask)
def update_task_on_subtask_save(sender, instance, **kwargs):
    instance.task.total = instance.task.subtask_set.count()
    instance.task.save()

@receiver(pre_delete, sender=SubTask)
def update_task_on_subtask_delete(sender, instance, **kwargs):
    instance.task.total = instance.task.subtask_set.count() - 1
    instance.task.save()


# Project Table updation from tasks
@receiver(post_save, sender=Task)
def update_task_progress_on_subtask_save(sender, instance, **kwargs):
    if instance.status == 'Completed':
        instance.project.complete += 1
        instance.project.save()

@receiver(pre_delete, sender=Task)
def update_task_progress_on_subtask_delete(sender, instance, **kwargs):
    if instance.status == 'Completed':
        instance.project.complete -= 1
        instance.project.save()


@receiver(post_save, sender=Task)
def update_project_on_task_save(sender, instance, **kwargs):
    instance.project.total_tasks = instance.project.task_set.count()
    instance.project.save()

@receiver(pre_delete, sender=Task)
def update_project_on_task_delete(sender, instance, **kwargs):
    project = instance.project
    project.total_tasks = project.task_set.count() - 1 if project.task_set.count() > 0 else 0
    project.save()
