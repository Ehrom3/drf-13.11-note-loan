from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from rest_framework import serializers

from .models import NotesLoan

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'password2']
    
class RegisterSerializer(ModelSerializer):
    password = serializers.CharField(write_only = True)
    password2 = serializers.CharField(write_only = True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'password2']
        
    def validate(self, attrs):
        if attrs ["password"] != attrs["password2"]:
            raise ValueError("Password must be same")
        return attrs
        
    def create(self, validated_data):
        validated_data.pop("password2")
        return User.objects.create_user(**validated_data)
    
class NoteSerializer(ModelSerializer):
    class Meta:
        model = NotesLoan
        fields = ['full_name', 'description', 'phone', 'is_paid', 'price', 'created_at', 'user']
        