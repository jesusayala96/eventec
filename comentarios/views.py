# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from home.models import Comentario
from django.http import HttpResponse
import json
from django.contrib.auth.decorators import login_required,user_passes_test

def check_not_staff(username):
    print username
    return not Staff.objects.filter(user=username).exists()

# Create your views here.
@login_required(login_url="/login/")
@user_passes_test(check_not_staff,login_url="/login/")
def delete_comentario(request,pk):
    comentario=Comentario.objects.get(pk=pk)
    comentario.delete()
    response_data={}
    response_data['result']="Comentario Borrado"
    return HttpResponse(json.dumps(response_data),content_type="application/json")