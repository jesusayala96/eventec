from django import template
from home.models import Evento,Comentario,Usuario

register = template.Library()

@register.inclusion_tag('home/template_ultimos.html')
def ultimos():
    try:
        eventoss=Evento.publicados_actuales_objects.all().order_by('Fecha')[:5]
    except:
        eventoss=None
    return {'ultimos_eventos':eventoss}

@register.inclusion_tag('home/template_likes.html')
def likeados():
    try:
        eventoss=Evento.publicados_actuales_objects.all().order_by('Likes')[:3]
    except:
        eventoss=None
    return {'ultimos_eventos':eventoss}

@register.inclusion_tag('home/template_comentados.html')
def comentados():
    try:
        eventoss=Evento.publicados_actuales_objects.all().order_by('Comentarios')[:3]
    except:
        eventoss=None
    return {'ultimos_eventos':eventoss}