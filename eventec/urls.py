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
from home import views
from django.conf.urls.static import url, static
from django.conf import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
  
    url(r'^sign/$', views.sign),
    url(r'^signup-alumno/$', views.signup_Alumno),
    url(r'^signup-externo/$', views.signup_Externo),
    
    url(r'^$', views.index, name='index'),
    
    url(r'^login/$', auth_views.LoginView.as_view(template_name= 'home/login.html'), name='login'),
    url(r'^logout/$', auth_views.logout_then_login, name='logout'),
    
    url(r'^evento/(?P<pk>\d+)/$',views.detalle_evento,name='evento-details'),
  
    url(r'^eventos/categoria/$',views.lista_categorias,name='eventos-categoria'),
    url(r'^eventos/tipo/$',views.lista_tipos,name='eventos-tipo'),

    url(r'^eventos/categoria/(?P<categoria>\d+)/$',views.lista_categoria,name='evento-categoria'),
    url(r'^eventos/tipo/(?P<tipo>\d+)/$',views.lista_tipo,name='evento-tipo'),
  
    url(r'^wsevento/like/(?P<pk>\d+)$',views.wsLike,name='evento-like'),
    url(r'^wsevento/esperado/(?P<pk>\d+)$',views.wsGuardar,name='evento-esperado'),

    url(r'^staff/', include('staff.urls') ),
  
    url(r'^user/', include('usuario.urls') ),
  
    url(r'^comments/', include('comentarios.urls') ),

  
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#handler404 = 'home.views.error404'
#handler500 = 'home.views.error500'
#handler403 = 'home.views.error403'
#handler400 = 'home.views.error400'
if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
