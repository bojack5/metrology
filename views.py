from django.http import HttpResponse
from django.shortcuts import render_to_response,render
from contacto.forms import ContactoForm
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.contrib.gis.geoip import GeoIP


import datetime


'''A PARTIR DE AKI SON VIEWS DEL SISTEMA '''

def inicio(request):
    inicio = True
    title = 'inicio | Borbolla Metrology'
    texto = '''En Borbolla Metrology nos esforzamos por ofrecerle los mejores proveedores en el area de metrologia dimensional en Mexico, y poder asi brindarle la mejor solucion en medicion. Con equipos de medicion nuevos y seminuevos podemos llegar a todos los niveles de presupuesto. El concepto nacio desde finales del 96 donde se vio la necesidad de ofrecer servicios con alto grado de profesionalismo y servicio al cliente. Desde entonces hemos tratado de tener solo los mejores proveedores en nuestra lista, para poder de igual manera soportar sus necesidades de inspeccion Actualmente tenemos presencia en diferentes puntos de la Republica Mexicana, ya sea con oficinas o representantes que cubren el area. '''
    login = request.user.is_authenticated()
    print login
        
    return render_to_response('inicio.html', locals())

def servicios(request):
    inicio = False
    title = 'servicios | Borbolla Metrology'
    texto = 'EN este apartado iran los servicios que ofrecemos'
    login = request.user.is_authenticated()
    return render_to_response('inicio.html', locals())

def nosotros(request):
    inicio = False
    title = 'Nosotros | Borbolla Metrology'
    texto = 'Apartado donde habra informacion de la compania'
    login = request.user.is_authenticated()
    return render_to_response('inicio.html', locals())



def contacto(request):
    
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            meta = request.META
            g = GeoIP()
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')  
            print ip                      
            info = g.city(ip)
            coordenadas = g.lat_lon(ip)
            datos = form.cleaned_data
            coordenadas = '''\nCodigo de Continente : %s\n
                          \nCodigo Pais : %s\n
                          \nPais : %s\n
                          \nRegion : %s\n
                          \nCiudad : %s\n
                          \nCodigo Postal : %s\n
                          \ncoordenadas : %s'''%(  info['continent_code'] ,
                                                 info['country_code'] , 
                                                 info['country_name'] ,
                                                 info['region'] ,
                                                 info['city'] , 
                                                 info['postal_code'] ,
                                                 coordenadas )
            metadata = str('\n\n\n Favor de no responder al servidor , responder al email del cliente \n\nEmail del cliente : %s\nEmpresa : %s \n\nMETADATA\n\nNavegador : %s\nDireccion : %s\n' % (datos['email'],datos['empresa'] , meta['HTTP_USER_AGENT'] , meta['REMOTE_ADDR'] ,) )
            #print metadata                
            send_mail(str('MENSAJE DE SERVIDOR |'+datos['asunto']) , 
                str(datos['mensaje']+metadata+coordenadas), 
                'luis@4suredesign.com',
                ['luis@4suredesign.com','servicio_po@borbollametrology.com.mx','gabyborbolla@hotmail.com'])
            
            
            return HttpResponseRedirect('/contacto/gracias/')
    else:
        form = ContactoForm()
    #return render(request , 'formulario_contacto.html' ,{'form':form})
    return render(request , 'contacto_formulario.html' , {'subtitulo' : 'Formulario de contacto' ,
                                                          'login': request.user.is_authenticated(),
                                                          'form': form ,'title' : 'Contacto | Borbolla Metrology' ,
                                                          'texto': 'Porfavor llena el siguiente formulario , es importante que incluyas un correo real , ya que por este medio nos comunicaremos con tigo',
                                                          })                    
    
def contacto_gracias(request):
    title = 'Gracias | Borbolla Metrology'
    subtitulo = 'Tu mensaje ha sido enviado a nuestras operadoras!'
    texto      = 'Responderemos lo mas rapido posible, gracias por contactarnos!'
    login      = request.user.is_authenticated()

    return render_to_response('contacto_formulario.html', locals())

    



