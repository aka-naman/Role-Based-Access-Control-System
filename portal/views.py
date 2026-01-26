"""
Views for authentication, dashboard, and data management.
"""
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from .models import User, Department, Tab, Record
from .forms import SignUpForm, LoginForm, RecordForm
from .utils import import_excel_data


def landing(request):
    """Public landing page."""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'landing.html')


def signup(request):
    """User registration page."""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = SignUpForm()
    
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    """User login page."""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    """User logout."""
    logout(request)
    return redirect('landing')


@login_required
def dashboard(request):
    """Role-based dashboard showing departments and tabs."""
    departments = Department.objects.all()
    
    context = {
        'departments': departments,
        'user_role': request.user.role,
        'can_manage_tabs': request.user.can_manage_tabs(),
    }
    
    return render(request, 'dashboard.html', context)


@login_required
@require_http_methods(["POST"])
def create_department(request):
    """Create a new department (Director/Scientist only)."""
    if not request.user.can_manage_tabs():
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    try:
        data = json.loads(request.body)
        name = data.get('name', '').strip()
        description = data.get('description', '').strip()
        
        if not name:
            return JsonResponse({'error': 'Department name is required'}, status=400)
        
        if Department.objects.filter(name=name).exists():
            return JsonResponse({'error': 'Department already exists'}, status=400)
        
        department = Department.objects.create(
            name=name,
            description=description,
            created_by=request.user
        )
        
        return JsonResponse({
            'success': True,
            'department': {
                'id': department.id,
                'name': department.name,
                'description': department.description,
            }
        })
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@require_http_methods(["POST"])
def create_tab(request, department_id):
    """Create a new tab in a department (Director/Scientist only)."""
    if not request.user.can_manage_tabs():
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    department = get_object_or_404(Department, id=department_id)
    
    try:
        data = json.loads(request.body)
        name = data.get('name', '').strip()
        description = data.get('description', '').strip()
        
        if not name:
            return JsonResponse({'error': 'Tab name is required'}, status=400)
        
        if Tab.objects.filter(department=department, name=name).exists():
            return JsonResponse({'error': 'Tab already exists in this department'}, status=400)
        
        tab = Tab.objects.create(
            department=department,
            name=name,
            description=description,
            created_by=request.user
        )
        
        return JsonResponse({
            'success': True,
            'tab': {
                'id': tab.id,
                'name': tab.name,
                'description': tab.description,
            }
        })
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@require_http_methods(["POST"])
def rename_tab(request, tab_id):
    """Rename a tab (Director/Scientist only)."""
    if not request.user.can_manage_tabs():
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    tab = get_object_or_404(Tab, id=tab_id)
    
    try:
        data = json.loads(request.body)
        new_name = data.get('name', '').strip()
        
        if not new_name:
            return JsonResponse({'error': 'Tab name is required'}, status=400)
        
        if Tab.objects.filter(
            department=tab.department,
            name=new_name
        ).exclude(id=tab.id).exists():
            return JsonResponse({'error': 'Tab name already exists in this department'}, status=400)
        
        tab.name = new_name
        tab.save()
        
        return JsonResponse({
            'success': True,
            'tab': {
                'id': tab.id,
                'name': tab.name,
            }
        })
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@require_http_methods(["DELETE", "POST"])
def delete_tab(request, tab_id):
    """Delete a tab (Director/Scientist only)."""
    if not request.user.can_manage_tabs():
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    tab = get_object_or_404(Tab, id=tab_id)
    
    try:
        tab_name = tab.name
        tab.delete()
        
        return JsonResponse({
            'success': True,
            'message': f'Tab "{tab_name}" deleted successfully'
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def view_tab_data(request, tab_id):
    """View all records in a tab using TabulatorJS grid."""
    tab = get_object_or_404(Tab, id=tab_id)
    
    # Check permission
    if not request.user.has_permission('view', tab.department, tab):
        return HttpResponseForbidden('You do not have permission to view this tab.')
    
    context = {
        'tab': tab,
        'can_add': request.user.has_permission('add', tab.department, tab),
        'can_edit': request.user.has_permission('edit', tab.department, tab),
        'can_delete': request.user.has_permission('delete', tab.department, tab),
    }
    
    return render(request, 'view_tab_tabulator.html', context)


@login_required
def add_record(request, tab_id):
    """Add a new record to a tab."""
    tab = get_object_or_404(Tab, id=tab_id)
    
    # Check permission
    if not request.user.has_permission('add', tab.department, tab):
        return HttpResponseForbidden('You do not have permission to add records to this tab.')
    
    # Get existing columns from other records
    existing_columns = set()
    for record in tab.records.all():
        if isinstance(record.data, dict):
            existing_columns.update(record.data.keys())
    existing_columns = sorted(list(existing_columns))
    
    if request.method == 'POST':
        # Try to get JSON data first (from form submission with hidden field)
        data = {}
        
        # Check if data_json exists (from form handler)
        import json
        if 'data_json' in request.POST:
            try:
                data = json.loads(request.POST.get('data_json', '{}'))
            except json.JSONDecodeError:
                pass
        
        # Fallback: Build data from individual form fields
        if not data:
            for col in existing_columns:
                value = request.POST.get(f'field_{col}', '').strip()
                if value:
                    data[col] = value
            
            # Add any dynamic fields from POST
            for key, value in request.POST.items():
                if key.startswith('dynamic_col_'):
                    num = key.replace('dynamic_col_', '')
                    col_name = value.strip()
                    col_value = request.POST.get(f'dynamic_val_{num}', '').strip()
                    if col_name and col_value:
                        data[col_name] = col_value
        
        if data:
            record = Record.objects.create(
                tab=tab,
                data=data,
                created_by=request.user
            )
            messages.success(request, 'Record added successfully!')
            return redirect('view_tab', tab_id=tab_id)
        else:
            messages.error(request, 'Please fill in at least one field')
            context = {
                'tab': tab,
                'columns': existing_columns
            }
            return render(request, 'add_record.html', context)
    
    context = {
        'tab': tab,
        'columns': existing_columns if existing_columns else ['Field 1', 'Field 2']
    }
    return render(request, 'add_record.html', context)


@login_required
def edit_record(request, record_id):
    """Edit an existing record."""
    record = get_object_or_404(Record, id=record_id)
    
    # Check permission
    if not request.user.has_permission('edit', record.tab.department, record.tab):
        return HttpResponseForbidden('You do not have permission to edit this record.')
    
    if request.method == 'POST':
        try:
            data = json.loads(request.POST.get('data', '{}'))
            record.data = data
            record.updated_by = request.user
            record.save()
            return redirect('view_tab', tab_id=record.tab.id)
        except json.JSONDecodeError:
            context = {'record': record, 'tab': record.tab, 'error': 'Invalid JSON format'}
            return render(request, 'edit_record.html', context, status=400)
    
    context = {
        'record': record,
        'tab': record.tab,
        'data_json': json.dumps(record.data, indent=2)
    }
    
    return render(request, 'edit_record.html', context)


@login_required
@require_http_methods(["POST"])
def delete_record(request, record_id):
    """Delete a record."""
    record = get_object_or_404(Record, id=record_id)
    tab = record.tab
    
    # Check permission
    if not request.user.has_permission('delete', tab.department, tab):
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    try:
        record.delete()
        return JsonResponse({'success': True, 'message': 'Record deleted successfully'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def import_excel(request, tab_id):
    """Import Excel data into a tab."""
    tab = get_object_or_404(Tab, id=tab_id)
    
    # Check permission
    if not request.user.has_permission('add', tab.department, tab):
        return HttpResponseForbidden('You do not have permission to add records to this tab.')
    
    if request.method == 'POST':
        if 'file' not in request.FILES:
            return render(request, 'import_excel.html', {'tab': tab, 'error': 'No file selected'})
        
        file = request.FILES['file']
        
        if not file.name.endswith(('.xlsx', '.xls')):
            return render(request, 'import_excel.html', {'tab': tab, 'error': 'Please upload an Excel file'})
        
        try:
            count = import_excel_data(file, tab, request.user)
            return render(request, 'import_excel.html', {
                'tab': tab,
                'success': f'Successfully imported {count} records'
            })
        except Exception as e:
            return render(request, 'import_excel.html', {'tab': tab, 'error': f'Import failed: {str(e)}'})
    
    return render(request, 'import_excel.html', {'tab': tab})


@login_required
@require_http_methods(["POST"])
def update_cell(request, record_id):
    """Update a single cell value in a record (inline editing)."""
    record = get_object_or_404(Record, id=record_id)
    
    # Check permission
    if not request.user.has_permission('edit', record.tab.department, record.tab):
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    try:
        data = json.loads(request.body)
        column = data.get('column', '').strip()
        value = data.get('value', '')
        
        if not column:
            return JsonResponse({'error': 'Column name required'}, status=400)
        
        # Update the record data
        if not isinstance(record.data, dict):
            record.data = {}
        
        record.data[column] = value
        record.updated_by = request.user
        record.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Cell updated successfully',
            'value': value
        })
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# ============================================================================
# REST API ENDPOINTS FOR TABULATOR.JS
# ============================================================================

@login_required
@require_http_methods(["GET"])
@login_required
def api_fetch_records(request, tab_id):
    """
    REST API endpoint: Fetch all records in a tab with dynamic column detection.
    
    Method: GET
    URL: /api/tab/{tab_id}/records/
    
    Purpose:
    - Retrieve all records from a specific tab in JSON format
    - Dynamically extract column names from record JSONField data
    - Include permission information for frontend UI control
    
    Returns:
    {
        "data": [
            {
                "id": 1,
                "S.No": 1,
                "Name": "John",
                "Department": "IT",
                ...
            }
        ],
        "columns": ["id", "S.No", "Name", "Department", ...],
        "can_edit": true,
        "can_delete": true
    }
    
    Authorization: User must have VIEW permission on the tab's department
    """
    tab = get_object_or_404(Tab, id=tab_id)
    
    # Check permission: User must have view access to this tab
    if not request.user.has_permission('view', tab.department, tab):
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    records = tab.records.all()
    
    # Extract all unique column names from all records' JSONField data
    # This enables dynamic column generation in the frontend grid
    columns = set(['id'])  # Always include ID column first
    for record in records:
        if isinstance(record.data, dict):
            columns.update(record.data.keys())
    columns = sorted(list(columns))
    
    # Build data array: Convert each record with its ID and JSON data
    data = []
    for record in records:
        row = {'id': record.id}
        if isinstance(record.data, dict):
            row.update(record.data)  # Merge JSON field data into row
        else:
            row['data'] = record.data
        data.append(row)
    
    # Return data with permission flags for UI control (edit/delete buttons)
    return JsonResponse({
        'data': data,
        'columns': columns,
        'can_edit': request.user.has_permission('edit', tab.department, tab),
        'can_delete': request.user.has_permission('delete', tab.department, tab),
    })


@login_required
@require_http_methods(["POST"])
def api_create_record(request, tab_id):
    """
    REST API endpoint: Create a new record in a tab.
    
    Method: POST
    URL: /api/tab/{tab_id}/records/create/
    Body: JSON object with field names and values
    
    Purpose:
    - Create a new record with JSON data
    - Auto-increment ID (database-managed)
    - Track creator and timestamp
    
    Request Example:
    {
        "Name": "John Doe",
        "Department": "IT",
        "Age": 28
    }
    
    Returns:
    {
        "success": true,
        "id": 153,
        "data": {
            "Name": "John Doe",
            "Department": "IT",
            "Age": 28
        }
    }
    
    Authorization: User must have ADD permission on the tab's department
    """
    tab = get_object_or_404(Tab, id=tab_id)
    
    # Check permission: User must have add/create access
    if not request.user.has_permission('add', tab.department, tab):
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    try:
        # Parse JSON request body
        data = json.loads(request.body)
        
        # Remove 'id' if present (should not be in request, auto-generated by DB)
        if 'id' in data:
            del data['id']
        
        # Create new record with JSON data
        record = Record.objects.create(
            tab=tab,
            data=data,
            created_by=request.user
        )
        
        # Return success response with created record ID
        return JsonResponse({
            'success': True,
            'id': record.id,
            'data': record.data
        }, status=201)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@require_http_methods(["PATCH", "PUT"])
def api_update_record(request, record_id):
    """
    REST API endpoint: Update a record field(s).
    
    Method: PATCH (partial update) or PUT
    URL: /api/record/{record_id}/
    Body: JSON object with fields to update
    
    Purpose:
    - Update one or more fields in a record
    - Merge new data with existing data (PATCH semantics)
    - Track who updated the record and when
    
    Request Example:
    {
        "Name": "Jane Doe",
        "Age": 29
    }
    
    Returns:
    {
        "success": true,
        "id": 153,
        "data": {
            "Name": "Jane Doe",
            "Department": "IT",
            "Age": 29
        }
    }
    
    Authorization: User must have EDIT permission on the record's tab department
    """
    record = get_object_or_404(Record, id=record_id)
    
    # Check permission: User must have edit access to this tab
    if not request.user.has_permission('edit', record.tab.department, record.tab):
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    try:
        # Parse JSON request body
        data = json.loads(request.body)
        
        # Merge new data with existing record data (PATCH semantics)
        if not isinstance(record.data, dict):
            record.data = {}
        
        record.data.update(data)
        record.updated_by = request.user
        record.save()
        
        # Return success response with updated record
        return JsonResponse({
            'success': True,
            'id': record.id,
            'data': record.data
        })
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@require_http_methods(["DELETE"])
def api_delete_record(request, record_id):
    """
    REST API endpoint: Delete a record.
    
    Method: DELETE
    URL: /api/record/{record_id}/delete/
    
    Purpose:
    - Permanently delete a record from the database
    - Include ID in response for confirmation on frontend
    - Perform permission check before deletion
    
    Returns:
    {
        "success": true,
        "id": 153,
        "message": "Record deleted successfully"
    }
    
    Authorization: User must have DELETE permission on the record's tab department
    """
    record = get_object_or_404(Record, id=record_id)
    
    # Check permission: User must have delete access to this tab
    if not request.user.has_permission('delete', record.tab.department, record.tab):
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    try:
        # Store ID before deletion for response
        record_id = record.id
        record.delete()
        
        # Return success response with deleted record ID
        return JsonResponse({
            'success': True,
            'id': record_id,
            'message': 'Record deleted successfully'
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
