# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic import UpdateView, DetailView, ListView, CreateView
from home.models import Usuario, Evento, Staff, Asistencia,EventosEsperados,EventosGuardados, Imagenes
from home.forms import Crear_Evento_Form, Imagen_Form,SignUpForm_Alumno, SignUpForm_Staff, SignUpForm_Usuario
from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required,user_passes_test

# Create your views here.
def check_not_staff(username):
    print username
    return not Staff.objects.filter(user=username).exists()

def check_admin(username):
    print username
    return Usuario.objects.filter(user=username).filter(Tipo='B').exists()


#Validad solo el usuario lo hace(y)
class ActualizarPerfil(UpdateView):
    model = Usuario
    fields = ('Nombre', 'ApellidoPaterno','ApellidoMaterno','Correo','Direccion', 'Telefono')
    template_name = 'usuario/perfil/editar.html'
    def get_context_data(self, **kwargs):
        context = super(ActualizarPerfil, self).get_context_data(**kwargs)
        context['usuario'] = Usuario.objects.get(user=self.request.user)
        return context

    def get_success_url(self):
        view_name = 'usuario_detail'
        return reverse_lazy(view_name)

    def user_passes_test(self, request):
        if request.user.is_authenticated():
            self.object = self.get_object()
            return self.object.user == request.user
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            return redirect('login')
        return super(ActualizarPerfil, self).dispatch(request, *args, **kwargs)

@login_required(login_url="/login/")
@user_passes_test(check_not_staff,login_url="/login/")
def user_detail(request):
    user=Usuario.objects.get(user=request.user)
    return render(request,'usuario/perfil/usuario_detail.html',{'usuario':user})

class EventoUpdate(UpdateView):
    template_name="usuario/perfil/editar.html"
    model=Evento
    fields=['Titulo','DescripcionL','DescripcionC','Fecha','Lugar','Categorias','Tipos']

    def get_context_data(self, **kwargs):
        context = super(EventoUpdate, self).get_context_data(**kwargs)
        context['usuario'] = Usuario.objects.get(user=self.request.user)
        return context

    def get_success_url(self):
        view_name = 'evento-details'
        return reverse_lazy(view_name, kwargs={'pk': self.kwargs.get('pk','')})

    def user_passes_test(self, request):
        if request.user.is_authenticated():
            self.object = self.get_object()
            return self.object.Autor.user == request.user
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            return redirect('login')
        return super(EventoUpdate, self).dispatch(request, *args, **kwargs)

@login_required(login_url="/login/")
@user_passes_test(check_not_staff,login_url="/login/")
def Eventos_Creados_Usuario(request):
    try:
        usuario=Usuario.objects.get(user=request.user)
        eventoss=Evento.objects.filter(Autor=usuario)
        page = request.GET.get('page', 1)
        paginator = Paginator(eventoss, 6)
        try:
            eventos = paginator.page(page)
        except PageNotAnInteger:
            eventos = paginator.page(1)
        except EmptyPage:
            eventos = paginator.page(paginator.num_pages)
        return render(request,'usuario/perfil/mis_eventos.html',context={'eventos':eventos,})
    except:
        return render(request,'usuario/perfil/mis_eventos.html',context={'eventos':None,})

@login_required(login_url="/login/")
@user_passes_test(check_not_staff,login_url="/login/")
def Eventos_Guardados_Usuario(request):
    try:
        usuario=Usuario.objects.get(user=request.user)

        e=EventosGuardados.objects.get(Usuario=usuario)
        eventoss=e.Evento.all()

        page = request.GET.get('page', 1)
        paginator = Paginator(eventoss, 6)
        try:
            eventos = paginator.page(page)
        except PageNotAnInteger:
            eventos = paginator.page(1)
        except EmptyPage:
            eventos = paginator.page(paginator.num_pages)
        return render(request,'usuario/perfil/lista_eventos.html',context={'eventos':eventos,})
    except:
        return render(request,'usuario/perfil/lista_eventos.html',context={'eventos':None,})

@login_required(login_url="/login/")
@user_passes_test(check_not_staff,login_url="/login/")
def Eventos_Gustados_Usuario(request):
    try:
        usuario=Usuario.objects.get(user=request.user)

        e=EventosEsperados.objects.get(Usuario=usuario)
        print e
        eventoss=e.Evento.all()

        #EventosEsperados
        page = request.GET.get('page', 1)
        paginator = Paginator(eventoss, 6)
        try:
            eventos = paginator.page(page)
        except PageNotAnInteger:
            eventos = paginator.page(1)
        except EmptyPage:
            eventos = paginator.page(paginator.num_pages)
        return render(request,'usuario/perfil/lista_eventos.html',context={'eventos':eventos,})
    except:
        return render(request,'usuario/perfil/lista_eventos.html',context={'eventos':None,})

@login_required(login_url="/login/")
@user_passes_test(check_not_staff,login_url="/login/")
def Crear_Evento(request):
    form = Crear_Evento_Form(request.POST or None, request.FILES or None)
    form_img=Imagen_Form(request.POST or None, request.FILES or None)
    if request.method == "POST":
        if form.is_valid() and form_img.is_valid():
            form_=form.save(commit=False)
            autor=Usuario.objects.get(user=request.user)
            form_.Autor=autor
            form_.save()

            form.save_m2m()
            evento = Evento.objects.get(pk = form_.pk)
            x=form_img.save()

            evento.Imagenes.add(x)
            evento.save()

            Asistencia.objects.create(Evento = evento )
            form =Crear_Evento_Form()
            form_img=Imagen_Form()

    return render(request,'usuario/eventos/crear_evento.html',{"form":form,'img':form_img})


#Admin
class Eventos_No_Publicados_ListView(ListView):
    template_name="usuario/administrador/lista_eventos.html"
    model=Evento
    paginate_by=6
    context_object_name = 'eventos'
    queryset=Evento.objects.filter(Publicado=False)

    def user_passes_test(self, request):
        if request.user.is_authenticated():
            return Usuario.objects.filter(user=request.user).filter(Tipo='B').exists()
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            return redirect('login')
        return super(Eventos_No_Publicados_ListView, self).dispatch(request, *args, **kwargs)


class Eventos_Publicados_ListView(ListView):
    template_name="usuario/administrador/lista_eventos.html"
    model=Evento
    paginate_by=6
    context_object_name = 'eventos'
    queryset=Evento.objects.filter(Publicado=True)

    def user_passes_test(self, request):
        if request.user.is_authenticated():
            return Usuario.objects.filter(user=request.user).filter(Tipo='B').exists()
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            return redirect('login')
        return super(Eventos_Publicados_ListView, self).dispatch(request, *args, **kwargs)

@login_required(login_url="/login/")
@user_passes_test(check_admin,login_url="/login/")
def publicar(request,pk):
    evento=Evento.objects.get(pk=pk)
    evento.Publicado=True
    evento.save()
    return redirect('admin-eventos')

@login_required(login_url="/login/")
@user_passes_test(check_admin,login_url="/login/")
def despublicar(request,pk):
    evento=Evento.objects.get(pk=pk)
    evento.Publicado=False
    evento.save()
    return redirect('admin-eventos')

class Asignar_Staff(UpdateView):
    model = Asistencia
    fields = ['Staff']
    template_name = 'usuario/administrador/editar.html'
    def get_object(self):
        return Asistencia.objects.get(Evento__pk=self.kwargs['pk'])

    def get_success_url(self):
        view_name = 'asignar-staff'
        return reverse_lazy(view_name, kwargs={'pk': self.kwargs.get('pk','')})

    def user_passes_test(self, request):
        if request.user.is_authenticated():
            return Usuario.objects.filter(user=request.user).filter(Tipo='B').exists()
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            return redirect('login')
        return super(Asignar_Staff, self).dispatch(request, *args, **kwargs)

class Usuarios_Reporte(ListView):
    template_name="usuario/administrador/lista_usuarios.html"
    model=Usuario
    paginate_by=6
    context_object_name = 'usuarios'
    queryset=Usuario.objects.all()

    def user_passes_test(self, request):
        if request.user.is_authenticated():
            return Usuario.objects.filter(user=request.user).filter(Tipo='B').exists()
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            return redirect('login')
        return super(Usuarios_Reporte, self).dispatch(request, *args, **kwargs)

class Staff_Reporte(ListView):
    template_name="usuario/administrador/lista_staff.html"
    model=Staff
    paginate_by=6
    context_object_name = 'usuarios'
    queryset=Staff.objects.all()

    def user_passes_test(self, request):
        if request.user.is_authenticated():
            return Usuario.objects.filter(user=request.user).filter(Tipo='B').exists()
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            return redirect('login')
        return super(Staff_Reporte, self).dispatch(request, *args, **kwargs)

@login_required(login_url="/login/")
@user_passes_test(check_admin,login_url="/login/")
def Usuario_Detail(request,pk):
    return render(request,'usuario/administrador/ver_usuario.html',{'usuario' : Usuario.objects.get(pk=pk)})

@login_required(login_url="/login/")
@user_passes_test(check_admin,login_url="/login/")
def Staff_Detail(request,pk):
    return render(request,'usuario/administrador/ver_staff.html',{'usuario' : Staff.objects.get(pk=pk)})

class EventosUsuario(ListView):
    template_name="usuario/administrador/lista_eventos.html"
    model=Evento
    paginate_by=6
    context_object_name = 'eventos'
    def get_queryset(self):
        queryset=Evento.objects.filter(Autor__pk=self.kwargs['pk'])
        return queryset
    def user_passes_test(self, request):
        if request.user.is_authenticated():
            return Usuario.objects.filter(user=request.user).filter(Tipo='B').exists()
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            return redirect('login')
        return super(EventosUsuario, self).dispatch(request, *args, **kwargs)

class EventosStaff(ListView):
    template_name="usuario/administrador/eventos_staff.html"
    model=Asistencia
    paginate_by=6
    context_object_name = 'eventos'
    def get_queryset(self):
        queryset=Asistencia.objects.filter(Staff__pk=self.kwargs['pk']).all()
        return queryset
    def user_passes_test(self, request):
        if request.user.is_authenticated():
            return Usuario.objects.filter(user=request.user).filter(Tipo='B').exists()
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            return redirect('login')
        return super(EventosStaff, self).dispatch(request, *args, **kwargs)

class Staff_Update(UpdateView):
    model = Staff
    fields = ['Usuario']
    template_name = 'usuario/administrador/editar.html'

    def get_success_url(self):
        view_name = 'staff-view'
        return reverse_lazy(view_name, kwargs={'pk': self.kwargs.get('pk','')})

    def user_passes_test(self, request):
        if request.user.is_authenticated():
            return Usuario.objects.filter(user=request.user).filter(Tipo='B').exists()
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            return redirect('login')
        return super(Staff_Update, self).dispatch(request, *args, **kwargs)

class Usuario_Update(UpdateView):
    model = Usuario
    fields = ['Nombre','ApellidoPaterno','ApellidoMaterno','Correo','Direccion','Direccion','Telefono','NumControl','Tipo']
    template_name = 'usuario/administrador/editar.html'

    def get_success_url(self):
        view_name = 'editar-usuarios'
        return reverse_lazy(view_name, kwargs={'pk': self.kwargs.get('pk','')})

    def user_passes_test(self, request):
        if request.user.is_authenticated():
            return Usuario.objects.filter(user=request.user).filter(Tipo='B').exists()
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            return redirect('login')
        return super(Usuario_Update, self).dispatch(request, *args, **kwargs)




@login_required(login_url="/login/")
@user_passes_test(check_admin,login_url="/login/")
def crear_usuario(request):
  form= SignUpForm_Usuario(request.POST or None)
  if form.is_valid():
    user=form.save()
    username = form.cleaned_data.get('username')
    raw_password = form.cleaned_data.get('password1')
    Nombre = form.cleaned_data.get('first_name')
    Apellido_Paterno = form.cleaned_data.get('last_name')
    Apellido_Materno = form.cleaned_data.get('Apellido_Materno')
    Direccion = form.cleaned_data.get('Direccion')
    Correo = form.cleaned_data.get('email')
    Telefono = form.cleaned_data.get('Telefono')
    NumControl = form.cleaned_data.get('NumControl')
    tipo=form.cleaned_data.get('Tipo')
    #user = authenticate(username=username, password=raw_password)
    Usuario.objects.create(user=user, Nombre= Nombre, ApellidoPaterno= Apellido_Paterno,NumControl = NumControl, ApellidoMaterno = Apellido_Materno, Direccion = Direccion, Tipo=tipo, Telefono=Telefono, Correo=Correo)
    usuario_activo = Usuario.objects.get(user=user)
    EventosEsperados.objects.create(Usuario=usuario_activo)
    EventosGuardados.objects.create(Usuario=usuario_activo)
    return redirect('lista-usuarios')
  return render (request, 'usuario/administrador/crear.html', {'form': form})

@login_required(login_url="/login/")
@user_passes_test(check_admin,login_url="/login/")
def Crear_Staff(request):
    form = SignUpForm_Staff(request.POST or None)
    if form.is_valid():
      form.save()
      username = form.cleaned_data.get('username')
      raw_password = form.cleaned_data.get('password1')
      user = authenticate(username=username, password=raw_password)
      Staff.objects.create(Usuario=username, user=user)
      view_name = 'lista-staff'
      return redirect(view_name)
    return render(request,'usuario/administrador/crear.html', {'form': form})

class Evento_Update(UpdateView):
    template_name="usuario/perfil/editar.html"
    model=Evento
    fields=['Titulo','DescripcionL','DescripcionC','Fecha','Lugar','Categorias','Tipos']
    def user_passes_test(self, request):
        if request.user.is_authenticated():
            return Usuario.objects.filter(user=request.user).filter(Tipo='B').exists()
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            return redirect('login')
        return super(Evento_Update, self).dispatch(request, *args, **kwargs)