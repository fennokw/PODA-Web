@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\.requirements-sha256" (
    echo Run Setup-PODA.cmd first.
    exit /b 1
)
if not defined PODA_PORT set "PODA_PORT=8787"
set "PYTHONUTF8=1"
echo Open http://127.0.0.1:%PODA_PORT% when the server is ready. Use Ctrl+C to stop.
".venv\Scripts\python.exe" -m poda_app.server
