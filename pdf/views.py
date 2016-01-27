from django.shortcuts import render
from io import BytesIO
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from datos_pdf import Datos
from generar import Impresion
from sistema.models import Cotizacion , Ordenes_de_servicio , Factura
from mail_inges import Mandar
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response,render
from django.contrib.auth.decorators import login_required
import datetime
import json
@login_required
def print_cotizacion(request , id):
    # Create the HttpResponse object with the appropriate PDF headers.
    id = int(id)
    cotizacion = Cotizacion.objects.get(pk=id)
    nombre = '%s|%s-%s%s%s'%(cotizacion.contacto.nombre,cotizacion.id*10+80000,cotizacion.fecha.month/10,cotizacion.fecha.month%10 , cotizacion.fecha.year-2000)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="%s.pdf"'%nombre
    

    buffer = BytesIO()
    
    reporte = Impresion(buffer , 'Letter')
    print id
    pdf = reporte.print_cotizaciones(id=id)

    response.write(pdf)
       
    return response
@login_required
def print_servicio(request , id):
    id = int(id)
    servicio = Ordenes_de_servicio.objects.get(pk=id)
    nombre   = '%s|%s'%(servicio.cotizacion.contacto.cliente.nombre,servicio.id)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="%s.pdf"'%nombre

    buffer = BytesIO()

    reporte = Impresion(buffer , 'Letter')
    reporte.doc.topMargin = 100
    reporte.doc.leftMargin = 72

    pdf = reporte.print_servicio(id=id)
    response.write(pdf)

    return response
@login_required
def mail_ingenieros(request , id):
    id = int(id)
    login        = request.user.is_authenticated()
    orden = Ordenes_de_servicio.objects.get(pk=id)
    if orden.mail_enviado:
        return render(request,'contacto_formulario.html', {'subtitulo' : 'Correo ya enviado a los ingenieros' ,
                                                           'login' : login ,
                                                           'title' : 'Envio de servicio | Borbolla Metrology' ,
                                                           'texto' : 'El correo que intentas mandar , ya fue enviado a los ingenieros , el dia %s si deseas volverlo a enviar , contacta a un administrativo , o manda un correo a luis@4suredesign.com'%orden.fecha_mail_enviado ,
                                                          })

    else:
        Mandar(id)
        orden.mail_enviado=1
        orden.fecha_mail_enviado = datetime.datetime.now()
        orden.save()


    return render(request,'contacto_formulario.html', {'subtitulo' : 'Se ha enviado la orden a los ingenieros' ,
                                                           'login' : login ,
                                                           'title' : 'Envio de servicio | Borbolla Metrology' ,
                                                           'texto' : 'EL correo de la orden se ha enviado correctamente a los ingenieros !',
                                                          })
@login_required
def print_factura(request , id):
    id = int(id)
    print id
    factura = Factura.objects.get(pk=id)
    nombre = 'Factura-%s|%s'%(factura.id,factura.fecha)
    print nombre
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="%s.pdf"'%nombre
    
    buffer = BytesIO()


    reporte = Impresion(buffer , 'Letter')
    reporte.doc.topMargin = 100
    reporte.doc.leftMargin = 40 

    pdf = reporte.print_factura(id=id)
    response.write(pdf)

    return response
@login_required
def impresion(request):
    cotizaciones = ''
    if request.method == 'POST':
        if 'cotizacion_id' in request.POST:
            tipo = 'cotizacion'
            cotizacion_id = request.POST['cotizacion_id']
            print cotizacion_id
            if cotizacion_id == '':
                return render(request , 'contacto_formulario.html',{'subtitulo' : 'Porfavor Selecciona una %s'%tipo,'login':request.user.is_authenticated(),'title':'Error!','texto':'presiona Atras para regresar '})
            print 'hola'
            return HttpResponseRedirect('/cotizacion-%s/'%cotizacion_id)

        if 'servicio_id' in request.POST:
            tipo = 'orden de servicio'
            servicio_id = request.POST['servicio_id']
            if servicio_id == '':
                return render(request , 'contacto_formulario.html',{'subtitulo' : 'Porfavor Selecciona una %s'%tipo,'login':request.user.is_authenticated(),'title':'Error!','texto':'presiona Atras para regresar '})
            if request.POST['action'] == 'imprimir':
                return HttpResponseRedirect('/servicio-%s/'%servicio_id)
            elif request.POST['action'] == 'Enviar a Ingenieros':

                return HttpResponseRedirect('/mail-%s/'%servicio_id)
                        

        if 'factura_id' in request.POST:
            tipo = 'factura-'
            factura_id = request.POST['factura_id']
            if factura_id == '':
                return render(request , 'contacto_formulario.html',{'subtitulo' : 'Porfavor Selecciona una %s'%tipo,'login':request.user.is_authenticated(),'title':'Error!','texto':'presiona Atras para regresar '})
            return HttpResponseRedirect('/factura-%s/'%factura_id)

                    
            
    else:
        cotizaciones = Cotizacion.objects.all()
        servicios    = Ordenes_de_servicio.objects.all()
        facturas     = Factura.objects.all()
        formulario   = True
        subtitulo    ='Impresion de Cotizaciones , ordenes de servicio , y/o Facturas' 
        login        = request.user.is_authenticated()
        title        = 'Impresion | Borbolla Metrology' ,
        texto        = 'Escoja la opcion que desee imprimir o enviar' 
        print facturas
    return render(request,'contacto_formulario.html', {'cotizaciones':cotizaciones ,
                                                       'servicios' : servicios ,
                                                       'facturas'  : facturas ,
                                                       'formulario' : formulario ,
                                                       'subtitulo' : subtitulo ,
                                                       'login' : login ,
                                                       'title' : title ,
                                                       'texto' : texto ,
                                                       })



def get_cotizaciones(request):
    data = Cotizacion.objects.all()
    return HttpResponse(json.dumps(data),'application/json')
        








