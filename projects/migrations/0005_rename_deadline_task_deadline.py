# Generated by Django 5.0.3 on 2024-03-29 16:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_task_deadline_task_title'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='Deadline',
            new_name='deadline',
        ),
    ]
