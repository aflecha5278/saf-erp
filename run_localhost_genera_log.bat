@echo off
echo Iniciando proceso... > saf_log.txt

REM Ejecutar migraciones
python manage.py makemigrations >> saf_log.txt 2>&1
python manage.py migrate >> saf_log.txt 2>&1

REM Ejecutar servidor
python manage.py runserver >> saf_log.txt 2>&1

echo Proceso finalizado. >> saf_log.txt




