# Generated by Django 4.2.7 on 2024-01-12 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projectadmin', '0010_task_subtasks'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='complete',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='task',
            name='complete',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='task',
            name='total',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='task',
            name='subtasks',
            field=models.ManyToManyField(blank=True, related_name='task_subtask', to='projectadmin.subtask'),
        ),
    ]
