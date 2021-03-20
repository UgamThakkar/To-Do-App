from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView

from django.contrib.auth.mixins import LoginRequiredMixin #this will help us to restrict the anonymous user from accessing the main page of our website first he needs to create an account then hell be redirected to the main page of our site
#adding this loginreqmixin to all our classes because we have links to all these classes in our urls.py so in order to restrict the user from directly accessing any page we will pass it as the first parameter to our class and so it will restrict the user from doing anything if hes not logged in
from django.contrib.auth.forms import UserCreationForm #this is a built in form as soon as we submit it, it will create a user for us
from django.contrib.auth import login

from .models import Task

# Create your views here.


class CustomLoginView(LoginView):
    template_name = 'base/login.html'

#by defualt the loginview provides us with a form 
    fields = '__all__'

#redirect authenticated user is built in attribute of login view and it will prevent already logged in user to go to this page bcoz hes already logged in
    redirect_authenticated_user = True

    def get_success_url(self): #what this function does is that if a user is already logged in it will directly take him to the tasks page where all his tasks are saved
        return reverse_lazy('tasks')


class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)

class TaskList(LoginRequiredMixin, ListView): 
    
    #passing the loginreqmixin first here means that first check if the user is logged in or not if yes then show him the task_list.html page otherwise restrict him from going to that page # so we passed the LOGIN_URL in settings.py and it means that if the user is not logged in then the LOGIN_URL = 'login' will guide him to the login page rather then showing any kind of error page to the user
    
    
    #which model and its attributes we want to use its name is passed here to the var model
    model = Task
    
    #by default the listview class looks for a template of name 'modelname as prefix(aapda model nu naam pehla, here=task)suffix is '_list' so here the template it looks for is task_list.html
    # we dont need to pass in return render(request, base/...html) all this it is done by the class
    #template_name = 'base/task.html'
    # now if we want to change the name of our template from default task_list.html then we can use template_name property and pass the folder and changed template name of the org template(task_list.html)
    
    
    #by default if we want to access the objects of our model we use to get them using the query Customer.objects.all() or something like that but here using list view class what it does is that we dont need to pass any statement like 
    #Customer.objects.all() to get all the customers/objects of our customer model listview does that automatically for us but it has a specific name and that is object_list so in this example our task model objects are by defualt present in the object_list 
    #now if we want to change the name of the queryset where all our objects reside for specific model i.e.
    #object_list ma aapda model 'Task' na objects che to aapde aa queryset i.e. object_list nu naam change karvu hoy and biju kai karvu hoy to aavi rite thase
    context_object_name = 'tasks'
    #context_obj_name and providing the name of the queryset will change it from 'object_list' to 'tasks' and all our objects of model 'Task' will be contained in it

    #now as we are going to have multiple users using our website we dont want that one user can see the tasks or list of another user and in oorder to achieve that we will override the get_context_data() method 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user) # our objects are present in the tasks queryset which we set above so now we are filtering those objects depdening upon the user and passing it to this context['tasks']
        context['count'] = context['tasks'].filter(complete=False).count() #what this does is it counts the task which arent completed yet and displays them first
        
        #logic for searching among our tasks
        #here we are taking whatever is passed in the 'search-area' field of our form on task_list.html we will store it in the var
        search_input = self.request.GET.get('search-area') 
        
        #now if there is something present in our search bar i.e. if user searched something then it will trigger this if condition
        if search_input:
            #using whatever user wants to search we need to modify our queryset according to that return the filtered data back to the user
            context['tasks'] = context['tasks'].filter(title__icontains=search_input)
            #using this we are filtering our objects present in the queryset 'tasks' by passsing our search_input var to the title cuz we can search using the title and then we can return the result in the form of filtered tasks
            #what is happening here is if we search something it brings us that result but we stay there only it does not take us back to our tasks page if we remove our search data so in ordere to do that below is the logic
        
        #what this will do is if we searched something and then if we remove that from our search bar then it will bring back to us all our tasks 
        context['search_input'] = search_input
        
        return context


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task

    # so here I renamed my task_detail.html file to task.html and changed my queryset of objects which by defualt for class DetailView is named as 'objects' where all the objects of our model 'Task' are present and we renmaed it to 'task'
    template_name='base/task.html'  
    context_object_name = 'task'

class TaskCreate(LoginRequiredMixin, CreateView):
#also by default the create view looks/Searches for a template named modelame_form.html so here it is task_form.html and the updateview used below also looks for the same template 
#by defualt the createview class creates it for us and provides us with a modelform, modelform is just the a simple form for the model we pass in the var model below
    model = Task

# the fields we want to output from our model form is provided here and if we want to output some specific fields we can give it like fields = ['title', 'description'] so this way it will render these specific fields in our model form 
# but as we want to have all the fields of our model 'Task' here we are using '__all__' which will use all the attributes/fields of our model 'Task' and render it in our modelform    
    fields = ['title', 'description', 'complete']

#now what does these guys do is that if everything goes well then this success_url will redirect the user automatically to the url passed into the reverse_lazy function    
#this is kind of redirect of function based views
    success_url = reverse_lazy('tasks') 

    def form_valid(self, form): #so form valid is a inbuilt method of createview class and the reason we are using it here is because we dont if a user creates tasks for himself reflecting in the tasks of other user, user should be able to add tasks for himself only and not for any other user
        #we are also using this form so that a user can add task for himself and he shouldnt get a drop down list with names of users where he can add task to anyones account choosing their name from the drop down list
        #so it mens by default we want the task to be added to the currently logged in user and this will do that for us
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)  


class TaskUpdate(LoginRequiredMixin,UpdateView): #the updatevies is use to modify or update the data whereas the create view used above is used to fill out a form or create data
#also by default the update view looks/Searches for a template named modelame_form.html so here it is task_form.html and it will return updated values if any 
    model= Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')


class DeleteView(LoginRequiredMixin,DeleteView):
#delete view is kind of a conformation page it does two things: renders out a page that says are u sure u wanna del this item and secondly when we say yes it sends a post request and deletes that item for us
    model = Task
#by default deleteview looks for a template called modelname_confirm_delete.html so here it is task_confirm_delete.html

#by default our objects are present in the queryset here called as objects and so we are changing its name to 'task' using contextobjectname which will now have all our objects as querysets
    context_object_name = 'task'

    success_url = reverse_lazy('tasks')

