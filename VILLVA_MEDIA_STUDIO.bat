@echo off
chcp 65001 >nul 2>&1
title VILLVA MEDIA STUDIO
cd /d "%~dp0"

echo.
echo  ================================================
echo        VILLVA MEDIA STUDIO
echo        Tamil-first AI Video Studio
echo  ================================================
echo.
echo  Starting the studio in your browser...
echo  Stop it later with Ctrl+C in this window.
echo.

uv run streamlit run web\app.py

if errorlevel 1 (
    echo.
    echo  The studio could not start.
    echo  Check that uv is installed, then run: uv sync
    pause
)
