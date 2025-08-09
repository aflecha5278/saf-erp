@echo off
echo ================================
echo Iniciando servidor LOCAL Django
echo ================================
REM Activar entorno virtual
call env\Scripts\activate

REM Correr migraciones
python manage.py migrate

REM Levantar servidor local
python manage.py runserver


