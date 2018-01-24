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
from django.conf.urls import url
from staff import views as staff

urlpatterns = [
  url(r'^$', staff.index, name='index-staff' ),
    
  url(r'^eventos/$', staff.ver_eventos, name='eventos-staff' ),
  url(r'^eventos/(?P<pk>\d+)$', staff.asistencia, name='asistencia-staff' ),
    
  url(r'^eventos/wseventos/(?P<pk>\d+)$', staff.ajax_agregar, name='wsasistencia-staff' ),
  url(r'^eventos/wsasistentes/(?P<pk>\d+)$', staff.ajax_asistentes, name='wsasistentes-staff' ),
  url(r'^eventos/delete/(?P<pk>\d+)$', staff.delete_asistente, name='delete-staff' ),
  
  url(r'^user/', staff.Staff_Detail.as_view(), name="staff_detail_view"),
  
  url(r'^', staff.error, name='error-staff' ),
 # url(r'^(.*)', staff.error, name='error-staff' ),
  
    
  
]
