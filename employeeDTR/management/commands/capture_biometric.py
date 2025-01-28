# filepath: /Users/laptop-127/Desktop/Thesis/DTRPAYROLL_ALPHA/DTRPAYROLL/employeeDTR/management/commands/capture_biometric.py
from django.core.management.base import BaseCommand
from employeeDTR.pyzk.get_biometrics import capture_biometric

class Command(BaseCommand):
    help = 'Capture biometric data'

    def handle(self, *args, **kwargs):
        capture_biometric()