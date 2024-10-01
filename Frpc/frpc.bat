@echo off
chcp 65001
echo frpc.bat: successfully set cmd to utf-8.
set currentDir=%~dp0
cd /d "%currentDir%"
echo frpc.bat: successfully cd to currendir.
echo frpc.bat: current frpc dir: %cd%
start /b frpc.exe -c frpc.ini
