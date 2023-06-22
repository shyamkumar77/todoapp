from rest_framework import serializers
from django.contrib.auth.models import User 
from tasks.models import Todo


# Using Modelserializer: fields are automatically populated
# create(), update() method possible

# userserializer: for creating a user
class UserSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)

    class Meta:
        model=User
        fields=["id","username","email","password"]

    # method overiding: to hash the password
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)  #ORM query to hash psswd
    

# For creating todos
class TodoSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    date=serializers.CharField(read_only=True)
    user=serializers.CharField(read_only=True)
    status=serializers.CharField(read_only=True)
    
    class Meta:
        model=Todo
        fields="__all__"



