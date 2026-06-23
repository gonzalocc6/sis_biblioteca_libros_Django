# biblioteca/urls.py
from django.urls import path
from . import views

# Namespace para las URLs de esta app
app_name = 'biblioteca'

urlpatterns = [
    # RUTAS DE LIBROS
    path('', views.lista_libros, name='libros'),  # Página principal del catálogo
    path('libros/nuevo/', views.crear_libro, name='crear_libro'),  # Formulario de registro
    path('libros/<slug:slug>/', views.ver_libro, name='ver_libro'),  # Detalle usando el slug único
    path('libros/<int:libro_id>/editar/', views.editar_libro, name='editar_libro'),  # Edición por ID
    path('libros/<int:libro_id>/eliminar/', views.eliminar_libro, name='eliminar_libro'),  # Eliminación
    
    # RUTAS DE AUTORES
    path('autores/', views.lista_autores, name='autores'),
    path('autores/nuevo/', views.crear_autor, name='crear_autor'),
    path('autores/<int:autor_id>/editar/', views.editar_autor, name='editar_autor'),
    path('autores/<int:autor_id>/eliminar/', views.eliminar_autor, name='eliminar_autor'),
    
    # RUTAS DE PRÉSTAMOS
    path('prestamos/', views.lista_prestamos, name='prestamos'),
    path('prestamos/nuevo/', views.crear_prestamo, name='crear_prestamo'),
    path('prestamos/<int:prestamo_id>/editar/', views.editar_prestamo, name='editar_prestamo'),
    path('prestamos/<int:prestamo_id>/eliminar/', views.eliminar_prestamo, name='eliminar_prestamo'),
    
    # RUTAS DE AUTENTICACIÓN
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.Cerrarsesion, name='logout'),
]