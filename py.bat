@echo off
chcp 65001
echo py.bat: successfully set cmd to utf-8.
set currentDir=%~dp0
cd /d "%currentDir%\webpy2"
echo py.bat: successfully cd to currendir.
echo py.bat: current py dir: %cd%

echo py.bat: check if conda exist...
where conda > nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo py.bat: cannot find conda, use normal python.
    python -B app.py %1
) ELSE (
    echo py.bat: checking conda envs...
    conda env list | findstr /C:"pyweb"
    IF %ERRORLEVEL%==0 (
        echo py.bat: found conda env, use conda env.
        call conda activate pyweb
        python -B app.py %1
    ) ELSE (
        echo py.bat: cannot find conda env, use normal python.
        python -B app.py %1
    )
)
