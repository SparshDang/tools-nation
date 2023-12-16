from typing import Any, Dict
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView, ListView, DetailView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User



import base64
from django.core.files.base import ContentFile

from studentApp.forms import LoginForm, SignUpForm, NotepadForm, ReminderForm, FileForms
from studentApp.models import Project, Note, Notepad, Reminder, Whiteboard, FileUploads




# Create your views here.
class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'studentApp/login.html', {'form':form})

    def post(self, request):
        form = LoginForm(request.POST)

        if form.is_valid():
            
            data = form.cleaned_data
            username = data['username']
            password = data['password']    
            user = authenticate(request, username=username,password=password)
            if user is not None:
                login(request, user)
                
                return HttpResponseRedirect( reverse("home"), )
               
        form.add_error("", "Username or password incorrect")
        return render(request, 'studentApp/login.html', {'form':form})
    
class SignUpView(View):
    def get(self, request):
        form = SignUpForm()
        return render(request, 'studentApp/signup.html', {"form":form})

    def post(self, request):
        form = SignUpForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            username = data['username']
            password = data['password']
            last_name = data['last_name']
            first_name = data['first_name']
            email = data['email']

            print(password)
            user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
            login(request, user)
            return HttpResponseRedirect(reverse("home"))
        
        return render(request, 'studentApp/signup.html', {"form":form})
    
class LogoutView(LoginRequiredMixin, View):
    def post(self, request):
        logout(
            request
        )
        return HttpResponseRedirect(reverse("login"))

class HomeView(LoginRequiredMixin, ListView):
    template_name='studentApp/home.html'
    context_object_name = 'projects'
    model = Project

    def get_queryset(self) -> QuerySet[Any]:
        data = Project.objects.filter(user = self.request.user)
        return data
    
    def post(self, request):
        data = request.POST
        if 'delete' in data:
            project_id = data['delete']
            Project.objects.get(pk=project_id).delete()

        return HttpResponseRedirect(reverse('home'))
    
class CreateNewProjectView(LoginRequiredMixin, CreateView):
    model = Project
    fields = ['name', 'description']

    template_name = 'studentApp/new_project.html'

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        # return super().post(request, *args, **kwargs)
        name = request.POST['name']
        desc = request.POST['description']
        project = Project.objects.create(user=request.user, name=name, description=desc)   
        return HttpResponseRedirect(reverse('home'))
        
class ProjectView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = 'studentApp/project.html'
    context_object_name = 'project'

class NoteView(LoginRequiredMixin, ListView):
    model = Note
    template_name = 'studentApp/notes.html'
    context_object_name = 'notes'

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        project_id_ = kwargs['project_id']
        data = Note.objects.filter(project_id=project_id_)
        return render(request, 'studentApp/notes.html', context={'notes_':data, "project_id_" : project_id_})
    
    def post(self, request, *args: Any, **kwargs: Any):
        
        project_id_ = kwargs['project_id']
        project = Project.objects.get(pk=project_id_)
        if 'delete' in request.POST:
            note_id = request.POST['delete']
            Note.objects.get(pk=note_id).delete()

        else:
            note = request.POST['note']
            note_ = Note.objects.create(project=project, text=note)
         
        return HttpResponseRedirect( reverse("notes", kwargs= {'project_id' : project_id_}))    
    
class NotepadView(LoginRequiredMixin, View):
    def get(self,request, **kwargs):
        project_id_ = kwargs['project_id']
        project = Project.objects.get(pk=project_id_)
        notepad = Notepad.objects.filter(project=project)
        if notepad:
            form = NotepadForm({'body' : notepad[0].body})
        else:
            form = NotepadForm()
        return render(request, 'studentApp/notepad.html', {'form':form, "project_id_" : project_id_})

    def post(self, request, **kwargs):
        project_id_ = kwargs['project_id']
        project = Project.objects.get(pk=project_id_)
        form = NotepadForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['body']
            notepad = Notepad.objects.get_or_create(project=project )[0]
            notepad.body = text
            notepad.save()
        
        return  HttpResponseRedirect( reverse('project', kwargs={'pk':project_id_}))

class ReminderView(LoginRequiredMixin, ListView):
    model = Reminder
    template_name = 'studentApp/reminder.html'
    context_object_name = 'reminder_'

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        project_id_ = kwargs['project_id']
        data = Reminder.objects.filter(project_id=project_id_)
        form = ReminderForm()
        return render(request, 'studentApp/reminder.html', context={'reminders_':data, "project_id_" : project_id_, 'form':form})
    
    def post(self, request, *args: Any, **kwargs: Any):
        
        project_id_ = kwargs['project_id']
        project = Project.objects.get(pk=project_id_)
        if 'delete' in request.POST:
            reminder_id = request.POST['delete']
            Reminder.objects.get(pk=reminder_id).delete()
        else:
            schedule = request.POST['schedule']
            text = request.POST['text']
            reminder_ = Reminder.objects.create(project=project, text=text, schedule=schedule)
         
        return HttpResponseRedirect( reverse("reminders", kwargs= {'project_id' : project_id_}))
    
class WhiteboardView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        project_id_ = kwargs['project_id']
        whiteboard = Whiteboard.objects.filter(project_id=project_id_).first()

        return render(request, 'studentApp/whiteboard.html', context={ "project_id_" : project_id_, "whiteboard":whiteboard})
    
    def post(self, request, *args: Any, **kwargs: Any):    
        project_id_ = kwargs['project_id']
        project = Project.objects.get(pk=project_id_)
        image_data = request.POST.get('image_data')

        format, imgstr = image_data.split(';base64,')
        ext = format.split('/')[-1]
        image_data = ContentFile(base64.b64decode(imgstr), name='whiteboard.' + ext)

        whiteboard = Whiteboard.objects.filter(project=project).first()
        if whiteboard:
            whiteboard.file.save(f'whiteboard{project_id_}.' + ext, image_data)
        else:
            whiteboard = Whiteboard.objects.create(project=project)
            whiteboard.file.save(f'whiteboard{project_id_}.' + ext, image_data)

        return  HttpResponseRedirect( reverse("whiteboard", kwargs={"project_id":project_id_}) ) 
        
class FileUploadView(LoginRequiredMixin, ListView):
    model = FileUploads
    template_name = 'studentApp/fileupload.html'
    context_object_name = 'files'

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        project_id_ = kwargs['project_id']
        data = FileUploads.objects.filter(project_id=project_id_)

        form = FileForms()
        return render(request, 'studentApp/fileupload.html', context={'files':data, "project_id_" : project_id_, 'form':form})
    
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:  
        project_id_ = kwargs['project_id']
        project = Project.objects.get(pk=project_id_)
        form = FileForms(request.POST, request.FILES)

        if form.is_valid():
            data = form.cleaned_data
            file_ = data['file']
            file = FileUploads.objects.create(project=project)
            file.file.save(file_.name, file_)
        return  HttpResponseRedirect( reverse("files", kwargs={"project_id":project_id_}) )
    
