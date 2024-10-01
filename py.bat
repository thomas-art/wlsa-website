@echo off
chcp 65001
echo successfully set cmd to utf-8.
set currentDir=%~dp0
cd /d "%currentDir%\webpy2"
echo successfully cd to currendir.

echo check if conda exist...
where conda > nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo cannot find conda, use normal python.
    python app.py %1
) ELSE (
    echo checking conda envs...
    conda env list | findstr /C:"pyweb"
    IF %ERRORLEVEL%==0 (
        echo found conda env, use conda env.
        call conda activate pyweb
        python app.py %1
    ) ELSE (
        echo cannot find conda env, use normal python.
        python app.py %1
    )
)
