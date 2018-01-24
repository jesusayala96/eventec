from home.models import Usuario,Staff
def get_tipo_usuario(request):
    try:
        tipo=Usuario.objects.get(user=request.user).get_Tipo_display
    except:
        try:
            Staff.objects.get(user=request.user)
            tipo='Staff'
        except:
            tipo='Anonimo'
    if request.user.is_superuser:
        tipo='SuperUsuario'
    contexto = {'tipo_usuario':tipo}
    return contexto

def get_usuario_pk(request):
    try:
        user=Usuario.objects.get(user=request.user)
        pk=user.pk
        contexto = {'pk_user':pk}
        return contexto
    except:
        pass
    return {}