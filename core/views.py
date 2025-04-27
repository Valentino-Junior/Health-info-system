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
