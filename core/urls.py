from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    

    # Health Program URLs
    path('programs/', views.program_list, name='program_list'),
    path('programs/<uuid:pk>/', views.program_detail, name='program_detail'),
    path('programs/create/', views.program_create, name='program_create'),
    path('programs/<uuid:pk>/update/', views.program_update, name='program_update'),


    # Client URLs
    path('clients/', views.client_list, name='client_list'),
    path('clients/<uuid:pk>/', views.client_detail, name='client_detail'),
    path('clients/create/', views.client_create, name='client_create'),
    path('clients/<uuid:pk>/update/', views.client_update, name='client_update'),


     # Enrollment URLs
    path('clients/<uuid:client_id>/enroll/', views.enroll_client, name='enroll_client'),
    path('enrollments/<uuid:enrollment_id>/update/', views.update_enrollment, name='update_enrollment'),
    path('enrollments/', views.enrollment_list, name='enrollment_list'),
]