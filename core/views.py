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


def client_update(request, pk):
    """View for updating client information"""
    client = get_object_or_404(Client, pk=pk)
    
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            client = form.save()
            messages.success(request, f"Client '{client.full_name}' updated successfully!")
            return redirect('client_detail', pk=client.id)
    else:
        form = ClientForm(instance=client)
    
    context = {'form': form, 'client': client, 'title': 'Update Client Information'}
    return render(request, 'client/form.html', context)


# Enrollment Views
def enroll_client(request, client_id):
    """View for enrolling a client in one or more programs"""
    client = get_object_or_404(Client, pk=client_id)
    
    if request.method == 'POST':
        form = MultiEnrollmentForm(request.POST)
        if form.is_valid():
            programs = form.cleaned_data['programs']
            enrollment_date = form.cleaned_data['enrollment_date']
            notes = form.cleaned_data['notes']
            
            # Create enrollments for each selected program
            enrollment_count = 0
            for program in programs:
                # Check if enrollment already exists
                enrollment, created = Enrollment.objects.update_or_create(
                    client=client,
                    program=program,
                    defaults={
                        'enrollment_date': enrollment_date,
                        'notes': notes,
                        'is_active': True
                    }
                )
                if created:
                    enrollment_count += 1
            
            if enrollment_count > 0:
                messages.success(request, f"Client enrolled in {enrollment_count} program(s) successfully!")
            else:
                messages.info(request, "Client was already enrolled in the selected programs. Enrollments were updated.")
            
            return redirect('client_detail', pk=client.id)
    else:
        # Get programs the client is not yet enrolled in
        enrolled_program_ids = Enrollment.objects.filter(client=client).values_list('program_id', flat=True)
        available_programs = HealthProgram.objects.exclude(id__in=enrolled_program_ids)
        
        form = MultiEnrollmentForm()
        form.fields['programs'].queryset = available_programs
        form.fields['enrollment_date'].initial = timezone.now().date()
    
    context = {
        'form': form,
        'client': client,
        'title': f'Enroll {client.full_name} in Programs'
    }
    return render(request, 'client/enroll.html', context)



def update_enrollment(request, enrollment_id):
    """View for updating a client's enrollment in a program"""
    enrollment = get_object_or_404(Enrollment, pk=enrollment_id)
    client = enrollment.client
    
    if request.method == 'POST':
        form = EnrollmentForm(request.POST, instance=enrollment)
        if form.is_valid():
            enrollment = form.save()
            messages.success(request, f"Enrollment updated successfully!")
            return redirect('client_detail', pk=client.id)
    else:
        form = EnrollmentForm(instance=enrollment)
    
    context = {
        'form': form,
        'enrollment': enrollment,
        'client': client,
        'title': f'Update Enrollment for {client.full_name}'
    }
    return render(request, 'client/update_enrollment.html', context)



def enrollment_list(request):
    """View for listing all enrollments in the system with chart data"""
    from django.db.models import Count
    from django.db.models.functions import TruncMonth
    
    # Get all enrollments
    enrollments = Enrollment.objects.all().select_related('client', 'program').order_by('-enrollment_date')
    
    # Data for Program Distribution Chart
    program_stats = HealthProgram.objects.annotate(
        count=Count('enrollment')
    ).values('name', 'count').order_by('-count')
    
    # Data for Enrollment Timeline Chart - past 12 months
    from datetime import datetime, timedelta
    import calendar
    
    # Get enrollments for the past 12 months
    today = datetime.now().date()
    twelve_months_ago = today - timedelta(days=365)
    
    # Get counts per month
    enrollment_by_month = Enrollment.objects.filter(
        enrollment_date__gte=twelve_months_ago
    ).annotate(
        month=TruncMonth('enrollment_date')
    ).values('month').annotate(
        count=Count('id')
    ).order_by('month')
    
    # Process the data for the chart
    timeline_stats = []
    for item in enrollment_by_month:
        month_name = calendar.month_name[item['month'].month]
        year = item['month'].year
        timeline_stats.append({
            'month': f"{month_name} {year}",
            'count': item['count']
        })
    
    # If there's no data for some months, fill with zeros
    if len(timeline_stats) < 12:
        # Generate all months for the past year
        all_months = []
        for i in range(12):
            month_date = today.replace(day=1) - timedelta(days=30*i)
            month_name = calendar.month_name[month_date.month]
            year = month_date.year
            all_months.append(f"{month_name} {year}")
        
        # Create a dict for easy lookup
        existing_data = {item['month']: item['count'] for item in timeline_stats}
        
        # Create the final timeline stats with all months
        timeline_stats = []
        for month in reversed(all_months):
            timeline_stats.append({
                'month': month,
                'count': existing_data.get(month, 0)
            })
    
    context = {
        'enrollments': enrollments,
        'total_enrollments': enrollments.count(),
        'program_stats': program_stats,
        'timeline_stats': timeline_stats,
        'title': 'All Enrollments'
    }
    return render(request, 'enrollment/list.html', context)


def direct_enrollment(request):
    """View for enrolling any client in programs directly"""
    from django.utils import timezone
    
    # For GET request, initialize empty forms
    if request.method == 'GET':
        # Get all clients and programs for selection
        clients = Client.objects.all().order_by('last_name', 'first_name')
        programs = HealthProgram.objects.all().order_by('name')
        
        context = {
            'clients': clients,
            'programs': programs,
            'today': timezone.now(),
            'title': 'Quick Enrollment'
        }
        return render(request, 'enrollment/direct_enrollment.html', context)
    
    # For POST request, process the enrollment
    elif request.method == 'POST':
        client_id = request.POST.get('client')
        program_ids = request.POST.getlist('programs')
        enrollment_date = request.POST.get('enrollment_date')
        notes = request.POST.get('notes')
        
        if not client_id or not program_ids or not enrollment_date:
            messages.error(request, "Please select a client, at least one program, and an enrollment date.")
            return redirect('direct_enrollment')
        
        try:
            client = Client.objects.get(pk=client_id)
            enrollment_count = 0
            
            for program_id in program_ids:
                program = HealthProgram.objects.get(pk=program_id)
                
                # Create or update enrollment
                enrollment, created = Enrollment.objects.update_or_create(
                    client=client,
                    program=program,
                    defaults={
                        'enrollment_date': enrollment_date,
                        'notes': notes,
                        'is_active': True
                    }
                )
                
                if created:
                    enrollment_count += 1
            
            if enrollment_count > 0:
                messages.success(request, f"{client.full_name} enrolled in {enrollment_count} program(s) successfully!")
            else:
                messages.info(request, "Client was already enrolled in the selected programs. Enrollments were updated.")
            
            return redirect('enrollment_list')
            
        except (Client.DoesNotExist, HealthProgram.DoesNotExist) as e:
            messages.error(request, f"Error: {str(e)}")
            return redirect('direct_enrollment')