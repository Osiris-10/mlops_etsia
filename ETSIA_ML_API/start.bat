@echo off
REM Script de démarrage rapide pour Windows

echo ==========================================
echo API de Detection de Depression
echo ==========================================
echo.

REM Verifier Python
python --version >nul 2>&1
if errorlevel 1 (
    echo X Python n'est pas installe
    pause
    exit /b 1
)

echo + Python detecte

REM Creer environnement virtuel si necessaire
if not exist "venv" (
    echo Creation de l'environnement virtuel...
    python -m venv venv
)

REM Activer environnement virtuel
echo Activation de l'environnement virtuel...
call venv\Scripts\activate.bat

REM Installer dependances
echo Installation des dependances...
pip install -q -r requirements.txt

REM Verifier .env
if not exist ".env" (
    echo Fichier .env non trouve
    echo Copie de .env.example vers .env...
    copy .env.example .env
    echo.
    echo IMPORTANT: Editez le fichier .env avec vos cles API !
    echo.
    pause
)

REM Lancer l'API
echo.
echo ==========================================
echo Lancement de l'API...
echo ==========================================
echo.
echo URL: http://localhost:8000
echo Documentation: http://localhost:8000/docs
echo.
echo Appuyez sur Ctrl+C pour arreter
echo.

uvicorn app.main:app --reload --port 8000
