
import kronos
import smtplib
import MySQLdb

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from sistema.models import Factura
from datetime import datetime, timedelta , date , now

@kronos.register('0 7 * * 1')
def facturas_no_pagadas():
    facturas_no_pagadas = Facturas.objects.filter(pagada=False)
    texto = ''
    for factura in facturas_no_pagadas:
    	diferencia = date(datetime.now())-factura.fecha
        if diferencia>timedelta(factura.orden_servicio.cotizacion.contacto.cliente.dias_de_credito):
            texto += '''<li><b>Cliente :</b> %s<br>
                        <b>contacto :</b> %s<br>
                        <b>Telefono :</b> %s<br>
                        <b>Ext. :</b> %s<br>
                        <b>Email :</b> %s<br>
                        <b>Fecha de la cotizacion :</b> %s<br>
                        <b>Fecha de vencimiento :</b> %s<br>
                        <b>Folio :</b> %s<br>
                         </li>'''%(factura.orden_servicio.cotizacion.contacto.cliente.nombre,
                         	       factura.orden_servicio.cotizacion.contacto.nombre
                         	       factura.orden_servicio.cotizacion.contacto.telefono,
                         	       factura.orden_servicio.cotizacion.contacto.extension,
                         	       factura.orden_servicio.cotizacion.contacto.email,
                         	       factura.fecha,
                         	       factura.fecha+timedelta(factura.orden_servicio.cotizacion.contacto.cliente.dias_de_credito),
                         	       factura.id,)

    if 'li' in texto:
    	# me == my email address
        # you == recipient's email address
        me = "luis.borbolla@udem.edu"
        you = "luis@4suredesign.com"

        # Create message container - the correct MIME type is multipart/alternative.
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Facturas Pendientes de pago a la fecha"
        msg['From'] = me
        msg['To'] = you

        # Create the body of the message (a plain-text and an HTML version).
        text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttp://www.python.org"
        html = """\
        <html>
          <head></head>
          <body>
            <p>A continuacion se enlistan las facturas con credito vencido , sin pago a la fecha de envio de este correo<br>
               
            </p>
            <ol>
                %s

            </ol>
          </body>
        </html>
        """%texto
        
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

        

                         
            	



        