# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect
from django.http import HttpResponse
from staff.forms import TomarAsistencia_form
from django.core import serializers
from django.db.models import Prefetch
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required,user_passes_test
from home.models import Staff,Asistencia,Asistente,Evento,Usuario, Categoria, Tipo, Comentario, Like, Imagenes, EventosEsperados, EventosGuardados 
from datetime import datetime
import json
from django.views.generic import  DetailView
from django.shortcuts import get_object_or_404

# Create your views here.
#Staff ZONE :'v
def check_staff(username):
    print username
    return Staff.objects.filter(user=username).exists()
    
@login_required(login_url="/login/")
@user_passes_test(check_staff,login_url="/login/")
def index(request):
    return render(request,'staff/index.html')

@login_required(login_url="/login/")
@user_passes_test(check_staff,login_url="/login/")
def ver_eventos(request):
    queryset=Asistencia.objects.filter(Staff__user=request.user).prefetch_related(Prefetch('Evento',queryset=Evento.objects.filter(Publicado=True).filter(Fecha__lte=datetime.now())))
    return render(request,'staff/eventos.html',{'object_list':queryset})

@login_required(login_url="/login/")
@user_passes_test(check_staff,login_url="/login/")
def asistencia(request,pk):
    try:
        evento=Evento()
        evento=Asistencia.objects.get(Evento__pk=pk)
        form=TomarAsistencia_form(request.POST or None)
        return render(request,'staff/asistencia.html',{'form':form,'pk':pk})
    except:
        return redirect('error-staff')

@login_required(login_url="/login/")
@user_passes_test(check_staff,login_url="/login/")
def ajax_asistentes(request,pk):
    try:
        queryset=Asistencia.objects.get(Evento__pk=pk)
        asistentes=queryset.Asistentes.all()
        list=[]
        for asistente in asistentes:
            list.append(asistente)
        list.append(queryset)
        data = serializers.serialize('json', list)
        return HttpResponse(data, content_type='json')
    except:
        return redirect('error-staff')

@login_required(login_url="/login/")
@user_passes_test(check_staff,login_url="/login/")    
def ajax_agregar(request,pk):
    try:
        if request.method == 'POST':
            correo = request.POST.get('Correo')
            escuela=request.POST.get('Escuela')
            nombre=request.POST.get('Nombre')

            response_data = {}
            evento=Evento()
            try:
                evento=Asistencia.objects.get(Evento__pk=pk)
            except:
                return redirect('error-staff')
            if evento.Asistentes.filter(Correo=correo).exists():
                response_data['result'] = 'Existente'
            else:
                asistente=Asistente()
                try:
                    Usuario.objects.get(Correo=correo)
                    print "Hay un usuario con ese correo"
                    asistente.Usuario=Usuario.objects.get(Correo=correo)
                except:
                    pass

                asistente.Correo=correo
                asistente.Escuela=escuela
                asistente.Nombre=nombre
                asistente.save()

                evento.Asistentes.add(asistente)
                evento.save()

                response_data['result'] = 'Registrado'
                response_data['nombre'] = asistente.Nombre
                response_data['correo'] = asistente.Correo
                response_data['escuela'] = asistente.Escuela
                response_data['pk'] = asistente.pk

        return HttpResponse(
                json.dumps(response_data),
                content_type="application/json"
            )
    except:
        return redirect('error-staff')

@login_required(login_url="/login/")
@user_passes_test(check_staff,login_url="/login/")
def delete_asistente(request,pk):
    evento=Asistencia.objects.get(Asistentes__pk=pk)
    asistente=Asistente.objects.get(pk=pk)
    asistente.delete()
    response_data={}
    response_data['result']="Asistente Borrado"
    return HttpResponse(
            json.dumps(response_data),
            content_type="application/json")
    
    
def error(request):
    return render(request,'staff/error.html')
 
  #detail
class Staff_Detail(DetailView):
    template_name="staff/staff_detail.html"

    def get_object(self):
        if self.request.user.is_authenticated and check_staff(self.request.user):
            return get_object_or_404(Staff, user=self.request.user)
        else:
            return redirect('error-staff') 
  
  