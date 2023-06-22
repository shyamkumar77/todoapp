from django.db import models

# Create your models here.

class Employee(models.Model):
    name=models.CharField(max_length=250)
    department=models.CharField(max_length=200)
    options=(
        ("male","male"),
        ("female","female")
    )  #passing as nested tuple: (male,male) one for display and other as button
    gender=models.CharField(max_length=250,choices=options,default="male") #gave choices attribute
    salary=models.PositiveIntegerField()
    email=models.EmailField()
    profile_pic=models.ImageField(upload_to="images",null=True,blank=True) #uploading images store in "images" folder
    #null=True means: database can accept null value, blank=True means: form can accept blank(ie, we can submit without adding image)
    address=models.CharField(max_length=250)

    def __str__(self):
        return self.name