"""eventec URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf.urls.static import url, static
from django.conf import settings
from usuario import views
from django.views.static import serve
urlpatterns = [
    #url(r'^/', admin.site.urls),
  
    url(r'^profile/$', views.user_detail, name="usuario_detail"),
    url(r'^profile/edit/(?P<pk>[-\d]+)/$',views.ActualizarPerfil.as_view(),name='perfil_update'),
    url(r'^profile/miseventos/$', views.Eventos_Creados_Usuario, name="eventos_creados"),  
    url(r'^profile/miseventos/editar/(?P<pk>\d+)/$', views.EventoUpdate.as_view(), name="eventos_creados"),  
    url(r'^profile/guardados/$', views.Eventos_Guardados_Usuario, name="eventos_guardados"),  
    url(r'^profile/gustados/$', views.Eventos_Gustados_Usuario, name="eventos_gustados"),
    url(r'^crear_evento/$', views.Crear_Evento, name="crear_evento"),  
  
    
    #Admin
    url(r'^admin/$', views.Eventos_No_Publicados_ListView.as_view(), name="admin-eventos"),
    url(r'^admin/publicados/$', views.Eventos_Publicados_ListView.as_view(), name="Lista_Publicados"), 
    url(r'^admin/publicar/evento/(?P<pk>[-\d]+)/$', views.publicar, name="admin-publicar"),
    url(r'^admin/despublicar/evento/(?P<pk>[-\d]+)/$', views.despublicar, name="admin-despublicar"),
    url(r'^admin/usuarios/$', views.Usuarios_Reporte.as_view(), name="lista-usuarios"),
    url(r'^admin/usuarios/(?P<pk>[-\d]+)/$', views.Usuario_Detail, name="admin-usuarios"),
    url(r'^admin/staff/(?P<pk>[-\d]+)/$', views.Staff_Detail, name="staff-view"),
    url(r'^admin/staff/$', views.Staff_Reporte.as_view(), name="lista-staff"),
  
    url(r'^admin/staff/asignar/(?P<pk>[-\d]+)/$', views.Asignar_Staff.as_view(), name="asignar-staff"),
  
    url(r'^admin/staff/eventos/(?P<pk>[-\d]+)/$', views.EventosStaff.as_view(), name="lista-eventostaff"),
    url(r'^admin/usuarios/eventos/(?P<pk>[-\d]+)/$', views.EventosUsuario.as_view(), name="eventos-usuario"),
  
    url(r'^admin/usuarios/crear/$', views.crear_usuario, name="crear_usuario"),
    url(r'^admin/staff/crear/$', views.Crear_Staff, name="crear-staff"),
    url(r'^admin/usuarios/editar/(?P<pk>[-\d]+)/$', views.Usuario_Update.as_view(), name="editar-usuarios"),
    url(r'^admin/editar/evento/(?P<pk>[-\d]+)/$', views.Evento_Update.as_view(), name="editar-evento"),
    url(r'^admin/staff/editar/(?P<pk>[-\d]+)/$', views.Staff_Update.as_view(), name="editar-staff"),
     
]
