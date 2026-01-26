"""
Management command to populate initial test data
Usage: python manage.py populate_test_data
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from portal.models import Department, Tab, Record
import json

User = get_user_model()


class Command(BaseCommand):
    help = 'Populate database with test data for demonstration'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('⏳ Creating test data...'))

        # Check if data already exists
        if User.objects.filter(username='director_test').exists():
            self.stdout.write(self.style.ERROR('❌ Test data already exists!'))
            return

        try:
            # Create test users
            self.stdout.write('Creating test users...')
            
            director = User.objects.create_user(
                username='director_test',
                password='Director123!',
                email='director@example.com',
                first_name='John',
                last_name='Director',
                employee_id='EMP001',
                department='Management',
                role='director'
            )
            
            scientist = User.objects.create_user(
                username='scientist_test',
                password='Scientist123!',
                email='scientist@example.com',
                first_name='Jane',
                last_name='Scientist',
                employee_id='EMP002',
                department='Research',
                role='scientist'
            )
            
            staff = User.objects.create_user(
                username='staff_test',
                password='Staff123!',
                email='staff@example.com',
                first_name='Bob',
                last_name='Staff',
                employee_id='EMP003',
                department='Operations',
                role='staff'
            )
            
            self.stdout.write(self.style.SUCCESS('✅ Users created'))

            # Create test department
            self.stdout.write('Creating test department...')
            dept = Department.objects.create(
                name='Research & Development',
                description='Department focused on research and development initiatives',
                created_by=director
            )
            self.stdout.write(self.style.SUCCESS('✅ Department created'))

            # Create test tabs
            self.stdout.write('Creating test tabs...')
            
            paid_interns = Tab.objects.create(
                department=dept,
                name='Paid Interns',
                description='Records of paid internship positions',
                created_by=director
            )
            
            unpaid_interns = Tab.objects.create(
                department=dept,
                name='Unpaid Interns',
                description='Records of unpaid internship positions',
                created_by=director
            )
            
            publishing = Tab.objects.create(
                department=dept,
                name='Publishing',
                description='Published research and papers',
                created_by=scientist
            )
            
            self.stdout.write(self.style.SUCCESS('✅ Tabs created'))

            # Create test records
            self.stdout.write('Creating test records...')
            
            # Sample records for Paid Interns
            record1 = Record.objects.create(
                tab=paid_interns,
                data={
                    'Name': 'Alice Johnson',
                    'Email': 'alice@example.com',
                    'Position': 'Software Engineer Intern',
                    'Start Date': '2024-06-01',
                    'End Date': '2024-08-31',
                    'Status': 'Active'
                },
                created_by=director
            )
            
            record2 = Record.objects.create(
                tab=paid_interns,
                data={
                    'Name': 'Charlie Brown',
                    'Email': 'charlie@example.com',
                    'Position': 'Data Science Intern',
                    'Start Date': '2024-07-01',
                    'End Date': '2024-09-30',
                    'Status': 'Active'
                },
                created_by=scientist
            )
            
            # Sample records for Unpaid Interns
            record3 = Record.objects.create(
                tab=unpaid_interns,
                data={
                    'Name': 'Diana Martinez',
                    'Email': 'diana@example.com',
                    'Position': 'Research Assistant',
                    'Start Date': '2024-05-15',
                    'End Date': '2024-10-15',
                    'Status': 'Active'
                },
                created_by=scientist
            )
            
            # Sample records for Publishing
            record4 = Record.objects.create(
                tab=publishing,
                data={
                    'Title': 'Machine Learning in Healthcare',
                    'Authors': 'Jane Scientist, John Director',
                    'Journal': 'Nature Research',
                    'Publication Date': '2024-01-15',
                    'DOI': '10.1234/example.doi',
                    'Status': 'Published'
                },
                created_by=scientist
            )
            
            record5 = Record.objects.create(
                tab=publishing,
                data={
                    'Title': 'Advances in Data Processing',
                    'Authors': 'Jane Scientist',
                    'Journal': 'IEEE Transactions',
                    'Publication Date': '2024-03-20',
                    'DOI': '10.5678/example.doi',
                    'Status': 'Published'
                },
                created_by=scientist
            )
            
            self.stdout.write(self.style.SUCCESS('✅ Records created'))

            # Print summary
            self.stdout.write('\n' + '='*50)
            self.stdout.write(self.style.SUCCESS('✅ Test data created successfully!'))
            self.stdout.write('='*50)
            self.stdout.write('\n📋 Test Credentials:\n')
            self.stdout.write('Director Account:')
            self.stdout.write('  Username: director_test')
            self.stdout.write('  Password: Director123!')
            self.stdout.write('')
            self.stdout.write('Scientist Account:')
            self.stdout.write('  Username: scientist_test')
            self.stdout.write('  Password: Scientist123!')
            self.stdout.write('')
            self.stdout.write('Staff Account:')
            self.stdout.write('  Username: staff_test')
            self.stdout.write('  Password: Staff123!')
            self.stdout.write('\n' + '='*50 + '\n')

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error creating test data: {str(e)}')
            )
            raise
