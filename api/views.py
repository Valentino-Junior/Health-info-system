from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404

from core.models import Client, HealthProgram, Enrollment
from core.serializers import ClientSerializer, ClientDetailSerializer, HealthProgramSerializer, EnrollmentSerializer


class ClientViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for viewing clients.
    Provides:
    - List all clients with filtering
    - Retrieve a specific client with their program enrollments
    """
    queryset = Client.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['gender']
    search_fields = ['first_name', 'last_name', 'national_id', 'phone_number', 'email']
    ordering_fields = ['created_at', 'last_name', 'first_name']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ClientDetailSerializer
        return ClientSerializer
    
    @action(detail=True, methods=['get'])
    def enrollments(self, request, pk=None):
        """
        Returns all program enrollments for a specific client
        """
        client = self.get_object()
        enrollments = Enrollment.objects.filter(client=client).select_related('program')
        serializer = EnrollmentSerializer(enrollments, many=True)
        return Response(serializer.data)
