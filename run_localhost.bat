@echo off 
echo ====================================== 
echo Ejecutando migraciones de Django 
echo ====================================== 
python manage.py makemigrations 
python manage.py migrate 
python manage.py collectstatic 
echo ====================================== 
echo Levantando servidor local Django... 
echo ====================================== 
python manage.py runserver 
pause


