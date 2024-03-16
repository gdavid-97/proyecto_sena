from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from .forms import  forms_sugerencia, forms_historial

from django.contrib.auth import authenticate, login, get_user_model, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.conf import settings
from django.template import RequestContext
from .models import usuario_historial

api_key_maps = settings.GOOGLE_MAPS_API_KEY

def principal(request):
    context={
        
    }
    response = render(request,"index.html", context)
    return response

def acerca(request):
    context={
        'api_key': api_key_maps      
    }
    response = render(request,"Contactos.html", context)
    return response

def iniciar_sesion(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid:
            temp_usuario = request.POST['usuario']
            temp_password = request.POST['contrasena']
            usuario = authenticate(username=temp_usuario, password=temp_password)
            if usuario is not None:
                login(request, usuario)
                return redirect('home')
            else:
                messages.error(request,'Usuario no existe')
        else:
            messages.error(request,'Informacion incorrecta')
    
    form = AuthenticationForm(request, data=request.POST)
    return render(request,"Iniciar_sesion.html", {"form":form})


def crear_cuenta(request):
    if request.method == 'POST':

        User = get_user_model()

        for name in request.POST:
            print("{}: {}".format(name,request.POST.getlist(name)))
        temp_password1 = request.POST['contrasena']
        temp_password2 = request.POST['contrasena_repetida']
        temp_usuario = request.POST['usuario']
        temp_email = request.POST['email']

        if temp_password1 == temp_password2:
            if User.objects.filter(email=temp_email).exists():
                messages.warning(request, 'Email ya registrado')
                return redirect('crear_cuenta')
            elif User.objects.filter(username=temp_usuario).exists():
                messages.warning(request, 'Usuario ya utilizado')
                return redirect('crear_cuenta')
            else:
                user = User.objects.create_user(username=temp_usuario, email=temp_email, password=temp_password1, is_staff=False)
                
                user.save()
                messages.success(request, 'Usuario registrado')
                #user = authenticate(username=username, password=raw_password)
                login(request, user)

                #return redirect('home')
            
        else:
            messages.warning(request, 'contraseñas no coinciden')
            return redirect('crear_cuenta')

    context={
        
    }

    response = render(request,"crear_cuenta.html", context)
    return response

def sugerencia(request):
    if request.method == 'POST':
        for name in request.POST:
            print("{}: {}".format(name,request.POST.getlist(name)))
        form = forms_sugerencia(request.POST)
        print(form.is_valid())
        if form.is_valid():
            form.save()
    else:
        form = forms_sugerencia()

    return render(request, "sugerencias.html", {"method": form})

def cerrar_sesion(request):

    logout(request)
    return redirect('home')


def verificar_usuario(request, nombre_usuario, clave):
    if request.method == 'GET':
        User = get_user_model()
        if nombre_usuario == "admin":
            return HttpResponse("<h1>no existe</h1>")
        d = User.objects.get(username=nombre_usuario)
        if d.check_password(clave):
            return HttpResponse("<h1>existe</h1>")
        else:
            return HttpResponse("<h1>no existe</h1>")
    
def agregar_historial(request, informacion):
    if request.method == 'GET':
        User = get_user_model()
        print(informacion)
        print(request.GET.urlencode())
        temp = informacion
        temp = temp.split("%")
        d = User.objects.get(username=temp[1])
        print(d.pk)
        return HttpResponse("<p>hola</p>")

def tomar_historial(request, informacion):
    if request.method == 'GET':
        User = get_user_model()
        print(informacion)


def crud(request):
    User = get_user_model()
    
    s = request.POST
    f=s.getlist("btneditar")
    print(f)
        
    if request.method == 'POST':
        temp = request.POST['drop1']
        tempuser = User.objects.get(username=temp)
        try:
            tempuser1 = usuario_historial.objects.all()
            tempuser1 = tempuser1.filter(usuario_id=tempuser.pk)

            context={
                'userlist':User.objects.all(),
                'userselect': tempuser1
            }
            response = render(request,"crud.html", context)
        except Exception as e:
            print(f'{type(e).__name__}: {e}')
    else:
        context={
            'userlist':User.objects.all()
        }
        response = render(request,"crud.html", context)

    return response

def custom_404(request, exception):
    return render(request, '404.html', status=404)

def custom_400(request, exception):
    return render(request, '400.html', status=400)

def custom_500(request, exception):
    return render(request, '500.html', status=500)