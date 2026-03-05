@echo off
cd /d "%~dp0"
echo Running funnel (view -> cart -> purchase) on data\kaggle_data\...
echo.
python scripts/run_funnel.py
echo.
pause
