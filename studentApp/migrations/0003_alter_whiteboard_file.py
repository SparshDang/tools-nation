# Generated by Django 4.2 on 2023-05-15 06:18

from django.db import migrations, models
import studentApp.models


class Migration(migrations.Migration):

    dependencies = [
        ('studentApp', '0002_alter_notepad_project_whiteboard_voicememo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='whiteboard',
            name='file',
            field=models.ImageField(upload_to=studentApp.models.get_whiteboard_file_name),
        ),
    ]
