# Generated by Django 4.2.7 on 2023-11-21 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projectadmin', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='role',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
