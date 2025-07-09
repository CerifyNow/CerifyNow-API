from django.contrib import admin
from .models import Institution, Certificate

@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at', 'is_approved')
    search_fields = ('name', )
    list_filter = ('is_approved', 'created_at')
    ordering = ('-created_at',)

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('id', 'student__full_name', 'institution', 'issued_date', 'is_verified')
    search_fields = ('serial_number', 'student__full_name', 'institution__name')
    list_filter = ('is_verified', 'institution', 'issued_date')
    ordering = ('-issued_date',)