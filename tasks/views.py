from django.shortcuts import render,redirect
from django.views.generic import View

# import model
from tasks.models import Todo
from django.contrib import messages

# Create your views here.

from django import forms
# form creation
class TodoForm(forms.Form):
    task_name=forms.CharField()
    #user=forms.CharField()

# get implementation
class TodoCreateView(View):
    def get(self,request,*args,**kwargs):
        form=TodoForm()
        return render(request,"todo-add.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=TodoForm(request.POST)
        if form.is_valid():
            #print(form.cleaned_data)
            Todo.objects.create(**form.cleaned_data,user=request.user) #the data gets added to the model(Todo) , user=request.user -> to get loggedin user
            messages.success(request,"todo has been created successfully") #messages: [success,error,warning,info]
            return redirect("todo-list") 
        messages.error(request,"failed to create todo")
        return render(request,"todo-add.html")

#Listview   
class TodoListView(View):
    def get(self,request,*args,**kwargs):
        qs=Todo.objects.filter(status=False,user=request.user).order_by("-date") #status=False--> to list  the false todos #order_by() to list in date by descending order
        #user=request.user --> to list only the loggined user
        return render(request,"todo-list.html",{"todos":qs})
    
# Detailview
class TodoDetailView(View):
    def get(self,request,*args,**kwargs):
        print(kwargs)  #kwargs contains the id/value
        id=kwargs.get("pk")  #in 'kwargs' dictionary the id is present
        qs=Todo.objects.get(id=id) #now we need to take to todo with this id(second one)
        return render(request,"todo-detail.html",{"todo":qs})
    
# Delete View: its url-->localhost:8000/todos/id/remove/
class TodoDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk") #extracting the id from url
        Todo.objects.get(id=id).delete() 
        messages.success(request,"todo has been removed succesfully")
        return redirect("todo-list")

#updating the status=True, when clicking mark as done
class TaskEditView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Todo.objects.filter(id=id).update(status=True)
        messages.success(request,"todo has been changed successsfully")
        return redirect("todo-list")

#  the completed todos
class TodoCompletedView(View):
    def get(self,request,*args,**kwargs):
        qs=Todo.objects.filter(status=True)
        return render(request,"todo-completed.html",{"todos":qs})

        


