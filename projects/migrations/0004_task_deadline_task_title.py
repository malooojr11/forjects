# Generated by Django 5.0.3 on 2024-03-29 16:00

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_alter_task_project'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='Deadline',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='task',
            name='title',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
