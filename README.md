# Sistema Biblioteca Musical

## Descripción
Sistema de gestión repositorio automatizado para el control de inventario de libros de música, catálogo de autores y registro de préstamos de alumnos con persistencia en PostgreSQL y seguridad de roles.

## Requisitos
- Python 3.13.3  
- Django 6.0.6
- PostgreSQL 14
- Psycopg2 (Conector de base de datos)
## Instalación

1. Clonar el repositorio:
```bash
git clone git@github.com:tu-usuario/biblioteca-musical.git
cd biblioteca-musical
```

2. Crear entorno virtual:
```bash
python -m venv entorno
source entorno/bin/activate  # En Windows: entorno\Scripts\activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Aplicar migraciones en PostgreSQL:
```bash
python manage.py makemigrations
python manage.py migrate
```
5. Crear cuenta de Administrador:
```bash
python manage.py createsuperuser
```
6. Iniciar servidor:
```bash
python manage.py runserver
```

## Autor
Gonzalo Cruz
Rosa 