from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone

from .models import *
from .forms import *


def dashboard(request):
    """View for the dashboard showing system overview"""
    total_clients = Client.objects.count()
    total_programs = HealthProgram.objects.count()
    total_enrollments = Enrollment.objects.count()
    
    recent_clients = Client.objects.order_by('-created_at')[:5]
    recent_programs = HealthProgram.objects.order_by('-created_at')[:5]
    
    context = {
        'total_clients': total_clients,
        'total_programs': total_programs,
        'total_enrollments': total_enrollments,
        'recent_clients': recent_clients,
        'recent_programs': recent_programs,
    }
    return render(request, 'dashboard.html', context)


# Health Program Views
def program_list(request):
    """View for listing all health programs"""
    programs = HealthProgram.objects.all()
    context = {'programs': programs}
    return render(request, 'program/list.html', context)


def program_detail(request, pk):
    """View for displaying details of a specific health program"""
    program = get_object_or_404(HealthProgram, pk=pk)
    enrollments = Enrollment.objects.filter(program=program).select_related('client')
    
    context = {
        'program': program,
        'enrollments': enrollments
    }
    return render(request, 'program/detail.html', context)


def program_create(request):
    """View for creating a new health program"""
    if request.method == 'POST':
        form = HealthProgramForm(request.POST)
        if form.is_valid():
            program = form.save()
            messages.success(request, f"Health program '{program.name}' created successfully!")
            return redirect('program_detail', pk=program.id)
    else:
        form = HealthProgramForm()
    
    context = {'form': form, 'title': 'Create Health Program'}
    return render(request, 'program/form.html', context)


def program_update(request, pk):
    """View for updating an existing health program"""
    program = get_object_or_404(HealthProgram, pk=pk)
    
    if request.method == 'POST':
        form = HealthProgramForm(request.POST, instance=program)
        if form.is_valid():
            program = form.save()
            messages.success(request, f"Health program '{program.name}' updated successfully!")
            return redirect('program_detail', pk=program.id)
    else:
        form = HealthProgramForm(instance=program)
    
    context = {'form': form, 'program': program, 'title': 'Update Health Program'}
    return render(request, 'program/form.html', context)


# Client Views
def client_list(request):
    """View for listing and searching clients"""
    form = ClientSearchForm(request.GET)
    clients = Client.objects.all()
    
    # Search functionality
    if form.is_valid() and form.cleaned_data['search']:
        search_query = form.cleaned_data['search']
        clients = clients.filter(
            Q(first_name__icontains=search_query) | 
            Q(last_name__icontains=search_query) | 
            Q(national_id__icontains=search_query) |
            Q(phone_number__icontains=search_query)
        )
    
    context = {'clients': clients, 'form': form}
    return render(request, 'client/list.html', context)


def client_detail(request, pk):
    """View for displaying a client's profile including enrolled programs"""
    client = get_object_or_404(Client, pk=pk)
    enrollments = Enrollment.objects.filter(client=client).select_related('program')
    
    context = {
        'client': client,
        'enrollments': enrollments
    }
    return render(request, 'client/detail.html', context)


def client_create(request):
    """View for registering a new client"""
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save()
            messages.success(request, f"Client '{client.full_name}' registered successfully!")
            return redirect('client_detail', pk=client.id)
    else:
        form = ClientForm()
    
    context = {'form': form, 'title': 'Register New Client'}
    return render(request, 'client/form.html', context)