@echo off
echo ==========================
echo Ejecutando en LOCALHOST...
echo ==========================
REM Activar entorno virtual
call C:\_Tmp\Python\saf\env\Scripts\activate.bat

REM Migraciones
python manage.py makemigrations
python manage.py migrate

REM Ejecutar servidor local
python manage.py runserver

