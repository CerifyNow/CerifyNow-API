from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(DefaultUserAdmin):
    fieldsets = DefaultUserAdmin.fieldsets + (
        ('User Information', {'fields': ('role', 'full_name', 'phone_number', 'date_of_birth', 'profile_photo')}),
    )
    add_fieldsets = DefaultUserAdmin.add_fieldsets + (
        ('User Information', {'fields': ('role', 'full_name', 'phone_number', 'date_of_birth', 'profile_photo')}),
    )

    def has_module_permission(self, request):
        return request.user.is_authenticated and getattr(request.user, 'role', None) == 'superadmin'
    def has_view_permission(self, request, obj=None):
        return request.user.is_authenticated and getattr(request.user, 'role', None) == 'superadmin'
    def has_add_permission(self, request):
        return request.user.is_authenticated and getattr(request.user, 'role', None) == 'superadmin'
    def has_change_permission(self, request, obj=None):
        return request.user.is_authenticated and getattr(request.user, 'role', None) == 'superadmin'
    def has_delete_permission(self, request, obj=None):
        return request.user.is_authenticated and getattr(request.user, 'role', None) == 'superadmin'
