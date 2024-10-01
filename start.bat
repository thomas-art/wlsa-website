@echo off
set currentDir=%~dp0
cd /d "%currentDir%"

start /b Frpc\frpc.bat
start /b py.bat 1001

