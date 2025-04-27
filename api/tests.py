from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from datetime import date
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User

from core.models import Client, HealthProgram, Enrollment


class APIEndpointsTestCase(APITestCase):
    """Test cases for API endpoints"""
    
    def setUp(self):
        """Set up test data and authentication"""
        # Create a user for authentication
        self.user = User.objects.create_user(
            username='apiuser',
            password='api12345'
        )
        
        # Create health programs
        self.program1 = HealthProgram.objects.create(
            name="TB Program",
            description="Tuberculosis Treatment Program"
        )
        
        self.program2 = HealthProgram.objects.create(
            name="Malaria Program",
            description="Malaria Prevention Program"
        )
        
        # Create clients
        self.client1 = Client.objects.create(
            first_name="John",
            last_name="Doe",
            date_of_birth=date(1990, 1, 15),
            gender="M",
            phone_number="1234567890",
            email="john.doe@example.com",
            address="123 Main St",
            national_id="ID12345"
        )
        
        self.client2 = Client.objects.create(
            first_name="Jane",
            last_name="Smith",
            date_of_birth=date(1985, 5, 20),
            gender="F",
            phone_number="9876543210",
            email="jane.smith@example.com",
            address="456 Oak Ave",
            national_id="ID67890"
        )
        
        # Create enrollments
        self.enrollment1 = Enrollment.objects.create(
            client=self.client1,
            program=self.program1,
            enrollment_date=timezone.now().date(),
            notes="API test enrollment 1",
            is_active=True
        )
        
        self.enrollment2 = Enrollment.objects.create(
            client=self.client2,
            program=self.program1,
            enrollment_date=timezone.now().date(),
            notes="API test enrollment 2",
            is_active=True
        )
        
        self.enrollment3 = Enrollment.objects.create(
            client=self.client1,
            program=self.program2,
            enrollment_date=timezone.now().date(),
            notes="API test enrollment 3",
            is_active=False
        )
        
        # Authenticate
        self.client.force_authenticate(user=self.user)
    
    def test_client_list_api(self):
        """Test GET /api/clients/ endpoint"""
        url = reverse('client-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        
        # Test search functionality
        response = self.client.get(f"{url}?search=John")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['first_name'], 'John')
        
        # Test filtering
        response = self.client.get(f"{url}?gender=F")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['first_name'], 'Jane')
        
        # Test ordering
        response = self.client.get(f"{url}?ordering=first_name")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['first_name'], 'Jane')
        self.assertEqual(response.data['results'][1]['first_name'], 'John')
    
    def test_client_detail_api(self):
        """Test GET /api/clients/{id}/ endpoint"""
        url = reverse('client-detail', kwargs={'pk': self.client1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'John')
        self.assertEqual(response.data['last_name'], 'Doe')
        self.assertEqual(response.data['full_name'], 'John Doe')
        
        # Test enrollments are included in detail view
        self.assertEqual(len(response.data['enrollments']), 2)
        
        # Test non-existent client
        url = reverse('client-detail', kwargs={'pk': '00000000-0000-0000-0000-000000000000'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_program_list_api(self):
        """Test GET /api/programs/ endpoint"""
        url = reverse('healthprogram-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        
        # Test search functionality
        response = self.client.get(f"{url}?search=TB")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['name'], 'TB Program')
    
    def test_program_detail_api(self):
        """Test GET /api/programs/{id}/ endpoint"""
        url = reverse('healthprogram-detail', kwargs={'pk': self.program1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'TB Program')
        self.assertEqual(response.data['description'], 'Tuberculosis Treatment Program')
    
    def test_client_enrollments_api(self):
        """Test GET /api/clients/{id}/enrollments/ endpoint"""
        url = reverse('client-enrollments', kwargs={'pk': self.client1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        
        # Verify both TB and Malaria programs are included
        program_names = [enrollment['program']['name'] for enrollment in response.data]
        self.assertIn('TB Program', program_names)
        self.assertIn('Malaria Program', program_names)
        
        # Check active status filtering
        active_enrollments = [e for e in response.data if e['is_active']]
        inactive_enrollments = [e for e in response.data if not e['is_active']]
        self.assertEqual(len(active_enrollments), 1)
        self.assertEqual(len(inactive_enrollments), 1)
    
    def test_program_clients_api(self):
        """Test GET /api/programs/{id}/clients/ endpoint"""
        url = reverse('healthprogram-clients', kwargs={'pk': self.program1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        
        # Check both clients are included
        client_names = [client['full_name'] for client in response.data]
        self.assertIn('John Doe', client_names)
        self.assertIn('Jane Smith', client_names)
    
   