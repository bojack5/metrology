from django.core.mail import send_mail
from sistema.models import Ordenes_de_servicio
import math

class Mandar(object):
    """docstring for Email"""
    def __init__(self , id):
        import datetime
    	
        servicio = Ordenes_de_servicio.objects.get(pk=id)
        cliente ='''\nEmpresa : %s''' % servicio.cotizacion.contacto.cliente.nombre.upper()
        orden_servicio =  '''\nOrden Servicio : %s
        	                ''' % (servicio.id )
        PO =  '''\nPO : %s''' % (servicio.orden_compra )
        fecha_servicio = '''\nFecha :%s\n''' % (servicio.fecha)


        cotizacion_numero = '%s-%s%s%s' % (servicio.cotizacion.id*10+80000,servicio.cotizacion.fecha.month/10,servicio.cotizacion.fecha.month%10 , servicio.cotizacion.fecha.year-2000)
        print cotizacion_numero
        cotizacion = '''\nCOTIZACION :%s''' % cotizacion_numero
        ingenieros = servicio.ingeniero.values_list('nombre', flat=True)
        servicios = servicio.cotizacion.servicio.values_list('servicio', flat=True)

        inges_string = ''
        for nombre in ingenieros:
            inges_string += nombre+'\t'
        servicios_string = ''
        for service in servicios:
            servicios_string += service+'\t'    	

        ingenieros_mail = servicio.ingeniero.values_list('email',flat=True)

        dias = math.ceil(servicio.cotizacion.horas/8.0)
        limite = servicio.fecha+datetime.timedelta(days=dias)
        print 'Fecha = %s dias = %s limite=%s'%(servicio.fecha,dias,limite)
        datos =  '''\nIngeniero(s) : %s\nServicio(s) : %s\nDireccion : %s\nCiudad : %s\nEstado : %s\nContacto : %s\nTelefono : %s\nEmail : %s\nHoras : %s\nDias : %s\nServicio desde %s al  %s 
        	              '''%(inges_string,
        	              	   servicios_string,
        	              	   servicio.cotizacion.contacto.cliente.direccion.upper(),
        	              	   servicio.cotizacion.contacto.cliente.ciudad.upper(),
        	              	   servicio.cotizacion.contacto.cliente.estado.upper(),
        	              	   servicio.cotizacion.contacto.nombre.upper(),
        	              	   servicio.cotizacion.contacto.telefono.upper(),
        	              	   servicio.cotizacion.contacto.email,
        	              	   servicio.cotizacion.horas,
        	              	   int(dias),
        	              	   servicio.fecha,
        	              	   limite,
        	              	   )
        
        #data= [[cliente,],[[Orden_servicio,PO,fecha_servicio]],[[cotizacion,datos,]]]
 
        #t=Table(data , style=[('GRID',(0,0),(1,2),2,colors.black),])
        #t._argW[3]=1.5*inch
        datos_final = '''       servicio_po@borbollametrology.com.mx \n
        	                    Tel : 844 412-88-68\n
        	                    whatsapp : 8444164051\n
        	                    '''	
        send_mail('Orden de Servicio para | %s fecha : %s ' % (servicio.cotizacion.contacto.cliente.nombre , servicio.fecha_servicio),
                  cliente+orden_servicio+PO+fecha_servicio+cotizacion+datos+datos_final,
                  'luis@4suredesign.com',
                  ingenieros_mail)	                    
    	
        