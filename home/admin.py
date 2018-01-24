from django.contrib import admin
from home.models import Evento,Usuario, Categoria, Tipo, Comentario, Like, Imagenes, EventosEsperados, EventosGuardados 


# Register your models here.
admin.site.register(Evento)
admin.site.register(Usuario)
admin.site.register(Categoria)
admin.site.register(Tipo)
admin.site.register(Comentario)
admin.site.register(Like)
admin.site.register(Imagenes)
admin.site.register(EventosEsperados)
admin.site.register(EventosGuardados)