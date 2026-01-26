"""
Portal application models for role-based departmental data management.
"""
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator


class User(AbstractUser):
    """Extended user model with role and department information."""
    
    ROLE_CHOICES = [
        ('director', 'Director'),
        ('scientist', 'Scientist'),
        ('staff', 'Staff'),
    ]
    
    employee_id = models.CharField(max_length=50, unique=True)
    department = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    
    class Meta:
        db_table = 'auth_user'
        ordering = ['username']
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.role})"
    
    def has_permission(self, action, department=None, tab=None):
        """
        Check if user has permission to perform an action.
        Actions: 'view', 'add', 'edit', 'delete'
        """
        if self.role == 'director':
            return True
        elif self.role == 'scientist':
            # Scientists can do everything except delete
            return action != 'delete'
        elif self.role == 'staff':
            # Staff can only view and add
            return action in ['view', 'add']
        return False
    
    def can_manage_tabs(self):
        """Check if user can create, rename, or delete tabs."""
        return self.role in ['director', 'scientist']


class Department(models.Model):
    """Department model for organizing data."""
    
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_departments')
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Tab(models.Model):
    """
    Tab/Module model representing a data category within a department.
    """
    
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='tabs')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_tabs')
    
    class Meta:
        unique_together = ('department', 'name')
        ordering = ['name']
    
    def __str__(self):
        return f"{self.department.name} - {self.name}"


class Record(models.Model):
    """
    Record model for storing data entries within tabs.
    Uses JSONField to support flexible data structure.
    """
    
    tab = models.ForeignKey(Tab, on_delete=models.CASCADE, related_name='records')
    data = models.JSONField()  # Flexible data storage
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_records')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='updated_records')
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Record in {self.tab.name} ({self.id})"
