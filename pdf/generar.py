from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from django.contrib.auth.models import User
from reportlab.platypus import SimpleDocTemplate, Paragraph , Image , Table ,PageBreak
from sistema.models import Cotizacion , Contactos , ListaPrecios ,Clientes , Ordenes_de_servicio , Factura
from django.db.models import Max

from reportlab.pdfgen import canvas
from reportlab.lib.units import mm , inch

import moneda
import math

 
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []
 
    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()
 
    def save(self):
        """add page info to each page (page x of y)"""
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)
 
    def draw_page_number(self, page_count):
        # Change the position of this to wherever you want the page number to be
        self.drawRightString(211 * mm, 15 * mm + (0.2 * inch),
                             "Pagina %d de %d" % (self._pageNumber, page_count))


class Impresion(object):
    """Clase para manejo de impresion de PDFs"""
    def __init__(self, buffer , pagesize):
        self.buffer = buffer
        if pagesize == 'A4':
            self.pagesize = A4
        elif pagesize == 'Letter':
            self.pagesize = letter
        self.width , self.height = self.pagesize
        self.doc = SimpleDocTemplate(buffer ,
        	                    rightMargin = 72 , 
        	                    leftMargin = 130 ,
        	                    topMargin = 72 ,
        	                    bottomMargin = 72 ,
        	                    pagesize = self.pagesize ,)
        self.styles = getSampleStyleSheet()
        self.styles.add(ParagraphStyle(name = 'centered' , alignment = TA_CENTER))
        self.direccion = Paragraph('''
        	                       <br></br>
        	                       <para align=right>319 East Coma Ave<br></br>
        	                       Hidalgo Texas USA<br></br>
        	                       Tel : +52 1 (844) 4 12 88 68. (844) 4 10 36 06<br></br>
        	                       servicio_po@borbollametrology.com.mx<br></br>
        	                       www.borbollametrology.com

        	                       ''',self.styles['BodyText'])


    @staticmethod
    def _header_footer(canvas,doc):
        #guardamos el estado de nuestro canvas , para poder dibujar en el 
        canvas.saveState()
        canvas.setTitle("Cotizacion Cliente")
        styles = getSampleStyleSheet()

        #header
        header = Image('/home/borbolla/metrology/static_media/assets/images/borbolla_metrology_logo.jpg' )
        header.drawHeight = 60
        header.drawWidth = 424
        header.hAlign = 'RIGHT'
        w , h = header.wrap(doc.width , doc.topMargin)
        header.drawOn(canvas , doc.leftMargin , 700)
        
        marcas = Image('/home/borbolla/metrology/static_media/assets/images/marcas.png' )
        marcas.drawWidth = 90
        marcas.drawHeight = 477
        marcas.drawOn(canvas , 20,200) 
        
        marcas2 = Image('/home/borbolla/metrology/static_media/assets/images/logo.png' )
        marcas2.drawWidth = 116
        marcas2.drawHeight = 34
        marcas2.drawOn(canvas , 20,150) 

        # Footer
        footer = Paragraph('www.borbollametrology.com', styles['Normal'])
        w, h = footer.wrap(doc.width, doc.bottomMargin)
        footer.drawOn(canvas, doc.leftMargin, h)
 
        # Release the canvas
        canvas.restoreState()

    @staticmethod
    def _header_servicio(canvas,doc):
        #guardamos el estado de nuestro canvas , para poder dibujar en el 
        canvas.saveState()
        canvas.setTitle("Orden de servicio")
        styles = getSampleStyleSheet()

        #header
        header = Image('/home/borbolla/metrology/static_media/assets/images/logo_servicio.png' )
        header.drawHeight = 50
        header.drawWidth = 285
        header.hAlign = 'RIGHT'
        w , h = header.wrap(doc.width , doc.topMargin)
        header.drawOn(canvas , doc.leftMargin , 700)
        
        

        # Footer
        footer = Paragraph('www.borbollametrology.com', styles['Normal'])
        w, h = footer.wrap(doc.width, doc.bottomMargin)
        footer.drawOn(canvas, doc.leftMargin, h)
 
        # Release the canvas
        canvas.restoreState()        	
    @staticmethod
    def _header_factura(canvas,doc):
        #guardamos el estado de nuestro canvas , para poder dibujar en el 
        canvas.saveState()
        canvas.setTitle("Factura")
        styles = getSampleStyleSheet()

        #header
        header = Image('/home/borbolla/metrology/static_media/assets/images/logo_servicio.png' )
        header.drawHeight = 70
        header.drawWidth = 399
        header.hAlign = 'RIGHT'
        w , h = header.wrap(doc.width , doc.topMargin)
        header.drawOn(canvas , doc.leftMargin , 700)
        
        

        # Footer
        footer = Paragraph('www.borbollametrology.com', styles['Normal'])
        w, h = footer.wrap(doc.width, doc.bottomMargin)
        footer.drawOn(canvas, doc.leftMargin, h)
 
        # Release the canvas
        canvas.restoreState()

    def print_cotizaciones(self , id=7):
        buffer = self.buffer
        doc = self.doc
        #Contenedor de objetos
        elements = []
        #coleccion de stylesheets pre-hechas
        styles = self.styles
        #dibujamos cosas en el PDF 
        print id
        cotizacion = Cotizacion.objects.get(pk = id)
        cliente    = Clientes.objects.get(pk=cotizacion.contacto.cliente.id)
        print cliente
        
        contacto  = cotizacion.contacto.nombre
        cliente   = cotizacion.contacto.cliente.nombre
        direccion = cotizacion.contacto.cliente.direccion
        ciudad    = cotizacion.contacto.cliente.ciudad
        estado    = cotizacion.contacto.cliente.estado
        telefono  = cotizacion.contacto.telefono
        extension = cotizacion.contacto.extension
        email     = cotizacion.contacto.email
        
        cotizacion_fecha = Paragraph('''
        	                   <para align=right>
        	                   <b>
        	                   <font color=red>COTIZACION : %s</font><br></br>
        	                   Fecha : %s
        	                   </b>
        	                   '''%(str(cotizacion.id*10+80000)+'-%s%s%s'%(cotizacion.fecha.month/10,cotizacion.fecha.month%10,cotizacion.fecha.year-2000) , cotizacion.fecha) ,
        	                   styles['BodyText'])

        datos_cliente = Paragraph('''
        	                      <para align=left>
        	                      <b>%s</b><br></br>
        	                      %s <br></br>
        	                      %s <br></br>
        	                      %s %s<br></br>
        	                      %s EXT %s<br></br>
        	                      %s<br></br>
        	                      '''%(contacto.upper() , cliente.upper() , direccion.upper() , ciudad.upper() , estado.upper() , telefono , extension , email.lower())
        	                      ,styles['BodyText'])
        texto_pre = Paragraph('Presentamos a continuacion la siguiente cotizacion solicitada por usted<br></br><br></br>',styles['BodyText'])
        
        h_modelo = Paragraph('<b>Modelo</b>',styles['BodyText'])
        h_no_serie = Paragraph('<b>No. de Serie</b>',styles['BodyText'])
        h_especificacion = Paragraph('<b>Especificacion</b>',styles['BodyText'])
        h_long_dm        = Paragraph('<b>Long_dm</b>',styles['BodyText'])
        h_id            = Paragraph('<b>ID</b>',styles['BodyText'])
        h_tipo           = Paragraph('<b>Tipo de servicio</b>',styles['BodyText'])
        cotizacion_datos = [[h_modelo,h_no_serie,h_especificacion,h_long_dm,h_id,h_tipo]]

        modelos = cotizacion.maquinas.values_list('modelo', flat=True)
        nos_serie = cotizacion.maquinas.values_list('no_serie', flat=True)
        mppes = cotizacion.maquinas.values_list('mppe', flat=True)
        mppls = cotizacion.maquinas.values_list('mppl', flat=True)
        #print mppls
        x = cotizacion.maquinas.values_list('rango_x', flat=True)
        y = cotizacion.maquinas.values_list('rango_y', flat=True)
        z = cotizacion.maquinas.values_list('rango_z', flat=True)
        servicios = cotizacion.servicio.values_list('servicio', flat=True)
        print 'modelos = %s \n servicios = %s \n'%(len(modelos),len(servicios))
        if len(modelos) >= len(servicios):
            for i in range(len(modelos)):
                cotizacion_datos.append([modelos[i],nos_serie[i],str(str(mppes[i])+'+L/'+str(mppls[i])),'%s, %s, %s'%(x[i],y[i],z[i]),'',''])
                #print cotizacion_datos
            for i in range(len(servicios)):
                cotizacion_datos[i+1][5] = servicios[i]
        elif len(servicios) > len(modelos):
            for i in range(len(servicios)):
                cotizacion_datos.append(['','','','','',servicios[i]])
            
            for i in range(len(modelos)):
                cotizacion_datos[i+1][0] = modelos[i]
                cotizacion_datos[i+1][1] = nos_serie[i]
                cotizacion_datos[i+1][2] = str(str(mppes[i])+'+L/'+str(mppls[i]))
                cotizacion_datos[i+1][3] = '%s, %s, %s'%(x[i],y[i],z[i])
                cotizacion_datos[i+1][4] = ''   


                    	
            
        tabla = Table(cotizacion_datos , style=[('GRID',(0,0),(5,len(cotizacion_datos)),2,colors.black),])
        id_lista = ListaPrecios.objects.all().aggregate(Max('id'))
        precio_unitario = ListaPrecios.objects.filter(id=id_lista['id__max'])
        print precio_unitario
        precios = []
        if not cotizacion.importe:
            if cotizacion.horas:
                precios.append(float(cotizacion.horas)*precio_unitario[0].horas)
                #print 'Horas'
            if cotizacion.horas_extra:
                precios.append(float(cotizacion.horas_extra)*precio_unitario[0].horas_extra)
            if cotizacion.contacto.cliente.horas:     
                precios.append(float(cotizacion.contacto.cliente.horas)*precio_unitario[0].horas_viaje)
                #print 'Horas Viaje'
            if cotizacion.viajes:     
                precios.append(int(cotizacion.viajes)*precio_unitario[0].kilometros * cotizacion.contacto.cliente.kilometros)
                #print 'Viajes'    
            if cotizacion.hotel:     
                precios.append(int(cotizacion.hotel)*precio_unitario[0].hotel )
            if cotizacion.manuales:     
                precios.append(int(cotizacion.manuales)*precio_unitario[0].manuales )
            if cotizacion.traslados:     
                precios.append(int(cotizacion.traslados)*precio_unitario[0].traslados)
            if cotizacion.aviones:     
                precios.append(int(cotizacion.aviones) *precio_unitario[0].aviones )  
            if cotizacion.sobre_equipaje:     
                precios.append(int(cotizacion.sobre_equipaje)*precio_unitario[0].sobre_equipaje  )  
            if cotizacion.renta_auto:     
                precios.append(int(cotizacion.renta_auto) *precio_unitario[0].renta_auto )  
            if cotizacion.papeleria:     
                precios.append(int(cotizacion.papeleria) *precio_unitario[0].papeleria )
            print precios               
            total = 0
            for precio in precios:
                total += precio	
            print cotizacion.importe    
        
            cotizacion.importe = total
            cotizacion.save()
            print 'adentro'    
        importe_letra = moneda.to_word(float(cotizacion.importe))
        importe = Paragraph('''
        	                <para align=right><b>(%s dolares)     $%s</b></para>
        	                ''' % (importe_letra,cotizacion.importe),styles['Heading3'])
        horas = int(cotizacion.horas)
        if cotizacion.horas_extra:
            horas += int(cotizacion.horas_extra)	
        texto = Paragraph(u'''
        	              <para align=left><font size=8>Ampara hasta <b>%s</b> horas de servicio.<br></br>
        	              Horarios 8:00 hrs -16:00 hrs Sujeto a cambios a desicion de Ingeniero de servicio.
        	              Si se encuentran partes danadas o en mal estado , se realizara una cotizacion por estas partes y por su instalacion
        	              para ser colocadas en vista posterior y terminacion del trabajo.
        	              Para calibracion espacial y repetitibilidad , se seguira el procedimiento BMI-10360-2 el cual se basa en la norma
        	              ISO-10360-2 SECCION 6.3.3. Agregar la seccion 6.5 se hara por requerimiento especifico del cliente y que la
        	              cotizacion asi lo indique.
        	              Para MPE se seguira el procedimiento BMI- 10360-5 el cual se basa en la norma ISO-10360-5. EL reporte de calibracion y calculo de incertidumbre 
        	              sera hecho bajo el procedimiento interno BMI-035 el cual
        	              se basa en la norma ISO+TS+23165-2006.
        	              Esta cotizacion tiene vigencia de 30 dias y su precio esta en dolares americanos
        	              Terminos de pago : 30 dias desde fecha de factura
        	              Esta cotizacion no incluye piezas , solo servicio.<br></br></font>
        	              </para>

        	              ''' %horas, styles['BodyText'])
        orden_compra = Paragraph('''
                                 <para align=center spaceb=3><font size=8>Si nos favorece la propuesta agradecemos colocar su orden de compra a</font>
                                 </para>
        	                     ''',styles['BodyText'])
        pagos = Paragraph('''
        	              <para align=center spaceb=3><font size=8>Pongo a su disposicion los datos para hacer transferencias bancarias para pagos</font>
        	              </para>
        	              ''',styles['BodyText'])
        orden_datos =  Paragraph('''<para align=center><font size=8>BORBOLLA METROLOGY , INC<br></br>
                                 319 East Coma Avenue
                                 Hidalgo Texas 78557 <br></br>
                                 TAX ID 20-0048198<br></br>
                                 email : servicio_po@borbollametrology.com.mx
                                 </font>
                                 </para>
        	                     ''',styles['BodyText'])
        transferencias_datos=Paragraph('''<para align=center spaceb=3><font size=8>International Bank of Commerce<br></br>
                                       One South Broadway , McAllen TX 78505<br></br>
                                       Borbolla Metrology Inc.<br></br>
                                       600 1029830 numero ABA : 114902528</font><br></br>
                                       </para>
        	                           ''',styles['BodyText'])
        datos_pagos = [[orden_compra , pagos],[orden_datos , transferencias_datos]]
        tabla_pagos = Table(datos_pagos , style=[('GRID',(0,0),(2,1),2,colors.black),
        	                                     ('ALIGN',(0,0),(1,1),'CENTER'),])
        
        mandar_email = Paragraph('''
        	                     <para align=left><font size=8>Una vez hecha cualquier transferencia favor de enviar una copia al email: <b>servicio_po@borbollametrology.com.mx</b> para su seguimiento</font>
        	                     </para>
        	                     ''',styles['BodyText'])
        observacion = cotizacion.observaciones
        firma = Paragraph('''<para align=center><font size=8>Atentamente<br></br>Ing. Luis Manuel Borbolla</font>
        	                 </para>''',styles['BodyText'])
                  
        elements.append(self.direccion)
        elements.append(cotizacion_fecha)
        elements.append(datos_cliente)
        elements.append(texto_pre)
        elements.append(tabla)
        if len(cotizacion_datos) > 5:
            elements.append(PageBreak())	
        elements.append(importe)
        elements.append(texto)
        elements.append(tabla_pagos)
        elements.append(mandar_email)
        if observacion:
            observaciones = Paragraph('''
        	                          <para align=left> OBSERVACIONES : <font color=red>%s</font></para> 
        	                          '''%observacion,styles['BodyText'])

            elements.append(observaciones) 

        elements.append(firma)         
        doc.build(elements , 
        	      onFirstPage=self._header_footer, 
        	      onLaterPages=self._header_footer,
        	      canvasmaker = NumberedCanvas,)
        pdf = buffer.getvalue()
        buffer.close()

        return pdf   

    def print_servicio(self , id=1):
    	import datetime

        buffer = self.buffer
        doc = self.doc
        
        styles = self.styles
        servicio = Ordenes_de_servicio.objects.get(pk=id)
        cliente = Paragraph('''
        	                <para align=left>Empresa :<font size=12> <b>%s</b></font>
        	                </para>
        	                ''' % servicio.cotizacion.contacto.cliente.nombre.upper(),styles['BodyText'])
        Orden_servicio =  Paragraph('''
                            <para align=left><b>Orden Servicio :</b>%s
                            </para>
        	                ''' % (servicio.id ), styles['BodyText'])
        PO =  Paragraph('''
                            <para align=left><b>PO : </b>%s
                            </para>
        	                ''' % (servicio.orden_compra ), styles['BodyText'])
        fecha_servicio =  Paragraph('''
                            <para align=right><b>Fecha :</b>%s
                            </para>
        	                ''' % (servicio.fecha), styles['BodyText'])


        cotizacion_numero = '%s-%s%s%s' % (servicio.cotizacion.id*10+80000,servicio.cotizacion.fecha.month/10,servicio.cotizacion.fecha.month%10 , servicio.cotizacion.fecha.year-2000)
        print cotizacion_numero
        cotizacion = Paragraph('''<para align=right><b>COTIZACION :</b>%s
        	                    </para>''' % cotizacion_numero,styles['BodyText'])
        ingenieros = servicio.ingeniero.values_list('nombre', flat=True)
        servicios = servicio.cotizacion.servicio.values_list('servicio', flat=True)

        inges_string = ''
        for nombre in ingenieros:
            inges_string += nombre+'<br></br>'
        servicios_string = ''
        for service in servicios:
            servicios_string += service+'<br></br>'    	

        
        
        
        dias = math.ceil(servicio.cotizacion.horas/8.0)
        limite = servicio.fecha+datetime.timedelta(days=dias)
        print 'Fecha = %s dias = %s limite=%s'%(servicio.fecha,dias,limite)
        datos = Paragraph('''
        	              <para align=left>
        	              <font size=11><b>Ingeniero(s) : </b></font><br></br>%s<br></br>
        	              <font size=11><b>Servicio(s) : </b></font><br></br>%s<br></br>
        	              <font size=11><b>Direccion : </b></font>%s<br></br>
        	              <font size=11><b>Ciudad : </b></font>%s<br></br>
        	              <font size=11><b>Estado : </b></font>%s<br></br>
        	              <font size=11><b>Contacto : </b></font>%s<br></br>
        	              <font size=11><b>Telefono : </b></font>%s<br></br>
        	              <font size=11><b>Email : </b></font>%s<br></br>
        	              <font size=11><b>Horas : </b></font>%s<br></br>
        	              <font size=11><b>Dias : </b></font>%s<br></br>
        	              <font size=11><b>Servicio desde</b> %s <b>al </b> %s </font><br></br>
        	              </para>
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
        	              	   ),styles['BodyText'])
        
        data= [[cliente,],[[Orden_servicio,PO,fecha_servicio]],[[cotizacion,datos,]]]
 
        t=Table(data , style=[('GRID',(0,0),(1,2),2,colors.black),])
        #t._argW[3]=1.5*inch
        datos_final = Paragraph('''
        	                    <para align=left>servicio_po@borbollametrology.com.mx <br></br>
        	                    Tel : 844 412-88-68<br></br>
        	                    whatsapp : 8444164051
        	                    </para>
        	                    ''',styles['BodyText'])
 
        


        #tabla = [[cliente],[orden]]
        #tabla_servicios = Table(tabla , style=[('GRID',(0,0),(0,0),2,colors.black)])
        
        elements = [t,datos_final]
        
        doc.build(elements , 
        	      onFirstPage=self._header_servicio, 
        	      onLaterPages=self._header_servicio,
        	      canvasmaker = NumberedCanvas,)
        pdf = buffer.getvalue()
        buffer.close()

        return pdf	 

    def print_factura(self , id = 1):
        import datetime
        buffer = self.buffer
        doc = self.doc
        styles = self.styles
        factura = Factura.objects.get(pk=id)

        direccion = Paragraph('''
                              <para align=left><font size=8>319 East Coma Ave<br></br>
                              Hidalgo Texas USA<br></br>
                              Tel : +52 1 (844) 4 12 88 68. (844) 4 10 36 06<br></br>
                              servicio_po@borbollametrology.com.mx<br></br>
                              www.borbollametrology.com</font>
                              </para>
    	                      ''',self.styles['BodyText'])
        ordering = Paragraph('''
                              <para align=left><font size=8><b>ORDERING</b></font>
                              </para>
    	                      ''',self.styles['BodyText'])
        service_date = Paragraph('''
                              <para align=left><font size=8><b>SERVICE DATE</b></font>
                              </para>
    	                      ''',self.styles['BodyText'])
        customer = Paragraph('''
                              <para align=left><font size=8><b>CUSTOMER</b></font>
                              </para>
    	                      ''',self.styles['BodyText'])
        contact = Paragraph('''
                              <para align=left><font size=8><b>CONTACT</b></font>
                              </para>
    	                      ''',self.styles['BodyText'])

        data1 = [[ordering,'Sales Person',service_date,customer,contact],
                  [factura.orden_servicio.id,'',factura.orden_servicio.fecha_servicio,factura.orden_servicio.cotizacion.contacto.cliente.id,factura.orden_servicio.cotizacion.contacto.nombre]]
        tabla1=Table(data1 , style=[('GRID',(0,0),(4,1),2,colors.black),])
        
        purchase_order = Paragraph('''
                              <para align=left><font size=8><b>PURCHASE ORDER : %s</b></font>
                              </para>
    	                      '''%factura.orden_servicio.orden_compra,self.styles['BodyText'])
        payment_terms = Paragraph('''
                              <para align=left><font size=8><b>PAYMENT TERMS : %s</b></font>
                              </para>
    	                      '''%factura.terminos_pago,self.styles['BodyText'])
        data2 = [[purchase_order,payment_terms]]
        tabla2=Table(data2 , style=[('GRID',(0,0),(4,1),2,colors.black),])

        ship_to =Paragraph('''
                              <para align=left><font size=8><b>SHIP TO</b><br></br>
                              %s<br></br>
                              %s<br></br>
                              %s %s<br></br>
                              <b>Email :</b> %s<br></br>
                              <b>Tel :</b> %s Ext : %s<br></br>
                              <b>Zip Code :</b> %s<br></br></font>
                              </para>
    	                      '''%(factura.orden_servicio.cotizacion.contacto_servicio.cliente.nombre,
    	                      	   factura.orden_servicio.cotizacion.contacto_servicio.cliente.direccion,
    	                      	   factura.orden_servicio.cotizacion.contacto_servicio.cliente.ciudad,
    	                      	   factura.orden_servicio.cotizacion.contacto_servicio.cliente.estado,
    	                      	   factura.orden_servicio.cotizacion.contacto_servicio.email,
    	                      	   factura.orden_servicio.cotizacion.contacto_servicio.telefono,
    	                      	   factura.orden_servicio.cotizacion.contacto_servicio.extension,
    	                      	   factura.orden_servicio.cotizacion.contacto_servicio.cliente.cp),self.styles['BodyText'])

        bill_to =Paragraph('''
                              <para align=left><font size=8><b>BILL TO</b><br></br>
                              %s<br></br>
                              %s<br></br>
                              %s %s<br></br>
                              <b>Email :</b> %s<br></br>
                              <b>Tel :</b> %s Ext : %s<br></br>
                              <b>Zip Code :</b> %s<br></br></font>
                              </para>
    	                      '''%(factura.orden_servicio.cotizacion.contacto.cliente.nombre,
    	                      	   factura.orden_servicio.cotizacion.contacto.cliente.direccion,
    	                      	   factura.orden_servicio.cotizacion.contacto.cliente.ciudad,
    	                      	   factura.orden_servicio.cotizacion.contacto.cliente.estado,
    	                      	   factura.orden_servicio.cotizacion.contacto.email,
    	                      	   factura.orden_servicio.cotizacion.contacto.telefono,
    	                      	   factura.orden_servicio.cotizacion.contacto.extension,
    	                      	   factura.orden_servicio.cotizacion.contacto.cliente.cp),self.styles['BodyText'])


        data3 = [[bill_to,ship_to]]
        tabla3=Table(data3 , style=[('GRID',(0,0),(1,1),2,colors.black),])
        servicios = factura.orden_servicio.cotizacion.servicio.values_list('servicio', flat=True)
        headers = ['ITEM','DESCRIPTION','QTY','TOTAL']
        header_p = []
        for nombre in headers:
            header_p.append(Paragraph('''
                              <para align=center><font size=8><b>%s</b></font>
                              </para>
    	                      '''%nombre,self.styles['BodyText']))	

        descripcion_texto = ''
        item = 1
        qty=''
        item_texto = ''
        for servicio in servicios:
            descripcion_texto += servicio.upper()+'<br></br>'
            item_texto += str(item)+'<br></br>'
            qty += '1<br></br>'
            item+=1

        descripcion = Paragraph('''
                              <para align=left><font size=8><b>%s</b></font>
                              </para>
    	                      '''%descripcion_texto,self.styles['BodyText'])
        item = Paragraph('''
                              <para align=center><font size=8><b>%s</b></font>
                              </para>
    	                      '''%item_texto,self.styles['BodyText'])
        qty = Paragraph('''
                              <para align=center><font size=8><b>%s</b></font>
                              </para>
    	                      '''%qty,self.styles['BodyText'])
        data4 = [header_p,]

        data4.append([item,descripcion,qty,'',])
        amount = Paragraph('''
                              <para align=right><font size=10><b>Total : </b>$%s</font>
                              </para>
    	                      '''%factura.orden_servicio.cotizacion.importe,self.styles['BodyText'])
        #data4.append(['','','','','$'+str(factura.orden_servicio.cotizacion.importe)])    
        tabla4=Table(data4 , style=[('GRID',(0,0),(4,len(data4)),2,colors.black),],colWidths=[50,338,50,50])	

       
        #data5 = 
        elements = [direccion,tabla1,tabla2,tabla3,tabla4,amount]

        doc.build(elements , 
        	      onFirstPage=self._header_factura, 
        	      onLaterPages=self._header_factura,
        	      canvasmaker = NumberedCanvas,)
        pdf = buffer.getvalue()
        buffer.close()

        return pdf



