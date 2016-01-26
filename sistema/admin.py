from django.contrib import admin
from django import forms

import sistema.models

class ClientesAdmin(admin.ModelAdmin):
    list_display = ('nombre' , 'estado' , 'ciudad')
    search_fields = ('nombre' , 'estado')


class ContactosAdmin(admin.ModelAdmin):
    """docstring for ContactosAdmin"""
    list_display = ('nombre' ,'cliente', 'departamento' , 'telefono' , 'extension' )
    search_fields = ('nombre' , 'cliente__nombre')
    #filter_horizontal = ('cliente')
    raw_id_fields = ('cliente',)

class MaquinasAdmin(admin.ModelAdmin):
    """docstring for MaquinasAdmin"""
    list_display = ('modelo' , 'fabricante' , 'contacto' , 'get_cliente')
    search_fields = ('contacto__cliente__nombre' , 'fabricante' , 'modelo')
    raw_id_fields = ('contacto',)

    def get_cliente(self,obj):
        return obj.contacto.cliente.nombre
        
    get_cliente.admin_order_field  = 'nombre'  #Allows column order sorting
    get_cliente.short_description = 'Cliente de Contacto'  #Renames column head 

class CotizacionForm(forms.ModelForm):
    class Meta(object):
        """docstring for Meta"""
        model = sistema.models.Cotizacion
        exclude = ['importe','iva']            
    
        
class CotizacionAdmin(admin.ModelAdmin):
    """docstring for CotizacionAdmin"""
    list_display = ( 'get_cliente', 'get_contacto' ,'fecha' , 'importe' ,'id')
    filter_horizontal = ('servicio','maquinas')
    search_fields = ('fecha' , 'contacto__cliente__nombre' )
    date_hierarchy = ('fecha')
    raw_id_fields = ('contacto',)
    exclude = ['importe']
    form = CotizacionForm

    def get_cliente(self,obj):
        return obj.contacto.cliente.nombre

    def get_contacto(self,obj):
        return obj.contacto.nombre    
    
    get_cliente.admin_order_field  = 'nombre'  #Allows column order sorting
    get_cliente.short_description = 'Cliente de Contacto'  #Renames column head         
    
    get_contacto.admin_order_field  = 'nombre'  #Allows column order sorting
    get_contacto.short_description = 'Nombre de Contacto'  #Renames column head 

class Ordenes_de_servicioAdmin(admin.ModelAdmin):
    """docstring for Ordenes_de_servicioAdmin"""
    list_display = ( 'get_cliente', 'fecha')
    filter_horizontal = ('ingeniero' ,)
    date_hierarchy    = ('fecha')		    
    search_fields     = ('fecha' , 'ingeniero')
    raw_id_fields = ('cotizacion',)
    exclude = ['mail_enviado','fecha_mail_enviado']

    def get_cliente(self,obj):
        return obj.cotizacion.contacto.cliente.nombre

    get_cliente.admin_order_field  = 'nombre'  #Allows column order sorting
    get_cliente.short_description = 'Cliente desde cotizacion'  #Renames column head


class FacturaAdmin(admin.ModelAdmin):
    """docstring for FacturaAdmin"""
    list_display = ('get_id','get_contacto' , 'get_cliente' ,  'get_cotizacion' , 'fecha')
    search_fields = ('orden_servicio__cotizacion__contacto__cliente__nombre' , 'orden_servicio__cotizacion__contacto__nombre')
    date_hierarchy = ('fecha')
    raw_id_fields = ('orden_servicio', 'contacto_a_facturar')
    def get_cliente(self,obj):
        return obj.orden_servicio.cotizacion.contacto.cliente.nombre

    def get_cotizacion(self,obj):
        return obj.orden_servicio.cotizacion.id    

    def get_contacto(self,obj):
        return obj.orden_servicio.cotizacion.contacto.nombre

    def get_id(self,obj):
        return obj.id

    get_id.admin_order_field  = 'id'  #Allows column order sorting
    get_id.short_description = 'Folio'  #Renames column head        


    get_contacto.admin_order_field  = 'nombre'  #Allows column order sorting
    get_contacto.short_description = 'Contacto'  #Renames column head        

    get_cliente.admin_order_field  = 'nombre'  #Allows column order sorting
    get_cliente.short_description = 'Cliente'  #Renames column head        
    
    get_cotizacion.admin_order_field  = 'Cot_id'  #Allows column order sorting
    get_cotizacion.short_description = 'Cotizacion'

class IngenierosAdmin(admin.ModelAdmin):
    list_display = ('nombre' , 'referencia' , 'telefono')
    search_fields = ('nombre' , 'referencia')                        
    

admin.site.register(sistema.models.Clientes,ClientesAdmin)
admin.site.register(sistema.models.Contactos , ContactosAdmin)
admin.site.register(sistema.models.Maquinas , MaquinasAdmin)
admin.site.register(sistema.models.Servicios)
admin.site.register(sistema.models.ListaPrecios)
admin.site.register(sistema.models.Cotizacion , CotizacionAdmin)
admin.site.register(sistema.models.Ingenieros , IngenierosAdmin)
admin.site.register(sistema.models.Ordenes_de_servicio , Ordenes_de_servicioAdmin)
admin.site.register(sistema.models.Factura , FacturaAdmin)
# Register your models here.
