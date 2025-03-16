from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.users.models import DriverProfile, StudentProfile
from django.utils import timezone

User = get_user_model()

class Command(BaseCommand):
    help = 'Initialize database with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating initial data...')

        # Create admin user
        admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@trackmyride.com',
            password='admin123',
            first_name='Admin',
            last_name='User',
            role='ADMIN'
        )
        self.stdout.write(self.style.SUCCESS(f'Created admin user: {admin_user.username}'))

        # Create sample drivers
        drivers_data = [
            {
                'username': 'driver1',
                'password': 'driver123',
                'email': 'driver1@trackmyride.com',
                'first_name': 'John',
                'last_name': 'Doe',
                'role': 'DRIVER',
                'phone_number': '+1234567890',
                'profile': {
                    'license_number': 'DL123456',
                    'years_of_experience': 5,
                }
            },
            {
                'username': 'driver2',
                'password': 'driver123',
                'email': 'driver2@trackmyride.com',
                'first_name': 'Jane',
                'last_name': 'Smith',
                'role': 'DRIVER',
                'phone_number': '+1234567891',
                'profile': {
                    'license_number': 'DL789012',
                    'years_of_experience': 3,
                }
            }
        ]

        for driver_data in drivers_data:
            profile_data = driver_data.pop('profile')
            driver = User.objects.create_user(**driver_data)
            DriverProfile.objects.create(user=driver, **profile_data)
            self.stdout.write(self.style.SUCCESS(f'Created driver: {driver.username}'))

        # Create sample students
        students_data = [
            {
                'username': 'student1',
                'password': 'student123',
                'email': 'student1@trackmyride.com',
                'first_name': 'Alice',
                'last_name': 'Johnson',
                'role': 'STUDENT',
                'phone_number': '+1234567892',
                'profile': {
                    'student_id': 'ST001',
                    'department': 'Computer Science',
                    'semester': 3,
                }
            },
            {
                'username': 'student2',
                'password': 'student123',
                'email': 'student2@trackmyride.com',
                'first_name': 'Bob',
                'last_name': 'Wilson',
                'role': 'STUDENT',
                'phone_number': '+1234567893',
                'profile': {
                    'student_id': 'ST002',
                    'department': 'Engineering',
                    'semester': 4,
                }
            }
        ]

        for student_data in students_data:
            profile_data = student_data.pop('profile')
            student = User.objects.create_user(**student_data)
            StudentProfile.objects.create(user=student, **profile_data)
            self.stdout.write(self.style.SUCCESS(f'Created student: {student.username}'))

        self.stdout.write(self.style.SUCCESS('Successfully created initial data')) 