"""
Forms for user authentication and data management.
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Record


class SignUpForm(UserCreationForm):
    """User registration form with additional fields."""
    
    first_name = forms.CharField(
        max_length=30,
        required=True,
        label='First Name',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        label='Last Name',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
    employee_id = forms.CharField(
        max_length=50,
        required=True,
        label='Employee ID',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Employee ID'})
    )
    department = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Department'})
    )
    role = forms.ChoiceField(
        choices=User.ROLE_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'})
    )
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'employee_id', 'department', 'role', 'username', 'password1', 'password2')
    
    def clean_email(self):
        """Ensure email is unique."""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already registered.')
        return email
    
    def clean_employee_id(self):
        """Ensure employee ID is unique."""
        employee_id = self.cleaned_data.get('employee_id')
        if User.objects.filter(employee_id=employee_id).exists():
            raise forms.ValidationError('This employee ID is already registered.')
        return employee_id


class LoginForm(forms.Form):
    """Login form with username and password."""
    
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )


class RecordForm(forms.ModelForm):
    """Form for creating and editing records."""
    
    data = forms.JSONField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
        help_text='Enter data as valid JSON format'
    )
    
    class Meta:
        model = Record
        fields = ('data',)
