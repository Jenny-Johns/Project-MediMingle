import re
from django.core.management.base import BaseCommand
from medi.models import Doctor

class Command(BaseCommand):
    help = 'Update consulting_fee field in Doctor model.'

    def handle(self, *args, **options):
        doctors = Doctor.objects.all()

        for doctor in doctors:
            if doctor.consulting_fee is not None:
                # Extract numeric part from the string and convert to integer
                numeric_part_match = re.search(r'\b(\d+)\b', str(doctor.consulting_fee))
                if numeric_part_match:
                    numeric_part = numeric_part_match.group(1)
                    doctor.consulting_fee = int(numeric_part)
                    doctor.save()

        self.stdout.write(self.style.SUCCESS('Successfully updated consulting_fee field.'))
