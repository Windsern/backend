from django.core.management.base import BaseCommand
from app.models import *


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        Verification.objects.all().delete()
        Building.objects.all().delete()
        CustomUser.objects.all().delete()