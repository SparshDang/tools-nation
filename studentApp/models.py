from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os


class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name




class Project(models.Model):
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description  = models.CharField(max_length=200, null=True, blank=True)
    start_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

class Note(models.Model):
    project = models.ForeignKey(Project, verbose_name="project", on_delete=models.CASCADE)
    title = models.CharField(max_length=50, null=True, blank=True)
    text = models.TextField()

    def __str__(self):
        return self.title if  self.title else 'title'

class Reminder(models.Model):
    project = models.ForeignKey(Project, verbose_name="project", on_delete=models.CASCADE)
    schedule = models.DateTimeField()
    text = models.CharField(max_length = 50)

    def __str__(self):
        return self.text

class Notepad(models.Model):
    project = models.OneToOneField(Project, verbose_name="project", on_delete=models.CASCADE)
    body=RichTextField(blank=True,null=True)

    def __str__(self):
        return f"Notepad : {self.id}"
    
def get_whiteboard_file_name(instance , file_name):
        return 'uploads/user_{0}/whiteboard/{1}'.format(instance.project.user.id, file_name)

class Whiteboard(models.Model):
    project = models.OneToOneField(Project, verbose_name="project", on_delete=models.CASCADE)
    file = models.ImageField(max_length=200, storage = OverwriteStorage() ,upload_to=get_whiteboard_file_name)
    
    def __str__(self) -> str:
        return f"{self.project.name} : {self.file}"


def get_voice_memo_file_name( instance, file_name):
    return 'uploads/user_{0}/file/{1}'.format(instance.project.user.id, file_name)

class FileUploads(models.Model):
    project = models.ForeignKey(Project, verbose_name="project", on_delete=models.CASCADE)
    file = models.FileField(upload_to=get_voice_memo_file_name)

    def __str__(self) -> str:
        return f"{self.project.name} : {self.file}"


