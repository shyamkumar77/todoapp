from django.shortcuts import render,redirect
from django.views.generic import View

# Create your views here.
from django import forms
from crm.models import Employee
from django.contrib.auth.models import User  #importing User model
from django.contrib.auth.forms import UserCreationForm #importing the usercreation form
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages


# ModelForm creation
class EmployeeForm(forms.ModelForm):
    class Meta:
        model=Employee
        fields="__all__" #__all__:  for all fields      ["name","department",..]
        widgets={
            "name":forms.TextInput(attrs={"class":"form-control"}),
            "department":forms.TextInput(attrs={"class":"form-control"}),
            "gender":forms.Select(attrs={"class":"form-select"}),
            "salary":forms.NumberInput(attrs={"class":"form-control"}),
            "email":forms.EmailInput(attrs={"class":"form-control"}),
            "profile_pic":forms.FileInput(attrs={"class":"form-control"}),
            "address":forms.Textarea(attrs={"class":"form-control","rows":2})
        } #model form styling

# ##########################################################################################
# ##########################################################################################
#auth application:..............
# RegistrationForm creation, its model is bultin in auth aplication
class RegistrationForm(UserCreationForm):

    password1=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))
    password2=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    # password1 & password2 are athe attribute of UserCreationForm, not from the builtin  User model

    class Meta:
        model=User #builtin model
        fields=['first_name','last_name',"email","username","password1","password2"]
        widgets={
            "first_name":forms.TextInput(attrs={"class":"form-control"}),
            "last_name":forms.TextInput(attrs={"class":"form-control"}),
            "email":forms.EmailInput(attrs={"class":"form-control"}),
            "username":forms.TextInput(attrs={"class":"form-control"})
        } #styling the form


class SignUpView(View):
    def get(self,request,*args,**kwargs):
        form=RegistrationForm()
        return render(request,"register.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"account has been created succesfully")
            return redirect("signin")
        messages.error(request,"failed to create account")
        return render(request,"register.html",{"form":form})
    
#  loginform using norml form method
class LoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))

class SignInView(View):
    def get(self,request,*args,**kwargs):
        form=LoginForm()
        return render(request,"login.html",{"form":form})
    def post(self,request,*args,**kw):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username") #form.cleaned_data: bcoz used normal form mthod
            pwd=form.cleaned_data.get("password")
            usr=authenticate(request,username=uname,password=pwd)  #checking user valid or not
            if usr:
                login(request,usr) 
                messages.success(request,"successfully logged in")           
                return redirect("todo-list")
            messages.error(request,"invalid credential")
        return render(request,"login.html",{"form":form})
    
# function based view(fbv) for signout
def signout_view(request,*args,**kwargs):
    logout(request)
    return redirect("signin")


#  using class based view

# class SignOutView(View):
#     def get(self,request,*args,**kw):
#         logout(request)
#         return redirect("signin")
    



#######################################################################################
######################################################################################
#employee creation form
class EmployeeCreateView(View):
    def get(self,request,*args,**kwargs):
        form=EmployeeForm()
        return render(request,"emp-add.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=EmployeeForm(request.POST,files=request.FILES) #files=request.FILES --> to take image/file data's
        if form.is_valid():
            form.save()  #it will save to the database
            return redirect("emp-list")
        return render(request,"emp-add.html",{"form":form})

#list employees 
class EmployeeListView(View):
    def get(self,request,*args,**kwargs):
        qs=Employee.objects.all()
        return render(request,"employee-list.html",{"employees":qs})

#detail  
class EmployeeDetailView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Employee.objects.get(id=id)
        return render(request,"emp-detail.html",{"employee":qs})

# delete view
class EmployeeDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Employee.objects.filter(id=id).delete()
        return redirect("emp-list")
    
# edit/update view
class EmployeeEditView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        emp=Employee.objects.get(id=id)
        form=EmployeeForm(instance=emp)  #initializing with emp, to get values in form
        return render(request,"emp-edit.html",{"form":form})
    
    def post(self,request,*args,**kwargs):#updating the values using post
        id=kwargs.get("pk")
        emp=Employee.objects.get(id=id)
        form=EmployeeForm(data=request.POST,instance=emp,files=request.FILES) #files=request.FILES --> to take image/file data's
        if form.is_valid():
            form.save()
            return redirect("emp-detail",pk=id)#pk=id used to goto detail page 
        return render(request,"emp-edit.html",{"form":form})

#image upload and display
