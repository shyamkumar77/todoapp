from django.db import models

from django.contrib.auth.models import User

# Create your models here.

class Todo(models.Model):
    task_name=models.CharField(max_length=250)
    user=models.ForeignKey(User,on_delete=models.CASCADE)  #using user models object, on_delete=models.CASCADE, to delete todos created that user object
    status=models.BooleanField(default=False)
    date=models.DateTimeField(auto_now_add=True) #defaultly set date and time

    def __str__(self):
        return self.task_name
    
