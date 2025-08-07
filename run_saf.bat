@echo off
cd /d C:\_Tmp\Python\saf
call env\Scripts\activate.bat
echo === Ejecutando migraciones ===
python manage.py makemigrations
python manage.py migrate
echo === Iniciando servidor Django ===
python manage.py runserver
pause
