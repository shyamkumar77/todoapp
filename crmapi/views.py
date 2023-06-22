from django.shortcuts import render

from rest_framework.viewsets import ViewSet,ModelViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework import authentication,permissions


from crm.models import Employee

# Create your views here.

# serializer
class EmployeeSerializers(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True) #to get id while reading, not required while writing data in thunder client
    class Meta:
        model=Employee
        fields="__all__"
        #exclude=("id", )



class EmployeesView(ViewSet):

    def list(self,request,*args,**kwargs):
        # localhost:8000/api/employees/
        # method get
        qs=Employee.objects.all()

    #  query parameter
        if "department" in request.query_params:
            dept=request.query_params.get("department")
            qs=qs.filter(department__iexact=dept) #__iexact: used to solve case sensitive issue

        if "salary" in request.query_params: #request.query_params --> the dictionary name
            sal=request.query_params.get("salary")
            qs=qs.filter(salary=sal)

    # salary greater than
        if "salary_gt" in request.query_params:
            sal=request.query_params.get("salary_gt")
            qs=qs.filter(salary__gt=sal)

        # deserialization
        # syntax: varname=SerializerName(qs)
        serializer=EmployeeSerializers(qs,many=True)  #many=True, use if more than one object in the queryset
        return Response(data=serializer.data)
    
                                        
    def create(self,request,*args,**kwargs):
        # localhost:8000/api/
        # method post
        serializer=EmployeeSerializers(data=request.data) #to take data
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
    
    
    def retrieve(self,request,*args,**kwargs): 
        # localhost:8000/api/employees/id/
        # method get
        id=kwargs.get("pk")
        qs=Employee.objects.get(id=id)
        # deserializing
        serializer=EmployeeSerializers(qs,many=False)
        return Response(data=serializer.data)
    
    def update(self,request,*args,**kwargs):
        # localhost:8000/api/employees/id/
        # method put
        id=kwargs.get("pk")
        emp_obj=Employee.objects.get(id=id)
        serializer=EmployeeSerializers(instance=emp_obj,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        
    
    def destroy(self,request,*args,**kwargs):
        # localhost:8000/api/employees/id/
        # method delete
        id=kwargs.get("pk")
        try:
            Employee.objects.get(id=id).delete()
            return Response(data="deleted")
        except Exception:
            return Response(data="no matching record found")
        

# custom method: to get department
    @action(methods=["get"],detail=False)
    def departments(self,request,*args,**kwargs):
        qs=Employee.objects.all().values_list("department",flat=True).distinct()
        return Response(data=qs) #no need to desserialize
        

# to get department values
# open the shell then import model
# dept=Employee.objects.all().values_list("department",flat=True).distinct()

###################################################################################################################
###################################################################################################################


# ModelViewSet --> contain implementation of all the methods of viewset

class EmployeeViewsetView(ModelViewSet):
    serializer_class=EmployeeSerializers
    model=Employee
    queryset=Employee.objects.all()
    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAdminUser] #so createdsuperuser

   

