from rest_framework import serializers
from .models import Client, HealthProgram, Enrollment


class HealthProgramSerializer(serializers.ModelSerializer):
    """Serializer for the HealthProgram model"""
    class Meta:
        model = HealthProgram
        fields = ['id', 'name', 'description', 'created_at', 'updated_at']
