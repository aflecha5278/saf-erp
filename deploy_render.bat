@echo off
echo =======================================
echo Preparando proyecto para Render
echo =======================================
REM Activar entorno virtual
call env\Scripts\activate

REM Instalar dependencias (aseguramos que whitenoise esté)
pip install -r requirements.txt

REM Recolectar archivos estáticos
python manage.py collectstatic --noinput

echo.
echo Proyecto listo para subir a Render.
echo No olvides hacer git add / commit / push
git add .
git commit -m "Deploy a Render"
git push origin main

pause

