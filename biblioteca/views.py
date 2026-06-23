# biblioteca/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Libro, Autor, Prestamo
from .forms import LibroForm, AutorForm, PrestamoForm
# Herramientas de seguridad para bloquear o permitir el acceso según el rol del usuario
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
# Herramientas nativas para el control de sesiones HTTP y alertas en la interfaz web
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages

# Create your views here.
# MÓDULO: Gestion de libros, "Rol usuario Anonimo vista publica"
def lista_libros(request):
    libros = Libro.objects.all()  # Consulta ORM
    return render(request, "libros/index.html", {"libros": libros})

def ver_libro(request, slug):
    libro = get_object_or_404(Libro, slug=slug)  # Busca el registro; si no existe, lanza un Error 404.
    return render(request, 'libros/detalle_libro.html', {'libro': libro})


@login_required  # RESTRICCIÓN: Rol usuario administrador con cuenta activa registrado.
def crear_libro(request):
    if request.method == "POST":
        form = LibroForm(request.POST)
        nuevo_autor_nombre = request.POST.get('nuevo_autor_nombre', '').strip()
        
        if nuevo_autor_nombre:
            autor, creado = Autor.objects.get_or_create(nombre=nuevo_autor_nombre)
            datos_modificados = request.POST.copy()
            datos_modificados['autor'] = autor.id
            form = LibroForm(datos_modificados)

        if form.is_valid():
            form.save()
            messages.success(request, "¡Libro y Autor registrados exitosamente!")
            return redirect("biblioteca:libros")
    else:
        form = LibroForm()
        
    return render(request, "libros/form.html", {"form": form})


@login_required  # RESTRICCIÓN: Rol usuario administrador con cuenta activa registrado "puede editar".
def editar_libro(request, libro_id):
    libro = get_object_or_404(Libro, pk=libro_id)
    form = LibroForm(request.POST or None, instance=libro)    
    if form.is_valid():
        form.save()
        messages.success(request, "¡Libro modificado correctamente!")
        return redirect("biblioteca:libros")
        
    return render(request, "libros/form.html", {"form": form})


@staff_member_required  # RESTRICCIÓN DE ACCESO: Rol Administrador solo Superusuario.
def eliminar_libro(request, libro_id):
    libro = get_object_or_404(Libro, pk=libro_id)
    libro.delete()
    messages.success(request, "El libro ha sido eliminado del inventario de forma segura.")
    return redirect("biblioteca:libros")


# MÓDULO 2: GESTIÓN DE AUTORES "Rol usuario Anonimo vista publica"
def lista_autores(request):
    autores = Autor.objects.all()
    return render(request, "autores/index.html", {"autores": autores})


@login_required  # RESTRICCIÓN: Rol usuario administrador con cuenta activa registrado.
def crear_autor(request):
    if request.method == "POST":
        form = AutorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "¡Autor registrado exitosamente!")
            return redirect("biblioteca:autores")
    else:
        form = AutorForm()
    return render(request, "autores/form.html", {"form": form})


@login_required  # RESTRICCIÓN: Rol usuario administrador con cuenta activa registrado "puede editar".
def editar_autor(request, autor_id):
    autor = get_object_or_404(Autor, pk=autor_id)
    form = AutorForm(request.POST or None, instance=autor)
    if form.is_valid():
        form.save()
        messages.success(request, "Información del autor actualizada.")
        return redirect("biblioteca:autores")
    return render(request, "autores/form.html", {"form": form})


@staff_member_required  # RESTRICCIÓN DE ACCESO: Rol Administrador solo Superusuario.
def eliminar_autor(request, autor_id):
    autor = get_object_or_404(Autor, pk=autor_id)
    autor.delete()
    messages.success(request, "Autor y sus obras asociadas eliminados en cascada.")
    return redirect("biblioteca:autores")


# MÓDULO 3: GESTIÓN DE PRÉSTAMOS "Rol usuario Anonimo vista publica"
def lista_prestamos(request):
    prestamos = Prestamo.objects.all()
    return render(request, "prestamos/index.html", {"prestamos": prestamos})


@login_required
def crear_prestamo(request):
    if request.method == "POST":
        form = PrestamoForm(request.POST)        
        if form.is_valid():
            form.save()
            messages.success(request, "¡Préstamo registrado exitosamente en PostgreSQL!")
            return redirect("biblioteca:prestamos")
        else:
            print("❌ ERROR DE VALIDACIÓN DETECTADO EN PRÉSTAMOS:", form.errors)
            messages.error(request, "No se pudo guardar el préstamo. Verifique los formatos de los campos.")
    else:
        form = PrestamoForm()
    return render(request, "prestamos/form.html", {"form": form})


@login_required
def editar_prestamo(request, prestamo_id):
    prestamo = get_object_or_404(Prestamo, pk=prestamo_id)
    form = PrestamoForm(request.POST or None, instance=prestamo)    
    if form.is_valid():
        form.save()
        messages.success(request, "Bitácora de préstamo actualizada con éxito.")
        return redirect("biblioteca:prestamos")
        
    return render(request, "prestamos/form.html", {"form": form})


@staff_member_required
def eliminar_prestamo(request, prestamo_id):
    prestamo = get_object_or_404(Prestamo, pk=prestamo_id)
    prestamo.delete()
    messages.success(request, "Registro de préstamo purgado del historial.")
    return redirect("biblioteca:prestamos")


# SISTEMA DE AUTENTICACIÓN SEGURIDAD registro
def login_view(request):
    if request.user.is_authenticated:
        return redirect('biblioteca:libros')
        
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"¡Login exitoso! Bienvenido {request.user.username}")
            return redirect("biblioteca:libros")
        else:
            messages.error(request, "Credenciales inválidas, intente de nuevo o verifique los datos.")
    else:
        form = AuthenticationForm()
    return render(request, "libros/login.html", {"form": form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('biblioteca:libros')
        
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "¡Registro exitoso! Cuenta creada y sesión iniciada.")
            return redirect("biblioteca:libros")
        else:
            messages.error(request, "Por favor corrige los errores del formulario de registro.")
    else:
        form = UserCreationForm()
    return render(request, "libros/register.html", {"form": form})


@login_required
def Cerrarsesion(request):
    logout(request)
    messages.info(request, "Sesión cerrada correctamente.")
    return redirect('biblioteca:libros')