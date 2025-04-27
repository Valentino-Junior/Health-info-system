from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Client, HealthProgram, Enrollment


@admin.register(HealthProgram)
class HealthProgramAdmin(admin.ModelAdmin):
    """Admin configuration for HealthProgram model"""
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at',)
    readonly_fields = ('id', 'created_at', 'updated_at')
    fieldsets = (
        ('Program Details', {
            'fields': ('id', 'name', 'description')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    """Admin configuration for Client model"""
    list_display = ('full_name', 'national_id', 'gender', 'age', 'phone_number', 'created_at')
    search_fields = ('first_name', 'last_name', 'national_id', 'phone_number', 'email')
    list_filter = ('gender', 'created_at')
    readonly_fields = ('id', 'created_at', 'updated_at', 'age')
    fieldsets = (
        ('Personal Information', {
            'fields': ('id', 'first_name', 'last_name', 'date_of_birth', 'age', 'gender', 'national_id')
        }),
        ('Contact Information', {
            'fields': ('phone_number', 'email', 'address')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def full_name(self, obj):
        return obj.full_name
    
    full_name.short_description = 'Full Name'


class EnrollmentInline(admin.TabularInline):
    """Inline admin for Enrollments"""
    model = Enrollment
    extra = 1
    readonly_fields = ('id', 'created_at', 'updated_at')


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    """Admin configuration for Enrollment model"""
    list_display = ('client', 'program', 'enrollment_date', 'is_active', 'created_at')
    list_filter = ('is_active', 'enrollment_date', 'program')
    search_fields = ('client__first_name', 'client__last_name', 'program__name')
    readonly_fields = ('id', 'created_at', 'updated_at')
    fieldsets = (
        ('Enrollment Details', {
            'fields': ('id', 'client', 'program', 'enrollment_date', 'is_active', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    # Add more efficient database queries
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('client', 'program')


# Add enrollment inline to Client admin
ClientAdmin.inlines = [EnrollmentInline]