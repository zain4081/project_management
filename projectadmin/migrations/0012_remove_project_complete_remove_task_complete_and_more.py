# Generated by Django 4.2.7 on 2024-01-12 14:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projectadmin', '0011_project_complete_task_complete_task_total_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='complete',
        ),
        migrations.RemoveField(
            model_name='task',
            name='complete',
        ),
        migrations.RemoveField(
            model_name='task',
            name='total',
        ),
    ]
