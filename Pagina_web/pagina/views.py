from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from .forms import  forms_sugerencia

from django.contrib.auth import authenticate, login, get_user_model, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.conf import settings
from django.template import RequestContext
from .models import usuario_historial, historial

import datetime

from reportlab.pdfgen import canvas 
from reportlab.pdfbase.ttfonts import TTFont 
from reportlab.pdfbase import pdfmetrics 
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, letter

from reportlab.platypus.tables import Table

from reportlab.lib.units import inch, mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

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
            messages.success(request, 'Comentario Registrado')
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
        d = User.objects.get(username=nombre_usuario)
        clave = int(clave)
        if d.check_password(clave) == True:
            return HttpResponse("<h1>existe</h1>")
        else:
            return HttpResponse("<h1>no existe</h1>")
    
def agregar_historial(request, nombre_usuario, clave, informacion):
    if request.method == 'GET':
        informacion = informacion.replace("%20"," ")
        User = get_user_model()
        tempuser = User.objects.get(username=nombre_usuario)
        if tempuser.check_password(clave):
            temph = historial(busqueda = informacion, usuario = tempuser)
            temph.save()
            tempuh= usuario_historial(historial_id=temph.pk,usuario_id=tempuser.pk)
            tempuh.save()

            return HttpResponse("<h1>si</h1>")
    
            
            

def tomar_historial(request, informacion):
    if request.method == 'GET':
        User = get_user_model()
        print(informacion)


def crud(request):
    User = get_user_model()
        
    if request.method == 'POST':
        try:
            s = request.POST
            
            f = s.getlist('btnform1')
            m = len(f)
            if m != 0:
                temp = s.getlist('drop1')


            temp = request.POST['drop1']
            tempuser = User.objects.get(username=temp)

            tempuser3 = usuario_historial.objects.all()
            tempuser1 = tempuser3.filter(usuario_id=tempuser.pk)

            

            f = s.getlist("btneliminarusuario")
            m = len(f)
            if m != 0:
                temporal = user_eliminar(f[0])
                if temporal == True:
                    messages.success(request, 'Usuario eliminado')

            f = s.getlist("btneditar")
            m = len(f)

            if m != 0:
                t = s.getlist(f"textarea")
                temporal1= str(f[0])
                l=temporal1.split("/")
                temporal= crud_editar(l[0], t[int(l[1])-1])
                if temporal == True:
                    messages.success(request, 'Busqueda editada')

            f = s.getlist("btneliminar")
            m = len(f)
            if m != 0:
                temporal=crud_eliminar(f[0])
                if temporal == True:
                    messages.success(request, 'Busqueda eliminada')

            f=s.getlist("btnimprimir1")
            m = len(f)
            if m != 0:
                temporal = crud_imprimir(tempuser1)
                if temporal == True:
                    messages.success(request, 'Informe realizado')

            temp = s.getlist('drop1')
            temp = temp[0]
            t = User.objects.all().exclude(id=1)
            n = 0
            m = 0
            for x in t:
                m += 1
                k = str(x)
                temp1 = k.replace("  ","")
                temp2 = temp.replace("  ","")
                if temp1 == temp2:
                    n = m
                    print(m)


            context={
                'userlist':User.objects.all().exclude(id=1),
                'userselect': tempuser1,
                'temp': temp,
                'vuelta': n
            }
            response = render(request,"crud.html", context)
        except Exception as e:
            print(f'{type(e).__name__}: {e}')
    else:
        context={
            'userlist':User.objects.all().exclude(id=1)
        }
        response = render(request,"crud.html", context)

    return response

def crud_eliminar(id):
    tempuser1 = usuario_historial.objects.all()
    tempuser1 = tempuser1.get(id=id)
    temp = tempuser1.historial.pk
    tempuser1.delete()

    tempuser2 = historial.objects.all()
    tempuser2 = tempuser2.get(id=temp)
    tempuser2.delete()
    return True

def user_eliminar(id):

    User = get_user_model()

    tempuser1 = usuario_historial.objects.all()
    tempuser1 = tempuser1.filter(usuario_id=id)

    for x in tempuser1:
        tempuser2 = historial.objects.all()
        tempuser2 = tempuser2.filter(id=x.id)
        tempuser2.delete()

    tempuser1.delete()

    tempuser3 = User.objects.get(id=id)
    tempuser3.delete()

    return True

def crud_editar(id, texto):
    tempuser1 = usuario_historial.objects.all()
    tempuser1 = tempuser1.get(id=id)
    temp = tempuser1.historial.pk

    tempuser2 = historial.objects.all()
    tempuser2 = tempuser2.filter(id=temp).update(busqueda=texto)

    return True

def crud_imprimir(lista):

    doc = SimpleDocTemplate("form_letter.pdf",pagesize=letter,
                        rightMargin=72,leftMargin=72,
                        topMargin=72,bottomMargin=18)
    

    fileName = 'informe.pdf'
    documentTitle = 'informe'
    title = 'Historial'
    subTitle = 'Busquedas'

    pdf = canvas.Canvas(fileName) 
    pdf.setTitle(documentTitle)
    
    pdf.setFont("Courier-Bold", 36) 
    pdf.drawCentredString(300, 770, title)

    pdf.setFillColorRGB(0, 0, 255) 
    pdf.setFont("Courier-Bold", 24) 
    pdf.drawCentredString(290, 720, subTitle)

    pdf.line(30, 710, 550, 710) 
    
    text = pdf.beginText(40, 680) 
    text.setFont("Courier", 18) 
    text.setFillColor(colors.red) 

    datos = []
    datos.append("Usuario")
    datos.append("Fecha")
    datos.append("Busqueda")
    for dato in lista:
        datos.append(dato.usuario.username)
        datos.append(dato.historial.fecha.ctime())
        datos.append(dato.historial.busqueda)
        #text.textLine(f"{dato.usuario}   {dato.historial.fecha}    {dato.historial.busqueda} ")

    filas = int(len(datos) / 3)

    
    d=0
    tabla=[]
    for i in range(filas):
        col = []
        for j in range(3):
            col.append(datos[d])
            d += 1
        tabla.append(col)
    print(tabla)


    tabla_i = Table(tabla, spaceBefore=2*inch, spaceAfter=2*inch)

    tabla_i.wrapOn(pdf, 100, 100)
    tabla_i.drawOn(pdf, 100, 200)
    
    pdf.drawText(text)
    pdf.save()

    return True

def custom_404(request, exception):
    return render(request, '404.html', status=404)

def custom_400(request, exception):
    return render(request, '400.html', status=400)

def custom_500(request, exception):
    return render(request, '500.html', status=500)