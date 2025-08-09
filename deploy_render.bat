@echo off
echo ==========================
echo Preparando para RENDER...
echo ==========================
REM Activar entorno virtual
call C:\_Tmp\Python\saf\env\Scripts\activate.bat

REM Migraciones
python manage.py makemigrations
python manage.py migrate

REM Generar archivos estáticos para WhiteNoise
python manage.py collectstatic --noinput

REM Confirmar en git y pushear
git add .
git commit -m "Deploy a Render"
git push origin main
pause

