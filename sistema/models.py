from __future__ import unicode_literals

from django.db import models

class Terminos_pago(models.Model):
    terminos = models.CharField(max_length = 20)

    def __unicode__(self):
        return self.terminos



class Clientes(models.Model):
    """docstring for Clientes"""
    nombre    = models.CharField(max_length=40)
    direccion = models.CharField(max_length=70)
    estado    = models.CharField(max_length=16)
    ciudad    = models.CharField(max_length=30)
    cp        = models.IntegerField()
    kilometros= models.IntegerField()
    rfc       = models.CharField(max_length=13 , null = True)
    horas     = models.DecimalField(null = True,decimal_places = 2 , max_digits = 5)
    terminos_pago = models.ForeignKey(Terminos_pago,null=True)
    dias_de_credito = models.IntegerField(blank = True , null = True)

    def __unicode__(self):
        return u'%s %s' % (self.nombre , self.horas)

class Contactos(models.Model):
    """docstring for Contactos"""
    nombre       = models.CharField(max_length=30)
    departamento = models.CharField(max_length=16)
    telefono     = models.CharField(max_length = 16)
    extension    = models.IntegerField()
    email        = models.EmailField(blank = True)
    cliente      = models.ForeignKey(Clientes)
    
    def __unicode__(self):
        return self.nombre    


class Maquinas(models.Model):
    """docstring for Maquinas"""
    contacto        = models.ForeignKey(Contactos , null = True)
    id_usuario     = models.CharField(max_length=13 , null = True , blank = True)
    fabricante     = models.CharField(max_length=15 )
    no_serie       = models.CharField(max_length=10 )
    modelo         = models.CharField(max_length=10 )
    rango_x        = models.IntegerField()
    rango_y        = models.IntegerField()
    rango_z        = models.IntegerField()
    mppl           = models.IntegerField()
    mppe           = models.IntegerField()
    probe_type     = models.CharField(max_length=10 )
    probe_head     = models.CharField(max_length=16)
    probe_serial   = models.CharField(max_length=15 )
    extension      = models.IntegerField( blank = True , null = True)
    version_software=models.CharField(max_length=15)
    version_firmware=models.CharField(max_length=15)
    controlador    = models.CharField(max_length=10)
    accesorios     = models.CharField(max_length=15 , null = True , blank = True)
    driver_software= models.CharField(max_length=15)
    modelo_computadora=models.CharField(max_length=10)
    fecha_fabricacion = models.DateField(blank=True , null = True)
    diametro_stylus= models.IntegerField()

    def __unicode__(self):
        return u'%s %s %s %s ' % (self.modelo , self.fabricante , self.contacto.nombre , self.contacto.cliente.nombre)

class Servicios(models.Model):
    """docstring for Servicios"""
    servicio = models.CharField(max_length = 20)

    def __unicode__(self):
        return self.servicio
		
class ListaPrecios(models.Model):
    """docstring for ListaPrecios"""
    fecha          = models.DateField(null = True)
    horas          = models.IntegerField()
    horas_extra    = models.IntegerField()
    horas_viaje    = models.IntegerField(null = True)
    kilometros     = models.IntegerField()
    hotel          = models.IntegerField()
    manuales       = models.IntegerField()
    traslados      = models.IntegerField()
    avion          = models.IntegerField()
    sobre_equipaje = models.IntegerField() 
    renta_auto     = models.IntegerField()
    papeleria      = models.IntegerField()

    def __unicode__(self):
        return str(self.fecha)



class Ingenieros(models.Model):
    """docstring for Ingenieros"""
    nombre      = models.CharField(max_length=20)
    referencia = models.CharField(max_length=4)
    telefono   = models.CharField(max_length = 16)
    email      = models.EmailField(null = True)		    
    
    def __unicode__(self):
        return self.nombre

class Cotizacion(models.Model):
    """docstring for Cotizacion"""
    fecha          = models.DateField()
    contacto       = models.ForeignKey(Contactos , null = True)
    servicio       = models.ManyToManyField(Servicios)
    maquinas       = models.ManyToManyField(Maquinas)
    horas          = models.IntegerField()
    horas_extra    = models.IntegerField(blank=True ,null = True)
    #horas_viaje    = models.IntegerField()
    viajes         = models.IntegerField()
    hotel          = models.IntegerField(blank=True ,null = True)
    manuales       = models.IntegerField(blank=True ,null = True)
    traslados      = models.IntegerField( blank=True ,null = True)
    aviones        = models.IntegerField(blank=True ,null = True)
    sobre_equipaje = models.IntegerField(blank=True ,null = True)
    renta_auto     = models.IntegerField(blank=True ,null = True)
    papeleria      = models.IntegerField(blank=True ,null = True)
    importe        = models.IntegerField(blank = True , null = True)
    iva            = models.DecimalField(decimal_places = 2 , max_digits = 5 ,blank = True , default = 0.16)
    observaciones  = models.CharField(blank=True ,max_length = 255, null = True)
    SA             = models.IntegerField()
    tipo_cambio    = models.DecimalField(decimal_places = 2 , max_digits = 5, blank = True , null = True)

    def __unicode__(self):
        return u'%s %s %s %s' % (self.fecha , self.contacto.cliente.nombre , self.contacto.nombre ,self.servicio)

class Ordenes_de_servicio(models.Model):
    """docstring for Ordenes_de_trabajo"""
    fecha              = models.DateField(null = True)
    ingeniero          = models.ManyToManyField(Ingenieros)
    pagada             = models.IntegerField() 
    observaciones      = models.CharField(max_length = 255,null = True , blank = True)
    viaticos           = models.IntegerField()
    orden_compra       = models.CharField(max_length = 15)
    orden_compra_interna = models.IntegerField(blank = True , null = True)    
    fecha_servicio     = models.DateField(null = True)
    viaticos_pagados   = models.IntegerField(null = True)
    cotizacion         = models.ForeignKey(Cotizacion,null = True)
    mail_enviado       = models.IntegerField(null=True,blank=True,default=0)
    fecha_mail_enviado = models.DateField(null=True , blank = True)
    contacto_servicio  = models.ForeignKey(Contactos , null = True )


    

    def __unicode__(self):
        return u'%s %s' % (self.fecha,self.ingeniero)

class Factura(models.Model):
    """docstring for Factura"""
    fecha = models.DateField()    
    orden_servicio = models.ForeignKey(Ordenes_de_servicio)
    descripcion    = models.CharField(max_length=255,null = True , blank = True)
    pagada         = models.BooleanField()
    

    def __unicode__(self):
        return u'%s %s %s' % (self.orden_servicio.cotizacion.contacto.cliente.nombre , self.orden_servicio , self.fecha)

        

		
    




    				    		
# Create your models here.

# Create your models here.
