from django.shortcuts import render

# Create your views here.

from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import authentication,permissions

from django.contrib.auth.models import User
from todoapi.serializers import UserSerializer,TodoSerializer
from tasks.models import Todo


class UsersView(ModelViewSet): #list,create,retrieve,update,destroy implementations possible
    serializer_class=UserSerializer
    queryset=User.objects.all()
    model=User

    #method overiding: to mask the password
    # def create(self,request,*args,**kwargs):
    #     serializer=UserSerializer(data=request.data)
    #     if serializer.is_valid():
    #         # to hash password: create_user
    #         usr=User.objects.create_user(**serializer.validated_data) #**serializer.validated_data:to take data after serialization.
    #         serializer=UserSerializer(usr) #deserialization
    #         return Response(data=serializer.data)
    #     else:
    #         return Response(data=serializer.errors)


class TodosView(ModelViewSet):
    serializer_class=TodoSerializer
    queryset=Todo.objects.all()
    model=Todo
    #authentication_classes=[authentication.BasicAuthentication]
    authentication_classes=[authentication.TokenAuthentication]

    permission_classes=[permissions.IsAuthenticated] #credential passed users has only permission

# overiding create method: while saving the user value has tobe passed
    def create(self, request, *args, **kwargs):
        serializer=TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user) #passing the user value
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.data)
        
    
# overiding list method: to get only logined users todos
    # def list(self, request, *args, **kwargs):
    #     qs=Todo.objects.filter(user=request.user)
    #     serializer=TodoSerializer(qs,many=True)
    #     return Response(data=serializer.data)

# or by overiding get_queryset method: to get logginded users todos, both method works
    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)