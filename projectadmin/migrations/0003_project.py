# Generated by Django 4.2.7 on 2023-11-21 17:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projectadmin', '0002_customuser_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('visibility', models.CharField(choices=[('public', 'Public'), ('private', 'Private')], max_length=20)),
                ('manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='managed_projects', to=settings.AUTH_USER_MODEL)),
                ('team_members', models.ManyToManyField(related_name='assigned_projects', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
