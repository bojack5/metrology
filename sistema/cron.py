import kronos
import smtplib
import MySQLdb

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from sistema.models import Factura
from datetime import datetime, timedelta , date 

@kronos.register('0 16 * * *')
def facturas_no_pagadas():
    print 'funcionando'
    facturas_no_pagadas = Factura.objects.filter(pagada=False)
    texto = ''
    
    inicio_mes = False
    if datetime.date(datetime.now()).day == 1:
        print "dia de envio"
        inicio_mes=True
        for factura in facturas_no_pagadas:
    	    diferencia = datetime.date(datetime.now())-factura.fecha        	
            if diferencia>timedelta(factura.orden_servicio.cotizacion.contacto.cliente.dias_de_credito):
                texto += '''<li><b>Cliente :</b> %s<br>
                            <b>contacto :</b> %s<br>
                            <b>Telefono :</b> %s<br>
                            <b>Ext. :</b> %s<br>
                            <b>Email :</b> %s<br>
                            <b>Fecha de la factura :</b> %s<br>
                            <b>Fecha de vencimiento :</b> %s<br>
                            <b>Folio :</b> %s<br>
                            <b>Importe :</b> $%s USD<br>
                             </li>'''%(factura.orden_servicio.cotizacion.contacto.cliente.nombre,
                         	           factura.orden_servicio.cotizacion.contacto.nombre,
                         	           factura.orden_servicio.cotizacion.contacto.telefono,
                         	           factura.orden_servicio.cotizacion.contacto.extension,
                         	           factura.orden_servicio.cotizacion.contacto.email,
                         	           factura.fecha,
                         	           factura.fecha+timedelta(factura.orden_servicio.cotizacion.contacto.cliente.dias_de_credito),
                         	           factura.id,
                         	           factura.orden_servicio.cotizacion.importe)

                      
        mandar_mail(texto,inicio_mes)                     

def mandar_mail(texto,inicio_mes):
    print "Mandando mensaje...."
    me = "luis.borbolla@udem.edu"
    you = 'luis@4suredesign.com , servicio_po@borbollametrology.com.mx , gabyborbolla@hotmail.com'

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    
    msg['From'] = me
    msg['To'] = you

        # Create the body of the message (a plain-text and an HTML version).
    text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttp://www.python.org"
    if inicio_mes:
    	meses = ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']
    	mes = datetime.date(datetime.now()).month
    	if mes < 1:
    	    mes = 12

        if 'li' in texto:
    	    msg['Subject'] = "Facturas Pendientes de pago de fecha : %s"%datetime.now()
            html = """
            <html>
              <head></head>
              <body>
                <p>A continuacion se enlistan las facturas con credito vencido durante el mes de %s, sin pago a la fecha de envio de este correo<br>
               
                </p>
                <ol>
                    %s

                </ol>
              </body>
            </html>
            """%(meses[mes-1],texto)
        else:
    	    msg['Subject'] = "No hay Facturas pendientes de pago"
            html = """
            <html>
              <head></head>
              <body>
                <p>No hay facturas con adeudos en el mes de  %s<br>
               
                </p>
            
              </body>
            </html>"""%meses[mes-1]
    else:
    	if 'li' in texto:
    	    msg['Subject'] = "Facturas Pendientes de pago de fecha : %s"%datetime.now()
            html = """
            <html>
              <head></head>
              <body>
                <p>A continuacion se enlistan las facturas cuyo credito vence el dia de hoy , favor de tomar medidas necesarias<br>
               
                </p>
                <ol>
                    %s

                </ol>
              </body>
            </html>
            """%texto
        else:
    	    msg['Subject'] = "No hay Facturas pendientes de pago"
            html = """
            <html>
              <head></head>
              <body>
                <p>No hay facturas con adeudos a la fecha %s<br>
               
                </p>
            
              </body>
            </html>"""%datetime.now()
    

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)
    # Send the message via local SMTP server.
    mail = smtplib.SMTP('smtp.gmail.com', 587)

    mail.ehlo()

    mail.starttls()

    mail.login('luis@4suredesign.com', 'borbollaSP123')
    mail.sendmail(me, you, msg.as_string())
    mail.quit()

        

                         
            	



        
