# Generated by Django 4.2.7 on 2023-11-27 13:16

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projectadmin', '0003_project'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('role', models.CharField(choices=[('Developer', 'Developer'), ('QA', 'QA'), ('Designer', 'Designer')], max_length=20)),
                ('progress', models.PositiveIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(100)])),
                ('status', models.CharField(choices=[('Not Started', 'Not Started'), ('In Progress', 'In Progress'), ('Completed', 'Completed')], default='Not Started', max_length=20)),
                ('assigned_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projectadmin.project')),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='tasks',
            field=models.ManyToManyField(blank=True, related_name='project_tasks', to='projectadmin.task'),
        ),
    ]