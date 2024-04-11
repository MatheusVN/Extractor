@echo off

set VENV_NAME=C:\Qlik\scripts\xml_esocial_env

if not exist "%VENV_NAME%" (
    python -m virtualenv %VENV_NAME%
)

REM
call %VENV_NAME%\Scripts\activate

pip install -r C:\Qlik\scripts\requirements.txt

python C:\Qlik\scripts\process_xmls.py

deactivate
