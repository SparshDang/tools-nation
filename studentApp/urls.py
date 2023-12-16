from django.urls import path

from studentApp.views import LoginView, SignUpView, HomeView, CreateNewProjectView, ProjectView, NoteView, NotepadView, ReminderView, WhiteboardView, LogoutView, FileUploadView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', HomeView.as_view(), name='home'),
    path('create/', CreateNewProjectView.as_view(), name='new_project'),
    path('project/<int:pk>', ProjectView.as_view(), name='project'),
    path('project/<int:project_id>/notes', NoteView.as_view(), name='notes'),
    path('project/<int:project_id>/reminders', ReminderView.as_view(), name='reminders'),
    path('project/<int:project_id>/notepad', NotepadView.as_view(), name='notepad'),
    path('project/<int:project_id>/whiteboard', WhiteboardView.as_view(), name='whiteboard'),
    path('project/<int:project_id>/fileupload', FileUploadView.as_view(), name='files')
]
