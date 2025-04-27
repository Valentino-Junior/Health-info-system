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