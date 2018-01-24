from django.shortcuts import render

from .forms import  SignUpForm_Alumno, SignUpForm_Externo, SignUpForm_Usuario
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required,user_passes_test
from django.shortcuts import redirect,render
from django.http import HttpResponse
from django.core import serializers
import json
from comentarios.forms import comentario_form
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from home.models import Staff,Asistencia,Asistente,Evento,Usuario, Categoria, Tipo, Comentario, Like, Imagenes, EventosEsperados, EventosGuardados

import datetime

def check_not_staff(username):
    print username
    return not Staff.objects.filter(user=username).exists()

# Create your views here.
def index(request):
    try:
        tipo=Usuario.objects.get(user=request.user).get_Tipo_display
    except:
        try:
            Staff.objects.get(user=request.user)
            tipo='Staff'
        except:
            tipo='Anonimo'
            if request.user.is_superuser:
                tipo='Super'
                return redirect('/admin/')
    #tipo=request.tipo_usuario
    if tipo is 'Staff':
        return redirect('/staff/')
    try:
        eventoss=Evento.publicados_actuales_objects.all()
        page = request.GET.get('page', 1)
        paginator = Paginator(eventoss, 6)
        try:
            eventos = paginator.page(page)
        except PageNotAnInteger:
            eventos = paginator.page(1)
        except EmptyPage:
            eventos = paginator.page(paginator.num_pages)
    except:
        return render(request,'home/index.html',context={'eventos':None,})
    return render(request,'home/index.html',context={'eventos':eventos})

def sign(request):
  return render(request,'home/sign_base.html')

def signup_Alumno(request):
    form = SignUpForm_Alumno(request.POST or None)
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')
        Nombre = form.cleaned_data.get('first_name')
        Apellido_Paterno = form.cleaned_data.get('last_name')
        Apellido_Materno = form.cleaned_data.get('Apellido_Materno')
        Direccion = form.cleaned_data.get('Direccion')
        Correo = form.cleaned_data.get('email')
        Telefono = form.cleaned_data.get('Telefono')
        NumControl = form.cleaned_data.get('NumControl')
        user = authenticate(username=username, password=raw_password)
        login(request, user)
        Usuario.objects.create(user=user, Nombre= Nombre, ApellidoPaterno= Apellido_Paterno,NumControl = NumControl, ApellidoMaterno = Apellido_Materno, Direccion = Direccion, Tipo='A', Telefono=Telefono, Correo=Correo)
        usuario_activo = Usuario.objects.get(user=user)
        EventosEsperados.objects.create(Usuario=usuario_activo)
        EventosGuardados.objects.create(Usuario=usuario_activo)
        return render(request, 'home/index.html')
    return render(request, 'home/signup.html', {'form': form})

def signup_Externo(request):
    form = SignUpForm_Externo(request.POST or None)
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')
        Nombre = form.cleaned_data.get('first_name')
        Apellido_Paterno = form.cleaned_data.get('last_name')
        Apellido_Materno = form.cleaned_data.get('Apellido_Materno')
        Direccion = form.cleaned_data.get('Direccion')
        Correo = form.cleaned_data.get('email')
        Telefono = form.cleaned_data.get('Telefono')
        user = authenticate(username=username, password=raw_password)
        login(request, user)
        Usuario.objects.create(user=user, Nombre= Nombre, ApellidoPaterno= Apellido_Paterno, ApellidoMaterno = Apellido_Materno, Direccion = Direccion, Tipo='C', Telefono=Telefono, Correo=Correo)
        usuario_activo = Usuario.objects.get(user=user)
        EventosEsperados.objects.create(Usuario=usuario_activo)
        EventosGuardados.objects.create(Usuario=usuario_activo)

        return render(request, 'home/index.html')
    return render(request, 'home/signup.html', {'form': form})


def detalle_evento(request,pk):
    try:
        evento=Evento.objects.get(pk=pk)
        if request.method == "POST":
            form=comentario_form(request.POST)
            if form.is_valid():
                clean=form.cleaned_data
                comentario=Comentario()
                comentario.Comentario=clean['Comentario']
                comentario.Usuario=Usuario.objects.get(user=request.user)
                comentario.save()
                evento.Comentarios.add(comentario)
                evento.save()
                form=comentario_form()
                return redirect('evento-details', pk=pk)

        else:
            form=comentario_form()
    except:
        raise Http404("No existe esa publicacion")
    return render(request,'home/eventos/ver_evento.html',context={'evento':evento,'form':form})

#Para tener la primera imagen en el template
#for evento in object...
#evento.Imagenes.first().Imagen.url
def lista_tipos(request):
  return render(request,'home/eventos/tipos.html',{'tipos':Tipo.objects.all()})

def manejo_error(request):
  return render(request, 'home/error.html')

def lista_tipo(request,tipo):
    try:
        eventoss=Evento.publicados_actuales_objects.filter(Tipos__pk=tipo)
        page = request.GET.get('page', 1)
        paginator = Paginator(eventoss, 6)
        try:
            eventos = paginator.page(page)
        except PageNotAnInteger:
            eventos = paginator.page(1)
        except EmptyPage:
            eventos = paginator.page(paginator.num_pages)
        return render(request,'home/eventos/ver_eventos.html',context={'eventos':eventos,})
    except:
        return render(request,'home/eventos/ver_eventos.html',context={'eventos':None,})


def lista_categorias(request):
  return render(request,'home/eventos/categorias.html',{'categorias':Categoria.objects.all()})

def lista_categoria(request,categoria):
    try:
        eventoss=Evento.publicados_actuales_objects.filter(Categorias__pk=categoria)
        page = request.GET.get('page', 1)
        paginator = Paginator(eventoss, 6)
        try:
            eventos = paginator.page(page)
        except PageNotAnInteger:
            eventos = paginator.page(1)
        except EmptyPage:
            eventos = paginator.page(paginator.num_pages)
        return render(request,'home/eventos/ver_eventos.html',context={'eventos':eventos,})
    except:
        return render(request,'home/eventos/ver_eventos.html',context={'eventos':None,})

#Tiene que estar logueado
@login_required(login_url="/login/")
@user_passes_test(check_not_staff,login_url="/login/")
def wsLike(request,pk):
    try:
        usuario=Usuario.objects.get(user=request.user)
        evento=Evento.objects.get(pk=pk)
        response_data={}
        try:
            like=evento.Likes.get(Usuario=usuario)
            like.delete()
            guardando=EventosEsperados.objects.get(Usuario=usuario)
            guardando.Evento.remove(evento)
            guardando.save()
            response_data['result']='DisLike'
            return HttpResponse(json.dumps(response_data),content_type="application/json")
        except:
            like=Like()
            guardando=EventosEsperados.objects.get(Usuario=usuario)
            guardando.Evento.add(evento)
            guardando.save()
            like.Usuario=usuario
            like.save()
            evento.Likes.add(like)
            evento.save()
            response_data['result']='Like'
            return HttpResponse(json.dumps(response_data),content_type="application/json")
    except:
        return redirect('index')

@login_required(login_url="/login/")
@user_passes_test(check_not_staff,login_url="/login/")
def wsGuardar(request,pk):
    try:
        usuario=Usuario.objects.get(user=request.user)
        evento=Evento.objects.get(pk=pk)
        response_data={}
        try:
            guardando=EventosGuardados.objects.get(Usuario=usuario)
            guardando.Evento.get(pk=pk)
            guardando.Evento.remove(evento)
            guardando.save()
            response_data['result']='Eliminado de tu lista'
            return HttpResponse(json.dumps(response_data),content_type="application/json")
        except:
            guardando=EventosGuardados.objects.get(Usuario=usuario)
            guardando.Evento.add(evento)
            guardando.save()
            response_data['result']='Guardas'
            return HttpResponse(json.dumps(response_data),content_type="application/json")
    except:
        return redirect('index')

def error404(request):
  return render(request,'home/404.html')
def error403(request):
  pass
def error400(request):
  pass
def error500(request):
  pass