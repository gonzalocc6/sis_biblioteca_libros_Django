from django.db import models
from django.utils.text import slugify

# Create your models here.
# MODELO: AUTOR
class Autor(models.Model):
    nombre = models.CharField(max_length=100)
    biografia = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.nombre

# MODELO: LIBRO
class Libro(models.Model):
    nombre = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True) 
    genero_musical = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True, null=True)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE)
    # Logica personalizada
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre) 
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre

# MODELO: PRÉSTAMO
class Prestamo(models.Model):
    nombre_lector = models.CharField(max_length=100)
    fecha_prestamo = models.DateField()
    fecha_devolucion = models.DateField(blank=True, null=True)
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)

    def __str__(self):
        return f"Prestado a {self.nombre_lector} - Libro: {self.libro.nombre}"