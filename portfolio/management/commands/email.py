from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.template.loader import get_template
from django.utils import timezone

class Command(BaseCommand):
    help = 'Update portfolio prices'

    def handle(self, *args, **kwargs):
        print("Update portfolio prices")