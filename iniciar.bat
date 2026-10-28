@echo off
rem SentinelCloud - iniciador para Windows. Funciona SEM internet.
rem Requer apenas o Python 3.10 ou superior instalado.
rem Como usar: de duplo clique neste arquivo.
chcp 65001 >nul
cd /d "%~dp0"

set "PY="
for %%C in ("py -3" "python" "python3") do (
    if not defined PY (
        %%~C -c "import sys; sys.exit(0 if sys.version_info>=(3,10) else 1)" >nul 2>nul && set "PY=%%~C"
    )
)

if not defined PY (
    echo.
    echo Python 3.10 ou superior nao foi encontrado neste computador.
    echo.
    echo 1. Baixe em https://www.python.org/downloads/
    echo 2. Na instalacao, MARQUE a caixa "Add python.exe to PATH"
    echo 3. Depois de instalar, de duplo clique neste arquivo de novo.
    echo.
    pause
    exit /b 1
)

if not exist "vendor\boto3" (
    echo.
    echo A pasta "vendor" nao foi encontrada. Voce extraiu o projeto inteiro?
    echo Clique com o botao direito no .zip e escolha "Extrair tudo...".
    echo.
    pause
    exit /b 1
)

%PY% run.py %*
echo.
pause
