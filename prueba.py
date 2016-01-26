from django.core.management.base import BaseCommand
from sistema.models import cotizacion
from 

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        print "Hello, world"
