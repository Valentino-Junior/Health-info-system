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