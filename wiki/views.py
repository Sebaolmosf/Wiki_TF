from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, update_session_auth_hash, logout
from django.contrib.auth.decorators import login_required
from .models import Usuario


# ================== VISTAS BÁSICAS ==================

def animales(request):
    return render(request, 'wiki/Animales.html')

def armas(request):
    return render(request, 'wiki/Armas.html')

def construcciones(request):
    return render(request, 'wiki/Construcciones.html')

def consumibles(request):
    return render(request, 'wiki/Consumibles.html')

def enemigos(request):
    return render(request, 'wiki/Enemigos.html')

def flora(request):
    return render(request, 'wiki/Flora.html')

def forowiki(request):
    return render(request, 'wiki/forowiki.html')

def historia(request):
    return render(request, 'wiki/historia.html')

def logros(request):
    return render(request, 'wiki/Logros.html')

def lugarestf(request):
    return render(request, 'wiki/Lugarestf.html')

def menuprincipal_wiki(request):
    return render(request, 'wiki/menuprincipal_wiki.html')

def recuperarcontra(request):
    return render(request, 'wiki/recuperarcontra.html')


# ================== REGISTRO ==================

def registrase_wiki(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if not email or not password1 or not password2:
            messages.error(request, 'Todos los campos son obligatorios.')
            return redirect('registrase_wiki')

        if password1 != password2:
            messages.error(request, 'Las contraseñas no coinciden.')
            return redirect('registrase_wiki')

        if Usuario.objects.filter(email=email).exists():
            messages.error(request, 'El correo ya está registrado.')
            return redirect('registrase_wiki')

        nuevo_usuario = Usuario.objects.create_user(email=email, password=password1)
        messages.success(request, '¡Usuario registrado con éxito! Ahora puedes iniciar sesión.')
        return redirect('inicio_sesion_wiki')

    return render(request, 'wiki/registrase_wiki.html')


# ================== INICIO DE SESIÓN ==================

def inicio_sesion_wiki(request):
    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('micuentatf')
        else:
            messages.error(request, 'Credenciales inválidas.')

    return render(request, 'wiki/inicio_sesion_wiki.html')


# ================== CIERRE DE SESIÓN ==================

def cerrar_sesion(request):
    logout(request)  
    messages.success(request, "Has cerrado sesión con éxito.")
    return redirect('inicio_sesion_wiki')  


# ================== VISTA DE MI CUENTA ==================

@login_required(login_url='inicio_sesion_wiki')
def micuentatf(request):
    usuario = request.user

    if request.method == 'POST':
        if 'guardar' in request.POST:
            nuevo_email = request.POST.get('email')
            nueva_password = request.POST.get('password')

            if not nuevo_email:
                messages.error(request, 'El correo es obligatorio.')
                return redirect('micuentatf')

            if Usuario.objects.exclude(pk=usuario.pk).filter(email=nuevo_email).exists():
                messages.error(request, 'El correo ya está registrado.')
                return redirect('micuentatf')

            usuario.email = nuevo_email
            if nueva_password:
                usuario.set_password(nueva_password)
                update_session_auth_hash(request, usuario)

            usuario.save()
            messages.success(request, 'Datos actualizados correctamente.')
            return redirect('micuentatf')

        elif 'eliminar' in request.POST:
            usuario.delete()
            messages.success(request, 'Cuenta eliminada. Debes registrarte nuevamente.')
            return redirect('registrase_wiki')

    return render(request, 'wiki/micuentatf.html', {'usuario': usuario})


# ================== EDITAR INFORMACIÓN ==================

@login_required(login_url='inicio_sesion_wiki')
def editar_informacion(request):
    usuario = request.user

    if request.method == 'POST':
        nuevo_email = request.POST.get('email')
        nueva_password = request.POST.get('password')

        if not nuevo_email:
            messages.error(request, 'El correo es obligatorio.')
            return redirect('editar_informacion')

        if Usuario.objects.exclude(pk=usuario.pk).filter(email=nuevo_email).exists():
            messages.error(request, 'El correo ya está registrado.')
            return redirect('editar_informacion')

        usuario.email = nuevo_email
        if nueva_password:
            usuario.set_password(nueva_password)
            update_session_auth_hash(request, usuario)

        usuario.save()
        messages.success(request, 'Información actualizada.')
        return redirect('micuentatf')

    return render(request, 'wiki/editar_informacion.html', {'usuario': usuario})
