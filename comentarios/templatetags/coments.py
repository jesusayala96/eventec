from django import template
from home.models import Evento,Comentario,Usuario

register = template.Library()

@register.inclusion_tag('comentarios/comentarios.html',takes_context=True)
def coments(context,evento):
    request = context['request']
    evento=Evento.objects.get(pk=evento)
    comentarios=evento.Comentarios.all()
    return {'comentarios':comentarios,'usr':request.user}