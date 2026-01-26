"""
URL configuration for the portal application.
"""
from django.urls import path
from . import views

urlpatterns = [
    # Public pages
    path('', views.landing, name='landing'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Department management
    path('create-department/', views.create_department, name='create_department'),
    
    # Tab management
    path('create-tab/<int:department_id>/', views.create_tab, name='create_tab'),
    path('rename-tab/<int:tab_id>/', views.rename_tab, name='rename_tab'),
    path('delete-tab/<int:tab_id>/', views.delete_tab, name='delete_tab'),
    
    # Data management
    path('tab/<int:tab_id>/', views.view_tab_data, name='view_tab'),
    path('tab/<int:tab_id>/add-record/', views.add_record, name='add_record'),
    path('record/<int:record_id>/edit/', views.edit_record, name='edit_record'),
    path('record/<int:record_id>/delete/', views.delete_record, name='delete_record'),
    path('record/<int:record_id>/update-cell/', views.update_cell, name='update_cell'),
    
    # Excel import
    path('tab/<int:tab_id>/import-excel/', views.import_excel, name='import_excel'),
    
    # REST API endpoints (TabulatorJS)
    path('api/tab/<int:tab_id>/records/', views.api_fetch_records, name='api_fetch_records'),
    path('api/tab/<int:tab_id>/records/create/', views.api_create_record, name='api_create_record'),
    path('api/record/<int:record_id>/', views.api_update_record, name='api_update_record'),
    path('api/record/<int:record_id>/delete/', views.api_delete_record, name='api_delete_record'),
]
