@echo off
cd /d C:\_Tmp\Python\saf
call env\Scripts\activate.bat
python manage.py runserver
pause
