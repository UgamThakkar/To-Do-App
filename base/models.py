from django.db import models
from django.contrib.auth.models import User
# the user model by defualt has some tables built in for us and
#it takes care of the user information like username,email,password  
# Create your models here.
class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) #foreign key i.e. creating a one to many relationships where one user can have multiple items/tasks
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    create = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

    class Meta:
        ordering = ['complete']