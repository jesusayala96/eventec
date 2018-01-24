# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
import datetime
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from datetime import date,timedelta

def validate_current_date(value):
    if value <= date.today():
        raise ValidationError(u'%s Debe ser una fecha futura!' % value)
# Create your models here.
class Usuario(models.Model):
    user = models.OneToOneField(User)
    Nombre = models.CharField(max_length=40,validators=[RegexValidator(r'^([a-zA-Z]{2,}\s?[a-zA-z]{1,}?-?[a-zA-Z]{2,}\s?([a-zA-Z]{1,})?)$',message='Ingresa un nombre valido')])
    ApellidoPaterno = models.CharField(max_length=40,validators=[RegexValidator(r'^([a-zA-Z]{2,}\s?[a-zA-z]{1,}?-?[a-zA-Z]{2,}\s?([a-zA-Z]{1,})?)$',message='Ingresa un apellido valido')])
    ApellidoMaterno = models.CharField(max_length=40,validators=[RegexValidator(r'^([a-zA-Z]{2,}\s?[a-zA-z]{1,}?-?[a-zA-Z]{2,}\s?([a-zA-Z]{1,})?)$',message='Ingresa un apellido valido')])
    Correo = models.EmailField()
    Direccion = models.CharField(max_length=40,blank=True,validators=[RegexValidator(r'^.*$',message='Ingresa una direccion valida')])
    Telefono = models.CharField(blank=True,max_length=10, validators=[RegexValidator(r'^[2-9]{2}\d{8}$',message='Ingresa un numero telefonico valido')])
    PaginaWeb=models.CharField(max_length=50,blank=True)
    NumControl = models.CharField(blank=True,max_length=8, validators=[RegexValidator(r'^\d{8}$',message='Ingresa un numero de control valido')])
    tipo_opciones=(('A','Alumno'),('B','Admin'),('C','Externo'),('D','Interno'))
    Tipo =models.CharField(max_length=1,choices=tipo_opciones)
    def __unicode__(self):
        return self.user.username

class Categoria(models.Model):
    Categoria = models.CharField(max_length=40)
    def __unicode__(self):
        return self.Categoria
    #Agregar a bd

class Tipo(models.Model):
    Tipo = models.CharField(max_length=40)
    def __unicode__(self):
        return self.Tipo
    #Agregar a bd

class Comentario(models.Model):
    Comentario = models.TextField()
    Fecha = models.DateField(auto_now_add=True)
    Usuario = models.ForeignKey(Usuario)

class Like(models.Model):
    ##Like = models.BooleanField()
    Fecha = models.DateField(auto_now_add=True)
    Usuario = models.ForeignKey(Usuario)

class Imagenes(models.Model):
    Imagen=models.ImageField(upload_to='eventos')
    Fecha=models.DateTimeField(auto_now_add=True)




class publicados_manager(models.Manager):
    def get_queryset(self):
        return super(publicados_manager,self).get_queryset().filter(Publicado=True)
class publicados_actuales_manager(models.Manager):
    def get_queryset(self):
        today=date.today()
        return super(publicados_actuales_manager,self).get_queryset().filter(Publicado=True).filter(Fecha__gt=today - timedelta(days=3))

class Evento(models.Model):
    Titulo = models.CharField(max_length=50)
    DescripcionL = models.TextField()
    DescripcionC= models.CharField(max_length=150)
    Fecha = models.DateField()
    #validators=[validate_current_date]
    Hora = models.TimeField()
    Publicado = models.BooleanField(default=False)
    Vistas = models.IntegerField(default=0)
    Lugar= models.CharField(max_length=40, default="Teatro Calafornix")
    Categorias = models.ManyToManyField(Categoria)
    Comentarios = models.ManyToManyField(Comentario,blank=True)
    Likes = models.ManyToManyField(Like,blank=True)
    Tipos = models.ManyToManyField(Tipo,blank=True)
    Imagenes=models.ManyToManyField(Imagenes,blank=True)
    PlaceID=models.CharField(max_length=27,blank=True)
    Autor=models.ForeignKey(Usuario)

    #Managers
    objects=models.Manager()
    publicados_objects=publicados_manager()
    publicados_actuales_objects=publicados_actuales_manager()
    def __unicode__(self):
        return self.Titulo

class EventosEsperados(models.Model):
    Usuario = models.OneToOneField(Usuario)
    Evento = models.ManyToManyField(Evento,blank=True)


class EventosGuardados(models.Model):
    Usuario = models.OneToOneField(Usuario)
    Evento = models.ManyToManyField(Evento,blank=True)

class Staff(models.Model):
    Usuario = models.CharField(max_length=40)
    user = models.OneToOneField(User)
    def __unicode__(self):
        return self.Usuario

class Asistente(models.Model):
    Usuario=models.ForeignKey(Usuario,blank=True,null=True)
    Nombre=models.CharField(max_length=40,blank=True,validators=[RegexValidator(r'^([a-zA-Z]{2,}\s?[a-zA-z]{1,}?-?[a-zA-Z]{2,}\s?([a-zA-Z]{1,})?)$',message='Ingresa un nombre valido')])
    Escuela=models.CharField(max_length=40,blank=True,validators=[RegexValidator(r'^([a-zA-Z]{2,}\s?[a-zA-z]{1,}?-?[a-zA-Z]{2,}\s?([a-zA-Z]{1,})?)$',message='Ingresa una escuela valido')])
    Correo=models.EmailField()


class Asistencia(models.Model):
    Asistentes = models.ManyToManyField(Asistente,blank=True)
    Evento = models.OneToOneField(Evento)
    Staff = models.ManyToManyField(Staff,blank=True)
    def __unicode__(self):
       return self.Evento.Titulo


