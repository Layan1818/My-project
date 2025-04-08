from django.core.management.base import BaseCommand
from apps.bookmodule.models import Address, Student
import random

class Command(BaseCommand):
    help = 'Seeds the database with sample student and address data'

    def handle(self, *args, **kwargs):
        # Create addresses
        cities = ['New York', 'London', 'Paris', 'Tokyo', 'Sydney']
        addresses = []
        
        for city in cities:
            address = Address.objects.create(city=city)
            addresses.append(address)
            self.stdout.write(f'Created address: {address}')

        # Create students
        names = ['John Doe', 'Jane Smith', 'Bob Wilson', 'Alice Brown', 
                'Charlie Davis', 'Emma Wilson', 'James Miller', 'Sophia Taylor',
                'Oliver White', 'Mia Johnson']
        
        for name in names:
            age = random.randint(18, 25)
            address = random.choice(addresses)
            student = Student.objects.create(
                name=name,
                age=age,
                address=address
            )
            self.stdout.write(f'Created student: {student}')

        self.stdout.write(self.style.SUCCESS('Successfully seeded database'))
