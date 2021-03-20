from django.urls import path
from .views import TaskList,  TaskDetail, TaskCreate, TaskUpdate, DeleteView, CustomLoginView, RegisterPage

from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name = 'login'),    
    path('logout/', LogoutView.as_view(next_page='login'), name = 'logout'),    #here what next_page argument does is that if a user logs out of our website then it will redirect them to the next page i.e. login page
    path('register/', RegisterPage.as_view(), name = 'register'),    

    path('', TaskList.as_view(), name = 'tasks'),
    path('task/<int:pk>/', TaskDetail.as_view(), name = 'task'),
    path('task-create/', TaskCreate.as_view(), name = 'task-create'),    #I think that for class based views the url we are passing in the path function here that url name should match with the 'name' argument provided at the end of the function here because otherwise im facing an error of  Reverse for 'task_detail' not found. 'task_detail' is not a valid view function or pattern name #something like this and if the url name for eg here task-create/ and the name argument has same values then the error is not produced so i need to look up why is that happening
    path('task-update/<int:pk>/', TaskUpdate.as_view(), name ='task-update'),
    path('task-delete/<int:pk>/', DeleteView.as_view(), name ='task-delete'),

]