# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from home.models import Staff,Asistencia,Asistente
# Register your models here.

admin.site.register(Staff)
admin.site.register(Asistencia)
admin.site.register(Asistente)