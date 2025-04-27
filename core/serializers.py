from rest_framework import serializers
from .models import Client, HealthProgram, Enrollment


class HealthProgramSerializer(serializers.ModelSerializer):
    """Serializer for the HealthProgram model"""
    class Meta:
        model = HealthProgram
        fields = ['id', 'name', 'description', 'created_at', 'updated_at']


class EnrollmentSerializer(serializers.ModelSerializer):
    """Serializer for the Enrollment model with program details"""
    program = HealthProgramSerializer(read_only=True)
    
    class Meta:
        model = Enrollment
        fields = ['id', 'program', 'enrollment_date', 'is_active', 'notes', 'created_at', 'updated_at']


class ClientSerializer(serializers.ModelSerializer):
    """Serializer for the Client model"""
    age = serializers.IntegerField(read_only=True)
    full_name = serializers.CharField(read_only=True)
    
    class Meta:
        model = Client
        fields = [
            'id', 'first_name', 'last_name', 'full_name', 'date_of_birth', 
            'age', 'gender', 'phone_number', 'email', 'address', 
            'national_id', 'created_at', 'updated_at'
        ]