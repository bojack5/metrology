from django.core.management.base import BaseCommand
from sistema.models import Cotizacion
from django.core.mail import send_mail

cotizacion = Cotizacion.objects.get(pk=1)
send_mail('Correo desde pythonanywhere','%s'%cotizacion.contacto.nombre,'luis@4suredesign.com',['luis@4suredesign.com'])




