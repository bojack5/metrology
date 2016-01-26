from django.shortcuts import render , render_to_response
from django.contrib.auth import logout , authenticate, login
from django.http import HttpResponseRedirect , HttpResponse

from auth.forms import LoginForm , RegisterForm
# Create your views here.


def login_view(request):
    logged_in = request.user.is_authenticated() 
    if not logged_in:

        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                usuario    = request.POST['usuario']
                contrasena = request.POST['contrasena']	
                usuario    = authenticate(username = usuario , password = contrasena)
                if usuario is not None:
                    if usuario.is_active:
                        login(request , usuario)
                        return HttpResponseRedirect('/inicio/')
                    else:
                        return render(request , 'contacto_formulario.html' , {'subtitulo' : 'Usuario no esta activo' ,'title' : 'Error | Borbolla Metrology' , 'texto': 'El usuario no esta activo , favor de ponerse en contacto con el administrador '})
                else:
                    return render(request , 'contacto_formulario.html' , {'subtitulo' : 'Error de Autentificacion' ,'title' : 'Error | Borbolla Metrology' , 'texto': 'El usuario o contrasena son incorrectos , favor de introducirlos nuevamente'})	
        else:
            form = LoginForm()
        return render(request , 'contacto_formulario.html' , {'subtitulo' : 'Formulario de Acceso' ,'form': form ,'title' : 'Login | Borbolla Metrology' , 'texto': 'Ingrese su usuario y contrasena '})                    
    
    return render(request , 'contacto_formulario.html' , {'subtitulo' : 'Formulario de Acceso'  ,'title' : 'Login | Borbolla Metrology' , 'texto': 'Ya estas Autentificado '})    	

def logout_view(request):
    logout(request)          	
    return HttpResponseRedirect('/inicio/')    


