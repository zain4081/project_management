# Generated by Django 4.2.7 on 2023-11-27 13:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projectadmin', '0004_task_project_tasks'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='role',
        ),
    ]