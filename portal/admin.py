"""Portal admin configuration."""
from django.contrib import admin
from .models import User, Department, Tab, Record


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'employee_id', 'department', 'role')
    list_filter = ('role', 'department')
    search_fields = ('username', 'email', 'employee_id')
    fieldsets = (
        ('Personal Info', {'fields': ('username', 'first_name', 'last_name', 'email')}),
        ('Employee Info', {'fields': ('employee_id', 'department', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('name',)


@admin.register(Tab)
class TabAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'created_by', 'created_at')
    list_filter = ('department', 'created_at')
    search_fields = ('name', 'department__name')


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'tab', 'created_by', 'created_at')
    list_filter = ('tab', 'created_at')
    search_fields = ('tab__name',)
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by')
